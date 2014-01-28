"""
Thanks Josh Hemann for the example
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


def single_boxplot(shaped_dict, v1_sorter=None, v2_sorter=None, tick_format="{v1}/{v2}", title="Title", x_label="X", y_label="Y"):
	import inspect

	# Identity mapping
	sorters = [v1_sorter, v2_sorter]
	for idx, sorter in enumerate(sorters):
		if sorter is None:
			sorters[idx] = lambda k:k
		# Explicing sorting function
		elif inspect.isfunction(sorter):
			pass
		else:
			def make_comp(order):
				def comp(x, y):
					for v in (x,y):
						if v not in order:
							raise Exception, "Reference ordering %s does not contain %s" % (ordering, v)
					return order.index(x) - order.index(y)
			sorters[idx]=lambda l: sorted(l,key=lambda i:i[0], cmp=make_comp(list(sorter)))
	v1_sorter, v2_sorter = sorters

	fig = plt.figure(figsize=(18,8))
	ax = fig.add_subplot(111)
	ax.set_title(title)
	ax.set_xlabel(x_label)
	ax.set_ylabel(y_label)
	xticks = []
	box_data = []
	for k, v in v1_sorter(shaped_dict.items()):
		for kk, vv in v2_sorter(v.items()):
			box_data.append(vv)
			xticks.append((k,kk))
	plt.boxplot(box_data)
	ax.set_xticklabels([tick_format.format(v1=t,v2=tt) for t, tt in xticks])

def multi_boxplot(shaped_dict, v1_sorter=None, v2_sorter=None, tick_format="{v1}/{v2}", x_label="X", y_label="Y", plots_prefix="plot"):
	for k,v in shaped_dict.iteritems():
		single_boxplot(v, v1_sorter=v1_sorter, v2_sorter=v2_sorter, tick_format=tick_format, x_label=x_label, y_label=y_label, title=str(k))
		plt.savefig("%s_%s"%(plots_prefix, k));

# Generate some data from five different probability distributions,
# each with different characteristics. We want to play with how an IID
# bootstrap resample of the data preserves the distributional
# properties of the original sample, and a boxplot is one visual tool
# to make this assessment
def make_boxplot(data, experiments, boxColors, methods, title, top=10.0):

	numLabels = len(experiments)

	fig = plt.figure(figsize=(10,6))
	fig.canvas.set_window_title('A Boxplot Example')
	ax1 = fig.add_subplot(111)
	plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
	
	bp = plt.boxplot(data, notch=0, sym='+', vert=1, whis=1.5)
	plt.setp(bp['boxes'], color='black')
	plt.setp(bp['whiskers'], color='black')
	plt.setp(bp['fliers'], color='red', marker='+')
	
	# Add a horizontal grid to the plot, but make it very light in color
	# so we can use it for reading data values but not be distracting
	ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
	
	# Hide these grid behind plot objects
	ax1.set_axisbelow(True)
	ax1.set_title(title)
	ax1.set_xlabel('Datasets')
	ax1.set_ylabel('Distance')
	
	# Now fill the boxes with desired colors
	#boxColors = ['darkkhaki','royalblue']
	numBoxes = numLabels*len(methods)
	medians = range(numBoxes)
	averages = range(numBoxes)
	for i in range(numBoxes):
	  box = bp['boxes'][i]
	  boxX = []
	  boxY = []
	  for j in range(len(experiments)):
	      boxX.append(box.get_xdata()[j])
	      boxY.append(box.get_ydata()[j])
	  boxCoords = zip(boxX,boxY)
	  # Alternate between Dark Khaki and Royal Blue
	  k = i % len(methods)
	  boxPolygon = Polygon(boxCoords, facecolor=boxColors[k])
	  ax1.add_patch(boxPolygon)
	  # Now draw the median lines back over what we just filled in
	  med = bp['medians'][i]
	  # print med.get_ydata()
	  medianX = []
	  medianY = []
	  for j in range(2):
	      medianX.append(med.get_xdata()[j])
	      medianY.append(med.get_ydata()[j])
	      plt.plot(medianX, medianY, 'k')
	      medians[i] = medianY[0]
		  
	  # Finally, overplot the sample averages, with horizontal alignment
	  # in the center of each box
	  plt.plot([np.average(med.get_xdata())], [np.average(data[i])], color='w', marker='o', markeredgecolor='k')
	  averages[i] = np.average(data[i])
	#print averages ,len(averages)
	#print medians, len(medians)
	
	# Set the axes ranges and axes labels
	ax1.set_xlim(0.5, numBoxes+0.5)
	#top = min(max([max(d) for d in data]), 10) + 0.3
	top = max([max(d) for d in data])
	#top = 50.0
	#top = 10.0
	#top = top
	bottom = 0
	ax1.set_ylim(bottom, top)
	xtickNames = plt.setp(ax1, xticklabels=np.repeat(experiments, len(methods)))
	plt.setp(xtickNames, rotation=45, fontsize=8)
	
	# Due to the Y-axis scale being different across samples, it can be
	# hard to compare differences in medians across the samples. Add upper
	# X-axis tick labels with the sample medians to aid in comparison
	# (just use two decimal places of precision)
	pos = np.arange(numBoxes)+1
	#upperLabels = [str(np.round(s, 3)) for s in medians]
	#upperLabels_avg = [str(np.round(s, 3)) for s in averages]
	#floatformat = lambda x: '{:.4e}'.format(x)
	floatformat = lambda x: str(np.round(x, 5))
	upperLabels = [floatformat(s) for s in medians]
	upperLabels_avg = [floatformat(s) for s in averages]

	#weights = ['roman']*len(methods)
	weights = []
	weights_averages = []
			
	for i in range(len(experiments)):
		min_median = min(medians[i*len(methods):(i+1)*len(methods)])
		min_average = min(averages[i*len(methods):(i+1)*len(methods)])
		for j in range(len(methods)):
			if medians[i*len(methods) + j] == min_median:
				weights.append('bold')
			else:
				weights.append('roman')
			if averages[i*len(methods) + j] == min_average:
				weights_averages.append('bold')
			else:
				weights_averages.append('roman')

	#weights = ['bold', 'semibold'] * len(methods)

	ax1.text(0.005, top-(top*0.05), "   Mean:", horizontalalignment='center', size='x-small', weight='roman', color='black')
	ax1.text(0.005, top-(top*0.10), "Average:", horizontalalignment='center', size='x-small', weight='roman', color='black')
	wi = 0
	for tick,label in zip(range(numBoxes),ax1.get_xticklabels()):
	   k = tick % len(methods)
	   ax1.text(pos[tick], top-(top*0.05), upperLabels[tick], horizontalalignment='center', size='x-small', weight=weights[wi], color=boxColors[k])
	   #if weights[wi] == 'bold':
	   #   ax1.text(pos[tick], top-(top*0.07), "*", horizontalalignment='center', size='x-small', weight=weights_averages[wi], color=boxColors[k])
	   ax1.text(pos[tick], top-(top*0.10), upperLabels_avg[tick], horizontalalignment='center', size='x-small', weight=weights_averages[wi], color=boxColors[k])
	   #if weights_averages[wi] == 'bold':
	   #   ax1.text(pos[tick], top-(top*0.12), "*", horizontalalignment='center', size='x-small', weight=weights_averages[wi], color=boxColors[k])
	   wi += 1
	   #k += 1

	
	# Finally, add a basic legend
	legend_Y = 0.07
	legend_X = 0.6
	for i in range(len(methods)):
		#plt.figtext(legend_X, legend_Y - i*0.035, methods[i], backgroundcolor=boxColors[i], color='black', weight='roman', size='x-small')
		plt.figtext(legend_X + i*0.06, legend_Y, methods[i], backgroundcolor=boxColors[i], color='black', weight='roman', size='x-small')

	plt.figtext(legend_X, legend_Y - 0.005 - 0.034*(len(methods)), 'o', color='black', backgroundcolor='white', weight='roman', size='medium')
	plt.figtext(legend_X+0.015, legend_Y - 0.035*(len(methods)), ' Average Value', color='black', weight='roman', size='x-small')

	return plt

	
if __name__ == "__main__":
	from random import random
	experiments = ["Test%d"%(i) for i in range(4)]
	methods = ["Method A", "Method B", "Method C"]
	data = [[0.1*random(), 0.3*random(), 0.5*random()] for i in range(len(experiments)*len(methods))]
	boxColors = ["red", "green", "royalblue", "darkkhaki"]
	plt = make_boxplot(data, experiments, boxColors, methods, 'Boxplot', top=1.0)	
	plt.show()
