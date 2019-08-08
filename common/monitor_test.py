import unittest
import json
from common.monitor import _get_log_string


class MonitorTest(unittest.TestCase):
    def test_basic_case(self):
        result = _get_log_string(
            'some_id',
            int_value=1,
            message='nothing is better than this')
        self.assertEqual(
            json.loads(result),
            {"monitor_id": "some_id", "int_value": 1,
             "message": "nothing is better than this", "float_value": 0})
