"""Measures latency of functions."""
import logging
import time


class Tictoc(object):
    """Singleton class to store and retrieve latency data by tags."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Tictoc, cls).__new__(cls, *args, **kwargs)
            cls.TIC_TIME = None
            cls.TOC_TIME = None
        return cls._instance

    @staticmethod
    def getTictocIns():
        ins = Tictoc()
        return ins

    @staticmethod
    def tic(tag=None):
        """Marks the start to measure."""
        if tag is None:
            tag = 'default'

        ins = Tictoc.getTictocIns()
        try:
            ins.TIC_TIME[tag] = time.time()
        except (NameError, TypeError):
            ins.TIC_TIME = {tag: time.time()}

    @staticmethod
    def toc(tag=None):
        """Marks the end of a measurement uniquely identified by a tag."""
        if tag is None:
            tag = 'default'
        ins = Tictoc.getTictocIns()

        try:
            ins.TOC_TIME[tag] = time.time()
        except (NameError, TypeError):
            ins.TOC_TIME = {tag: time.time()}

        if ins.TIC_TIME:
            duration = ins.TOC_TIME[tag] - ins.TIC_TIME[tag]
            return duration * 1000
        else:
            logging.error(
                'no tic() start time available. Check global var settings')
            return None

