import unittest
import time
from common.tictoc import Tictoc


class TicTocTest(unittest.TestCase):
    def test_basic_case(self):
        Tictoc.tic('SCANNER')
        time.sleep(0.2)
        result = Tictoc.toc('SCANNER')
        self.assertEqual(float("{0:.1f}".format(result / 1000)), 0.2)
