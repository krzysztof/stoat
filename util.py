import pickle
import os

def pickle_obj(filename, obj):
	assert isinstance(filename, str), "First argument must be a string"
	with open(filename,'w') as f:
		pickle.dump(obj, f)


def unpickle_obj(filename):
	assert isinstance(filename, str), "First argument must be a string"
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
		d[k] = make_nested_dict(keys_list[1:])
	return d


def shape_dict(data, f_idx, x_idx, m_idx):
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

