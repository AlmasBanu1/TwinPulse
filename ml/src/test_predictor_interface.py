
import unittest

from predictor_interface import TwinPulsePredictor, FEATURES


class TestTwinPulsePredictor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.predictor = TwinPulsePredictor()

    def test_valid_input_returns_expected_fields(self):
        patient = {
            "age": 60,
            "bmi": 27.0,
            "sbp": 145,
            "dbp": 90,
            "imt_max": 0.9,
            "lvmi": 110,
            "ef": 60,
            "gender": "M",
            "smoker": "No",
        }

        result = self.predictor.predict(patient)

        self.assertIn("prediction", result)
        self.assertIn("exploratory_score", result)
        self.assertIn("interpretation", result)
        self.assertIn(result["prediction"], [0, 1])
        self.assertGreaterEqual(result["exploratory_score"], 0.0)
        self.assertLessEqual(result["exploratory_score"], 1.0)

    def test_missing_feature_is_rejected(self):
        patient = {
            "age": 60,
            "bmi": 27.0,
            "sbp": 145,
            "dbp": 90,
            "imt_max": 0.9,
            "lvmi": 110,
            "ef": 60,
            "gender": "M",
        }

        with self.assertRaisesRegex(
            ValueError, "Missing required features"
        ):
            self.predictor.predict(patient)

    def test_nonnumeric_age_is_rejected(self):
        patient = {
            "age": "not-a-number",
            "bmi": 27.0,
            "sbp": 145,
            "dbp": 90,
            "imt_max": 0.9,
            "lvmi": 110,
            "ef": 60,
            "gender": "M",
            "smoker": "No",
        }

        with self.assertRaisesRegex(ValueError, "age"):
            self.predictor.predict(patient)


if __name__ == "__main__":
    unittest.main()
