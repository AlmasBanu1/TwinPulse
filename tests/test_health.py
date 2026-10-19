import unittest
from urllib.request import urlopen
import json


class TestTwinPulseHealth(unittest.TestCase):
    def test_health_endpoint(self):
        with urlopen("http://127.0.0.1:8000/api/health", timeout=5) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode("utf-8"))

        self.assertTrue(data["success"])
        self.assertEqual(data["service"], "TwinPulse API")
        self.assertTrue(data["model_loaded"])
        self.assertTrue(data["digital_twin_engine_loaded"])


if __name__ == "__main__":
    unittest.main()
