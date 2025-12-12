# tests/test_ad_scoring.py
import unittest
from ad_scoring import score_ad

class TestAdScoring(unittest.TestCase):
    def test_basic_score_mid(self):
        features = {"ctr": 0.02, "relevance": 0.8, "budget_ratio": 0.5}
        s = score_ad(features)
        # compute expected value by same formula or assert range
        self.assertGreaterEqual(s, 0)
        self.assertLessEqual(s, 100)

    def test_zero_features(self):
        s = score_ad({})
        self.assertEqual(s, 0.0)

    def test_high_ctr_caps_at_100(self):
        features = {"ctr": 1.0, "relevance": 1.0, "budget_ratio": 1.0}
        self.assertEqual(score_ad(features), 100.0)

if __name__ == "__main__":
    unittest.main()
