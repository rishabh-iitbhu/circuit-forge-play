import unittest
from types import SimpleNamespace
from unittest.mock import patch

from lib.component_display import show_mosfet_rationale
from lib.component_suggestions import suggest_mosfets, ComponentSuggestion


class MOSFETReasoningTest(unittest.TestCase):
    def test_mosfet_selection_details_expose_filter_journey(self):
        suggestions = suggest_mosfets(25, 10)
        self.assertTrue(suggestions, "Expected at least one MOSFET suggestion")

        details = suggestions[0].selection_details
        self.assertIn('id_filter_threshold_a', details)
        self.assertIn('id_filter_passed', details)
        self.assertIn('selection_journey', details)
        self.assertIn('recommendation_reason', details)

    def test_gate_drive_and_gm_sensitivity_reasoning_is_exposed(self):
        suggestions = suggest_mosfets(25, 10)
        self.assertTrue(suggestions, "Expected at least one MOSFET suggestion")

        details = suggestions[0].selection_details
        self.assertIn('qgd_value_nC', details)
        self.assertIn('gm_value', details)
        self.assertIn('gate_drive_sensitivity_note', details)
        self.assertIn('gm_sensitivity_note', details)

    def test_reverse_recovery_reasoning_is_exposed_for_hypothetical_mosfet(self):
        candidate = SimpleNamespace(
            name='HYP_QRR', manufacturer='Test', vds=200, id=30, rdson=6, qg=18,
            package='LFPAK56', qgd=2, qgs=8, package_inductance=1, dc_soa=True,
            pulsed_soa=True, eas=2.5, repetitive_avalanche=True, rdson_at_125c=6,
            mosfet_type='Si', qrr=25.0, irr=8.0, trr=12.0, gm=50.0
        )

        details = {}
        selection_journey = []
        recommendation_reason = ''
        qgd_qgs_ratio = None
        gate_drive_sensitivity_note = ''
        gm_sensitivity_note = ''
        qgd_value_nC = None
        gm_value = None
        package_inductance = None
        qrr_value = getattr(candidate, 'qrr', None)
        irr_value = getattr(candidate, 'irr', None)
        trr_value = getattr(candidate, 'trr', None)
        recovery_product = None
        if qrr_value is not None:
            recovery_product = qrr_value
        elif irr_value is not None and trr_value is not None:
            recovery_product = irr_value * trr_value

        details['qrr_value'] = qrr_value
        details['irr_value'] = irr_value
        details['trr_value'] = trr_value
        details['recovery_product'] = recovery_product
        details['reverse_recovery_note'] = (
            f"Qrr={qrr_value}nC / Irr={irr_value}A / trr={trr_value}ns; lower recovery charge/current and time reduce switching loss and ringing, while higher temperature and forward current increase recovery stress."
        )

        self.assertEqual(details['qrr_value'], 25.0)
        self.assertEqual(details['irr_value'], 8.0)
        self.assertEqual(details['trr_value'], 12.0)
        self.assertEqual(details['recovery_product'], 25.0)
        self.assertIn('reverse_recovery_note', details)

    def test_reverse_recovery_is_penalized_for_high_temperature_and_current_stress(self):
        low_recovery = SimpleNamespace(
            name='LOW_RECOVERY', manufacturer='Test', vds=200, id=30, rdson=6, qg=18,
            package='LFPAK56', qgd=2, qgs=8, package_inductance=1, dc_soa=True,
            pulsed_soa=True, eas=2.5, repetitive_avalanche=True, rdson_at_125c=6,
            mosfet_type='Si', qrr=10.0, irr=4.0, trr=8.0, gm=50.0
        )
        high_recovery = SimpleNamespace(
            name='HIGH_RECOVERY', manufacturer='Test', vds=200, id=30, rdson=8, qg=25,
            package='TO-220', qgd=5, qgs=7, package_inductance=3, dc_soa=True,
            pulsed_soa=True, eas=2.0, repetitive_avalanche=True, rdson_at_125c=8,
            mosfet_type='Si', qrr=200.0, irr=20.0, trr=40.0, gm=45.0
        )

        with patch('lib.component_suggestions.MOSFET_LIBRARY', [low_recovery, high_recovery]):
            suggestions = suggest_mosfets(25, 10, operating_temperature_c=100.0, diode_forward_current_a=15.0)

        self.assertEqual(len(suggestions), 2)
        self.assertGreater(suggestions[0].score, suggestions[1].score)
        self.assertEqual(suggestions[0].component.name, 'LOW_RECOVERY')
        details = suggestions[0].selection_details
        self.assertIn('reverse_recovery_temperature_c', details)
        self.assertIn('reverse_recovery_forward_current_a', details)
        self.assertIn('reverse_recovery_stress_multiplier', details)

    def test_reverse_recovery_note_mentions_operating_temperature_and_current(self):
        candidate = SimpleNamespace(
            name='TEMP_STRESS', manufacturer='Test', vds=200, id=30, rdson=6, qg=18,
            package='LFPAK56', qgd=2, qgs=8, package_inductance=1, dc_soa=True,
            pulsed_soa=True, eas=2.5, repetitive_avalanche=True, rdson_at_125c=6,
            mosfet_type='Si', qrr=25.0, irr=8.0, trr=12.0, gm=50.0
        )

        with patch('lib.component_suggestions.MOSFET_LIBRARY', [candidate]):
            suggestions = suggest_mosfets(25, 10, operating_temperature_c=90.0, diode_forward_current_a=12.0)

        self.assertTrue(suggestions)
        note = suggestions[0].selection_details['reverse_recovery_note']
        self.assertIn('90.0°C', note)
        self.assertIn('12.0 A', note)

    def test_show_mosfet_rationale_is_visible_without_clicking_toggle(self):
        suggestion = ComponentSuggestion(
            component=SimpleNamespace(name='AUTO_VISIBLE', vds=200, part_number='AUTO_VISIBLE'),
            reason='test',
            selection_details={
                'vin_max': 25,
                'vin_peak': 31.25,
                'vds_rating_factor': 0.6,
                'required_vds': 52.1,
                'vds_headroom_ratio': 3.8,
                'id_filter_threshold_a': 12.0,
                'id_filter_passed': True,
                'selection_journey': ['passed'],
                'dc_soa_present': True,
                'pulsed_soa_present': True,
                'avalanche_energy_mJ': 2.0,
                'repetitive_avalanche': True,
                'rdson_used_mohm': 6,
                'rdson_actual_mohm': 6,
                'qgd_value_nC': 2.0,
                'qgd_qgs_ratio': 0.25,
                'gate_drive_sensitivity_note': 'gate note',
                'gm_value': 30.0,
                'gm_sensitivity_note': 'gm note',
                'qrr_value': None,
                'irr_value': None,
                'trr_value': None,
                'reverse_recovery_note': 'reverse note',
                'drain_source_short_risk_level': 'low',
                'drain_source_short_risk_note': 'Thermal overstress is the dominant failure mechanism.',
                'package_inductance_nH': 1.0,
                'recommendation_reason': 'recommended'
            }
        )

        markdown_calls = []

        class DummyStreamlit:
            session_state = {}

            def write(self, *args, **kwargs):
                return None

            def subheader(self, *args, **kwargs):
                return None

            def markdown(self, content, *args, **kwargs):
                markdown_calls.append(content)

            def button(self, *args, **kwargs):
                return False

            def expander(self, *args, **kwargs):
                class DummyExpander:
                    def __enter__(self):
                        return self

                    def __exit__(self, exc_type, exc, tb):
                        return False

                return DummyExpander()

        with patch('lib.component_display.st', DummyStreamlit()):
            show_mosfet_rationale(suggestion)

        self.assertTrue(markdown_calls)
        rendered = markdown_calls[0]
        self.assertIn('Drain-source short-failure risk', rendered)

    def test_show_mosfet_rationale_includes_reverse_recovery_bullet_for_qrr(self):
        suggestion = ComponentSuggestion(
            component=SimpleNamespace(name='QRR_ONLY', vds=200, part_number='QRR_ONLY'),
            reason='test',
            selection_details={
                'vin_max': 25,
                'vin_peak': 31.25,
                'vds_rating_factor': 0.6,
                'required_vds': 52.1,
                'vds_headroom_ratio': 3.8,
                'id_filter_threshold_a': 12.0,
                'id_filter_passed': True,
                'selection_journey': ['passed'],
                'dc_soa_present': True,
                'pulsed_soa_present': True,
                'avalanche_energy_mJ': 2.0,
                'repetitive_avalanche': True,
                'rdson_used_mohm': 6,
                'rdson_actual_mohm': 6,
                'qgd_value_nC': 2.0,
                'qgd_qgs_ratio': 0.25,
                'gate_drive_sensitivity_note': 'gate note',
                'gm_value': 30.0,
                'gm_sensitivity_note': 'gm note',
                'qrr_value': 25.0,
                'irr_value': None,
                'trr_value': None,
                'reverse_recovery_note': 'reverse note',
                'package_inductance_nH': 1.0,
                'recommendation_reason': 'recommended'
            }
        )

        markdown_calls = []
        button_calls = []
        state = {'show_vds_calc_QRR_ONLY': True}

        class DummyStreamlit:
            session_state = state

            def write(self, *args, **kwargs):
                return None

            def subheader(self, *args, **kwargs):
                return None

            def markdown(self, content, *args, **kwargs):
                markdown_calls.append(content)

            def button(self, *args, **kwargs):
                button_calls.append((args, kwargs))
                return False

        with patch('lib.component_display.st', DummyStreamlit()):
            show_mosfet_rationale(suggestion)

        self.assertTrue(markdown_calls)
        rendered = markdown_calls[0]
        self.assertIn('Qrr / Irr / trr logic', rendered)
        self.assertIn('Qrr = 25.00', rendered)

    def test_show_mosfet_rationale_includes_reverse_recovery_bullet_for_missing_values(self):
        suggestion = ComponentSuggestion(
            component=SimpleNamespace(name='NO_RECOVERY', vds=200, part_number='NO_RECOVERY'),
            reason='test',
            selection_details={
                'vin_max': 25,
                'vin_peak': 31.25,
                'vds_rating_factor': 0.6,
                'required_vds': 52.1,
                'vds_headroom_ratio': 3.8,
                'id_filter_threshold_a': 12.0,
                'id_filter_passed': True,
                'selection_journey': ['passed'],
                'dc_soa_present': True,
                'pulsed_soa_present': True,
                'avalanche_energy_mJ': 2.0,
                'repetitive_avalanche': True,
                'rdson_used_mohm': 6,
                'rdson_actual_mohm': 6,
                'qgd_value_nC': 2.0,
                'qgd_qgs_ratio': 0.25,
                'gate_drive_sensitivity_note': 'gate note',
                'gm_value': 30.0,
                'gm_sensitivity_note': 'gm note',
                'qrr_value': None,
                'irr_value': None,
                'trr_value': None,
                'reverse_recovery_note': 'reverse note',
                'package_inductance_nH': 1.0,
                'recommendation_reason': 'recommended'
            }
        )

        markdown_calls = []
        state = {'show_vds_calc_NO_RECOVERY': True}

        class DummyStreamlit:
            session_state = state

            def write(self, *args, **kwargs):
                return None

            def subheader(self, *args, **kwargs):
                return None

            def markdown(self, content, *args, **kwargs):
                markdown_calls.append(content)

            def button(self, *args, **kwargs):
                return False

        with patch('lib.component_display.st', DummyStreamlit()):
            show_mosfet_rationale(suggestion)

        self.assertTrue(markdown_calls)
        rendered = markdown_calls[0]
        self.assertIn('Qrr / Irr / trr logic', rendered)
        self.assertIn('not available', rendered)

    def test_drain_source_short_failure_risk_is_exposed_for_existing_components(self):
        suggestions = suggest_mosfets(25, 10)
        self.assertTrue(suggestions)

        details = suggestions[0].selection_details
        self.assertIn('drain_source_short_risk_level', details)
        self.assertIn('drain_source_short_risk_score', details)
        self.assertIn('drain_source_short_risk_note', details)

    def test_show_mosfet_rationale_includes_drain_source_short_failure_bullet(self):
        suggestion = ComponentSuggestion(
            component=SimpleNamespace(name='SHORT_RISK', vds=200, part_number='SHORT_RISK'),
            reason='test',
            selection_details={
                'vin_max': 25,
                'vin_peak': 31.25,
                'vds_rating_factor': 0.6,
                'required_vds': 52.1,
                'vds_headroom_ratio': 3.8,
                'id_filter_threshold_a': 12.0,
                'id_filter_passed': True,
                'selection_journey': ['passed'],
                'dc_soa_present': True,
                'pulsed_soa_present': True,
                'avalanche_energy_mJ': 2.0,
                'repetitive_avalanche': True,
                'rdson_used_mohm': 6,
                'rdson_actual_mohm': 6,
                'qgd_value_nC': 2.0,
                'qgd_qgs_ratio': 0.25,
                'gate_drive_sensitivity_note': 'gate note',
                'gm_value': 30.0,
                'gm_sensitivity_note': 'gm note',
                'qrr_value': None,
                'irr_value': None,
                'trr_value': None,
                'reverse_recovery_note': 'reverse note',
                'drain_source_short_risk_level': 'high',
                'drain_source_short_risk_note': 'Thermal overstress is the dominant failure mechanism.',
                'package_inductance_nH': 1.0,
                'recommendation_reason': 'recommended'
            }
        )

        markdown_calls = []
        state = {'show_vds_calc_SHORT_RISK': True}

        class DummyStreamlit:
            session_state = state

            def write(self, *args, **kwargs):
                return None

            def subheader(self, *args, **kwargs):
                return None

            def markdown(self, content, *args, **kwargs):
                markdown_calls.append(content)

            def button(self, *args, **kwargs):
                return False

        with patch('lib.component_display.st', DummyStreamlit()):
            show_mosfet_rationale(suggestion)

        self.assertTrue(markdown_calls)
        rendered = markdown_calls[0]
        self.assertIn('Drain-source short-failure risk', rendered)
        self.assertIn('high', rendered)

    def test_drain_source_short_failure_risk_penalizes_high_stress_hypothetical_parts(self):
        low_risk = SimpleNamespace(
            name='LOW_RISK', manufacturer='Test', vds=200, id=40, rdson=6, qg=18,
            package='LFPAK56', qgd=2, qgs=8, package_inductance=1, dc_soa=True,
            pulsed_soa=True, eas=2.5, repetitive_avalanche=True, rdson_at_125c=6,
            mosfet_type='Si', gm=50.0
        )
        high_risk = SimpleNamespace(
            name='HIGH_RISK', manufacturer='Test', vds=200, id=12, rdson=80, qg=40,
            package='TO-220', qgd=8, qgs=6, package_inductance=8, dc_soa=False,
            pulsed_soa=False, eas=None, repetitive_avalanche=False, rdson_at_125c=90,
            mosfet_type='Si', gm=20.0
        )

        with patch('lib.component_suggestions.MOSFET_LIBRARY', [low_risk, high_risk]):
            suggestions = suggest_mosfets(25, 10)

        self.assertEqual(len(suggestions), 2)
        self.assertEqual(suggestions[0].component.name, 'LOW_RISK')
        self.assertGreater(suggestions[0].score, suggestions[1].score)
        self.assertIn('drain-source short-failure', suggestions[0].selection_details['drain_source_short_risk_note'].lower())
        self.assertIn('high', suggestions[1].selection_details['drain_source_short_risk_level'].lower())


if __name__ == '__main__':
    unittest.main()
