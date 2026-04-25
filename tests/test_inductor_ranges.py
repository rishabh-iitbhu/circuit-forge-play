import os
import sys
import unittest

# Ensure project root is on sys.path for imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pages.buck_calculator import compute_available_inductor_ranges
from lib.component_suggestions import ComponentSuggestion

class MockComp:
    def __init__(self, inductance, current):
        self.inductance = inductance
        self.current = current

class TestInductorRanges(unittest.TestCase):
    def test_local_ranges_from_library(self):
        # Local DB should provide fallback ranges when CSV/XLSX missing
        L_min, L_max, I_min, I_max, ok = compute_available_inductor_ranges(
            required_inductance_uh=5000, max_current=0.5, inductor_suggestions=None, use_web_search=False
        )
        # Expect fallback values present in repository defaults
        self.assertGreater(L_max, 0)
        self.assertGreater(I_max, 0)
        self.assertTrue(isinstance(L_min, (int, float)))
        self.assertTrue(isinstance(I_min, (int, float)))

    def test_web_suggestions_override_ranges(self):
        # Create mock web suggestions with known ranges
        s1 = ComponentSuggestion(component=MockComp(22.0, 2.0), reason="a")
        s2 = ComponentSuggestion(component=MockComp(47.0, 5.0), reason="b")
        L_min, L_max, I_min, I_max, ok = compute_available_inductor_ranges(
            required_inductance_uh=30.0, max_current=1.0, inductor_suggestions=[s1, s2], use_web_search=True
        )
        self.assertEqual(L_min, 22.0)
        self.assertEqual(L_max, 47.0)
        self.assertEqual(I_min, 2.0)
        self.assertEqual(I_max, 5.0)
        # Required inductance 30 is between 22 and 47, and max_current 1.0 <= 5.0 so ok should be True
        self.assertTrue(ok)

if __name__ == '__main__':
    unittest.main()
