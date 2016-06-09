#!/usr/bin/python

"""Usage:
    test.py plot_single
    test.py plot_multi
    test.py test_shape_dict
"""

from docopt import docopt
from util import shape_dict
from plot import single_boxplot, multi_boxplot
import numpy as np

def plot_single():
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

def plot_multi():
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

def test_shape_dict():
    data = [
        (('a1', 0.5, 10, 555,), [1, ] ),
        (('a1', 0.5, 15, 555,), [2, ] ),
        (('a1', 0.6, 10, 555,), [3, ] ),
        (('a1', 0.6, 15, 555,), [4, ] ),
        (('a2', 0.5, 10, 555,), [5, ] ),
        (('a2', 0.5, 15, 555,), [6, ] ),
        (('a2', 0.6, 10, 555,), [7, ] ),
        (('a2', 0.6, 15, 555,), [8, ] ),
        (('a1', 0.5, 10, 555,), [11,] ),
        (('a1', 0.5, 15, 555,), [12,] ),
        (('a1', 0.6, 10, 555,), [13,] ),
        (('a1', 0.6, 15, 555,), [14,] ),
        (('a2', 0.5, 10, 555,), [15,] ),
        (('a2', 0.5, 15, 555,), [16,] ),
        (('a2', 0.6, 10, 555,), [17,] ),
        (('a2', 0.6, 15, 555,), [18,] ),
    ]

    sd = shape_dict(data,0,1,2)
    for k, v in sd.iteritems():
        print " ", k
        for kk,vv in v.iteritems():
            print "  ",kk
            for kkk,vvv in vv.iteritems():
                print "   ",kkk, vvv

if __name__ == "__main__":
    args = docopt(__doc__)
    if args['plot_single']:
        plot_single()
    elif args['plot_multi']:
        plot_multi()
    elif args['test_shape_dict']:
        test_shape_dict()

