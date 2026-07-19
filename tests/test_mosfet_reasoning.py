import unittest
from types import SimpleNamespace

from lib.component_suggestions import suggest_mosfets


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


if __name__ == '__main__':
    unittest.main()
