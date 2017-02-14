#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
////////////////////////////////////////////////

tests.filterTests.py
Created on Mon Dec 12 11:21 2016
@author: jsrhu

TEST FILE

////////////////////////////////////////////////
------------------------------------
Packages
------------------------
STDLIB:
unittest

MAINTAINED:

CUSTOM:
directory
parsers

------------------------------------
Constants
------------------------
Integers: int
------------

------------------------
Long: long
------------

------------------------
Floats: float
------------

------------------------
Complex: complex
------------

------------------------
Strings: str
------------

------------------------
Arrays: list
------------

------------------------
Tuple: (x,y)
------------

------------------------
Sets: set
------------

------------------------
Frozen Set: frozenset
------------

------------------------
Dictionary: {'x':x,'y':y}
------------

------------------------------------
Functions
------------------------
Public
------------

------------------------
Private
------------

------------------------------------
Classes
------------------------
Public
------------

------------------------
Private
------------

////////////////////////////////////////////

TODO:
Implement tests

////////////////////////////////////////////////
"""
import pandas as pd
import datetime as dt

import unittest2 as unittest

test_domains = ['a.com','b.org','c.net','d.gov','e.xyz']

test_span = dt.timedelta(days=10)

candidate_average = 1/2.0
whitelist_average = 1/1.0

class tests(unittest.TestCase):

    def testUpdate(self):
        self.assertEqual('foo'.upper(),'FOO')

    def testIsupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def testSplit(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def testFail(self):
        self.failIf(True, 'value is set to True')

    def testError(self):
        raise RuntimeError('Test error!')

    def testFailUnless(self):
        self.failUnless(True)

    def testAssertTrue(self):
        self.assertTrue(True)

    def testFailIf(self):
        self.failIf(False)

    def testAssertFalse(self):
        self.assertFalse(False)

    def testEqual(self):
        self.failUnlessEqual(1, 3-2)

    def testNotEqual(self):
        self.failIfEqual(2, 3-2)

    def testEqualAgain(self):
        self.failIfEqual(1, 3-2)

    def testNotEqualAgain(self):
        self.failUnlessEqual(2, 3-2)

    def testNotAlmostEqual(self):
        self.failIfAlmostEqual(1.1, 3.3-2.0, places=1)

    def testAlmostEqual(self):
        self.failUnlessAlmostEqual(1.1, 3.3-2.0, places=0)

def raises_error(*args, **kwds):
    print args, kwds
    raise ValueError('Invalid value: ' + str(args) + str(kwds))

class ExceptionTest(unittest.TestCase):

    def testTrapLocally(self):
        try:
            raises_error('a', b='c')
        except ValueError:
            pass
        else:
            self.fail('Did not see ValueError')

    def testFailUnlessRaises(self):
        self.failUnlessRaises(ValueError, raises_error, 'a', b='c')

class FixturesTest(unittest.TestCase):

    def setUp(self):
        print 'In setUp()'
        self.fixture = range(1, 10)

    def tearDown(self):
        print 'In tearDown()'
        del self.fixture

    def test(self):
        print 'in test()'
        self.failUnlessEqual(self.fixture, range(1, 10))

if __name__ == '__main__':
    unittest.main()
