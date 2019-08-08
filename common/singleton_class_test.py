# -*- coding: utf-8 -*-
from common.singleton_class import Singleton
import unittest


class A(object, metaclass=Singleton):
    def __init__(self):
        self.test_attr = 'Sample Text'

    def do_somethings(self):
        self.test_attr = 'Change text'


class TestSingleton(unittest.TestCase):
    def test_singleton(self):
        object_a = A()
        object_a.do_somethings()

        object_b = A()

        self.assertEqual(object_b.test_attr, 'Change text')
