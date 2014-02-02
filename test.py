#!/usr/bin/python

import unittest
from util import shape_dict
from plot import single_boxplot, multi_boxplot
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

if __name__ == "__main__":
	unittest.main()
