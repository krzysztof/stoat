"""Usage:
	test.py unittest
	test.py plot_s
	test.py plot_m
"""

#!/usr/bin/python

import unittest
from docopt import docopt
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

def plot_s():
	data = {
		5: {
			'Alg1': np.random.normal(2.0, 0.2, 20),
			'Alg2': np.random.normal(2.1, 0.2, 20),
			'Alg3': np.random.normal(2.2, 0.2, 20),
		},
		10: {
			'Alg1': np.random.normal(2.3, 0.2, 20),
			'Alg2': np.random.normal(2.4, 0.2, 20),
			'Alg3': np.random.normal(2.5, 0.2, 20),
		},
		15: {
			'Alg1': np.random.normal(2.6, 0.2, 20),
			'Alg2': np.random.normal(2.7, 0.2, 20),
			'Alg3': np.random.normal(2.8, 0.2, 20),
		},
	}
	v2_order = ['Alg1', 'Alg2', 'Alg3']
	v1_order = [5, 10, 15]

	import matplotlib.pyplot as plt
	single_boxplot(data, v1_sorter=lambda l: sorted(l, key=lambda i:i[0]), v2_sorter=v2_order, tick_format="{v2},N={v1}")
	plt.show()
	#single_boxplot(data, v1_sorter=v1_order, v2_sorter=v2_order)

def plot_m():
	data = [
		(('a1', 0.5, 10,), np.random.normal(2.0, 0.2, 20) ),
		(('a1', 0.5, 15,), np.random.normal(2.1, 0.2, 20) ),
		(('a1', 0.6, 10,), np.random.normal(2.2, 0.2, 20) ),
		(('a1', 0.6, 15,), np.random.normal(2.3, 0.2, 20) ),
		(('a2', 0.5, 10,), np.random.normal(2.4, 0.2, 20) ),
		(('a2', 0.5, 15,), np.random.normal(2.5, 0.2, 20) ),
		(('a2', 0.6, 10,), np.random.normal(2.6, 0.2, 20) ),
		(('a2', 0.6, 15,), np.random.normal(2.7, 0.2, 20) ),
	]
	sd = shape_dict(data,2,1,0)

	v2_order = ['a1', 'a2']
	v1_order = [0.5, 0.6]
	multi_boxplot(sd)

if __name__ == "__main__":
	args = docopt(__doc__)
	if args['unittest']:
		unittest.main()
	elif args['plot_s']:
		plot_s()
	elif args['plot_m']:
		plot_m()

