import unittest
from types import SimpleNamespace

from lib.component_suggestions import evaluate_mosfet_candidate, suggest_mosfets


class MOSFETReasoningTest(unittest.TestCase):
    def test_mosfet_selection_details_expose_filter_journey(self):
        suggestions = suggest_mosfets(25, 10)
        self.assertTrue(suggestions, "Expected at least one MOSFET suggestion")

        details = suggestions[0].selection_details
        self.assertIn('id_filter_threshold_a', details)
        self.assertIn('id_filter_passed', details)
        self.assertIn('selection_journey', details)
        self.assertIn('recommendation_reason', details)

    def test_edge_case_and_non_edge_case_synthetic_mosfets(self):
        good_candidate = SimpleNamespace(
            name='EDGE_GOOD', manufacturer='Test', vds=200, id=30, rdson=6, qg=18,
            package='LFPAK56', qgd=2, qgs=8, package_inductance=1, dc_soa=True,
            pulsed_soa=True, eas=2.5, repetitive_avalanche=True, rdson_at_125c=6,
            mosfet_type='Si'
        )
        bad_candidate = SimpleNamespace(
            name='EDGE_BAD', manufacturer='Test', vds=60, id=8, rdson=80, qg=80,
            package='TO-220', qgd=40, qgs=4, package_inductance=12, dc_soa=False,
            pulsed_soa=False, eas=None, repetitive_avalanche=False, rdson_at_125c=90,
            mosfet_type='Si'
        )
        borderline_candidate = SimpleNamespace(
            name='BORDERLINE', manufacturer='Test', vds=80, id=12, rdson=20, qg=30,
            package='TO-220', qgd=5, qgs=12, package_inductance=2, dc_soa=True,
            pulsed_soa=True, eas=1.0, repetitive_avalanche=True, rdson_at_125c=20,
            mosfet_type='Si'
        )

        good_result = evaluate_mosfet_candidate(good_candidate, 25, 10)
        self.assertIsNotNone(good_result)
        self.assertTrue(good_result['passed_filters'])
        self.assertTrue(good_result['selection_details']['id_filter_passed'])

        bad_result = evaluate_mosfet_candidate(bad_candidate, 25, 10)
        self.assertIsNone(bad_result)

        borderline_result = evaluate_mosfet_candidate(borderline_candidate, 25, 10)
        self.assertIsNotNone(borderline_result)
        self.assertTrue(borderline_result['selection_details']['id_filter_passed'])


if __name__ == '__main__':
    unittest.main()
