# Unit tests for the RequestData class
import sys
sys.path.append("DataInteractionClient")

import unittest

from DataInteractionClient.models.request_data import RequestData


class TestRequestData(unittest.TestCase):
    def setUp(self):
        self.request_data = RequestData(
            {
                "from_time": 10000,
                "to_time": 55555,
                "tag_id": "tag_id",
                "max_count": 5,
                "time_step": 856,
                "value": int,
                "format_param": "format_param",
                "actual": True,
            }
        )

    def test_init_valid_params(self):
        self.assertEqual(self.request_data.tag_id, "tag_id")

    def test_update_valid_params(self):
        self.request_data.update(
            from_time="2022-01-01T00:00:00",
            to_time="2022-01-02T00:00:00",
            max_count=100,
            time_step=1000000,
            value=[int, float],
            format_param=True,
            actual=True,
        )
        self.assertEqual(self.request_data.from_time, "2022-01-01T00:00:00")
        self.assertEqual(self.request_data.to_time, "2022-01-02T00:00:00")
        self.assertEqual(self.request_data.max_count, 100)
        self.assertEqual(self.request_data.time_step, 1000000)
        self.assertEqual(self.request_data.value, [int, float])
        self.assertTrue(self.request_data.format_param)
        self.assertTrue(self.request_data.actual)

    def test_update_invalid_tag_id(self):
        with self.assertRaises(ValueError):
            self.request_data.update(["tag1", 123])

    def test_init_invalid_time(self):
        with self.assertRaises(ValueError):
            self.request_data.update(from_time=[3213])

    def test_update_invalid_time(self):
        with self.assertRaises(ValueError):
            self.request_data.update(from_time=[123])

    def test_init_invalid_max_count(self):
        with self.assertRaises(ValueError):
            self.request_data.update(max_count="43234")

    def test_update_invalid_max_count(self):
        with self.assertRaises(ValueError):
            self.request_data.update(max_count="100")

    def test_init_invalid_time_step(self):
        with self.assertRaises(ValueError):
            self.request_data.update(time_step="23442")

    def test_update_invalid_time_step(self):
        with self.assertRaises(ValueError):
            self.request_data.update(time_step="1000000")

    def test_init_invalid_value(self):
        with self.assertRaises(ValueError):
            self.request_data.update(value="int")

    def test_update_invalid_value(self):
        with self.assertRaises(ValueError):
            self.request_data.update(value="int")

    def test_init_invalid_value_list(self):
        with self.assertRaises(ValueError):
            self.request_data.update(value=["int", float])

    def test_update_invalid_value_list(self):
        with self.assertRaises(ValueError):
            self.request_data.update(value=[int, "float"])


if __name__ == "__main__":
    unittest.main()
