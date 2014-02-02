import pickle
import os

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


def nested_dict(keys_list):
	"""
	Returns a nested dictionary, with the final value being empty list

	make_nested_dict([[1,2,3],["a","b","c"]])
	d = {
			1:{"a":[], "b":[], "c":[]},
			2:{"a":[], "b":[], "c":[]},
			3:{"a":[], "b":[], "c":[]},
		}
	make_nested_dict([[1,2],'xy',[10,20]])

	d = {
		1:	{
			'x': { 10: [], 20: [], },
			'y': { 10: [], 20: [], },
			},
		2:	{
			'x': { 10: [], 20: [], },
			'y': { 10: [], 20: [], },
			},
		}
	"""
	if len(keys_list) == 0:
		return []
	d = {}
	for k in keys_list[0]:
		d[k] = nested_dict(keys_list[1:])
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
