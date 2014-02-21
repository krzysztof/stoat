#!/usr/bin/python

import unittest
from util import shape_dict, nested_dict
import numpy as np

class TestDataDict(unittest.TestCase):

	def setUp(self):
		self.data0 = [
			(('a1', 0.5, 10,), (1,) ),
			(('a1', 0.5, 15,), (2,) ),
			(('a1', 0.6, 10,), (3,) ),
			(('a1', 0.6, 15,), (4,) ),
			(('a2', 0.5, 10,), (5,) ),
			(('a2', 0.5, 15,), (6,) ),
			(('a2', 0.6, 10,), (7,) ),
			(('a2', 0.6, 15,), (8,) ),
		]

	def testShapeDict(self):
		ref_0_1_2 = {
			'a1': { 0.5: { 10: (1,), 15: (2,), }, 0.6: { 10: (3,), 15: (4,), }, },
			'a2': { 0.5: { 10: (5,), 15: (6,), }, 0.6: { 10: (7,), 15: (8,), }, }
		}
		self.assertEquals(shape_dict(self.data0, 0, 1, 2), ref_0_1_2)

		ref_1_2_0 = {
			0.5: { 10: { 'a1': (1,), 'a2': (5,), }, 15: { 'a1': (2,), 'a2': (6,), }, },
			0.6: { 10: { 'a1': (3,), 'a2': (7,), }, 15: { 'a1': (4,), 'a2': (8,), }, },
		}
		self.assertEquals(shape_dict(self.data0, 1, 2, 0), ref_1_2_0)

		ref_2_0_1 = {
			10: { 'a1': { 0.5: (1,), 0.6: (3,), }, 'a2': { 0.5: (5,), 0.6: (7,), }, },
			15: { 'a1': { 0.5: (2,), 0.6: (4,), }, 'a2': { 0.5: (6,), 0.6: (8,), }, },
		}
		self.assertEquals(shape_dict(self.data0, 2, 0, 1), ref_2_0_1)

class TestNestedDict(unittest.TestCase):

	def test_basic(self):

		d1 = nested_dict([[1,2,3],["a","b","c"]])
		ref_d1 = {
				1:{"a":[], "b":[], "c":[]},
				2:{"a":[], "b":[], "c":[]},
				3:{"a":[], "b":[], "c":[]},
			}
		self.assertEquals(d1, ref_d1)

		d2 = nested_dict([[1,2],'xy',[10,20]])
		ref_d2 = {
			1:	{
				'x': { 10: [], 20: [], },
				'y': { 10: [], 20: [], },
				},
			2:	{
				'x': { 10: [], 20: [], },
				'y': { 10: [], 20: [], },
				},
		}
		self.assertEquals(d2, ref_d2)

	def test_values(self):
		"""Tests the various non-default values."""

		d1 = nested_dict([[1,2,3],["a","b","c"]])
		d1[2]['b'].append("foo")
		ref_d1 = {
				1:{"a":[], "b":[], "c":[]},
				2:{"a":[], "b":['foo',], "c":[]},
				3:{"a":[], "b":[], "c":[]},
			}
		self.assertEquals(d1, ref_d1)

		d2 = nested_dict([[1,2,3],["a","b","c"]], value=False)
		d2[1]['a']=True
		d2[3]['c']=True
		ref_d2 = {
				1:{"a":True,  "b":False, "c":False},
				2:{"a":False, "b":False, "c":False},
				3:{"a":False, "b":False, "c":True},
			}
		self.assertEquals(d2, ref_d2)

		d3 = nested_dict([[1,2,3],["a","b","c"]], value=0)
		d3[1]['a']=5
		d3[3]['c']=3
		ref_d3 = {
				1:{"a":5, "b":0, "c":0},
				2:{"a":0, "b":0, "c":0},
				3:{"a":0, "b":0, "c":3},
			}
		self.assertEquals(d3, ref_d3)

if __name__ == "__main__":
	unittest.main()
