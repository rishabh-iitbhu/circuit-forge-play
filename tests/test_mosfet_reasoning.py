import unittest

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


if __name__ == '__main__':
    unittest.main()
