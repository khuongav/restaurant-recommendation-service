"""Adds monitoring info so that logging server can parse."""
import logging
import json

RECOMMENDER_EXCEPTION = 'RECOMMENDER_EXCEPTION'

def add(monitor_id, int_value=0, float_value=0, message=''):
    """
    Args:
        monitor_id -- unique id to identify the monitoring metric, pattern: [a-zA-Z0-9._-]+.
        int_value -- integer value of the metric
        float_value -- float value of the metric
        message -- a string containing other information for this message"""
    logging.info(
        _get_log_string(
            monitor_id,
            int_value,
            float_value,
            message))


def _get_log_string(
        monitor_id,
        int_value=0,
        float_value=0,
        message=''):
    kwargs = {"monitor_id": monitor_id, "int_value": int_value, "float_value": float_value,
              "message": message}
    return '%s' % (json.dumps(kwargs))
