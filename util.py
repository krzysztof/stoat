import pickle, json
import os
import threading, sys

class TimeoutError(Exception): pass

def printf(string):
	"""Print something and flushes the output right away."""
	sys.stdout.write(string)
	sys.stdout.flush()

def timelimit(limit):
	from multiprocessing import Process, Queue
	def wrapper(func):
		def inner(*args, **kwargs):
			def bar(q):
				out = func(*args, **kwargs)
				q.put(out)
			q = Queue()
			p = Process(target=bar, args=[q,])
			p.start()
			p.join(limit)
			if p.is_alive():
				p.terminate()
				p.join()
				raise TimeoutError, "Reached the timelimit of %s seconds" % (limit)

			else:
				return q.get()
		return inner
	return wrapper

def json_obj(filename, obj):
	assert isinstance(filename, str), "First argument must be a string, got %s instead" %(type(filename))
	with open(filename,'w') as f:
		json.dump(obj, f)

def unjson_obj(filename):
	assert isinstance(filename, str), "First argument must be a string, got %s instead" %(type(filename))
	assert os.path.isfile(filename), "File pickle does not exist."

	obj = None
	with open(filename, 'r') as f:
		obj = json.load(f)
	return obj

def pickle_obj(filename, obj):
	assert isinstance(filename, str), "First argument must be a string, got %s instead" %(type(filename))
	with open(filename,'w') as f:
		pickle.dump(obj, f)


def unpickle_obj(filename):
	assert isinstance(filename, str), "First argument must be a string, got %s instead" %(type(filename))
	assert os.path.isfile(filename), "File pickle does not exist."

	obj = None
	with open(filename, 'r') as f:
		obj = pickle.load(f)
	return obj

def nested_dict(keys_list, value=[]):
	"""
	Returns a nested dictionary, with the final value being empty list

	make_nested_dict([[1,2],["a","b"]], value=[])
	d = {
			1:{"a":[], "b":[], "c":[]},
			2:{"a":[], "b":[], "c":[]},
		}
	"""

	if len(keys_list) == 0:
		return type(value)(value)
	d = {}
	for k in keys_list[0]:
		d[k] = nested_dict(keys_list[1:], value=value)
	return d

def shape_dict_bak(data, f_idx, x_idx, m_idx):
	shaped_dict = {}
	fs = list(set(d[0][f_idx] for d in data))
	for f in fs:
		shaped_dict[f] = {}
		xs = list(set(d[0][x_idx] for d in data if d[0][f_idx]==f))
		for x in xs:
			shaped_dict[f][x] = {}
			ms = list(set(d[0][m_idx] for d in data if d[0][f_idx]==f and d[0][x_idx]==x))
			for m in ms:
				ds = [d for d in data if d[0][f_idx]==f and d[0][x_idx]==x and d[0][m_idx]==m]
				if len(ds) != 1:
					raise ValueError, "Combined variables do not separate the data"
				shaped_dict[f][x][m] = ds[0][1]
	return shaped_dict

def shape_dict(data, *args):
	shaped_dict = {}
	assert all(isinstance(arg, int) for arg in args), "Positional arguments must be interegers"
	assert len(args) > 0, "At least one positional argument (int) is required"
	def make_shape(idxs, l):
		if len(idxs)==0:
			orig_type = type(l[0][1])
			return orig_type(sum([list(li[1]) for li in l], []))
		idx = idxs[0]
		keys = list(set(li[0][idx] for li in l))
		d = {}
		for k in keys:
			d[k] = make_shape(idxs[1:], [li for li in l if li[0][idx]==k])
		return d
	
	return make_shape(args, data)
