#!/usr/bin/env python
import h5py
import numpy as np
import argparse

import matplotlib
matplotlib.rcParams["backend"] = "TkAgg"
import matplotlib.pyplot as plt

# TODO: add slice support
#		investigate horizontal sources

default_eps_parameters = {
		'interpolation':'spline36',
		'cmap':'binary',
		'alpha':1.0,
		'aspect':'equal'
	}
	
default_source_parameters = {
        'color':'r',
        'edgecolor':'r',
        'facecolor':'none',
        'hatch':'/',
        'linewidth':2
    }

default_monitor_parameters = {
        'color':'b',
        'edgecolor':'b',
        'facecolor':'none',
        'hatch':'/',
        'linewidth':2
    }

default_boundary_parameters = {
        'color':'g',
        'edgecolor':'g',
        'facecolor':'none',
        'hatch':'/'
    }

def load_struc(fname):
	f = h5py.File(fname, 'r')
	eps = np.array(f[list(f.keys())[0]])
	f.close()
	eshape = np.array(eps.shape)
	
	return(eps, eshape)
	
def parseV3(line):
	lbuf = line.translate({ord(i): None for i in '#()\r\n'})
	lbuf = lbuf.replace(';', ' ')
	lbuf = lbuf.split()
	numbuf = []
	for x in lbuf:
		numbuf.append(float(x))
	return numbuf
	
def parseRawNum(line):
	lbuf = line.translate({ord(i): ' ' for i in ';\r\n'})
	lbuf = lbuf.split()
	numbuf = []
	for x in lbuf:
		numbuf.append(float(x))
	if len(numbuf) == 1:
		numbuf = numbuf[0]
	return numbuf
	
def parseStruc(pname):
	with open(pname, 'r') as f:
		lns = f.readlines()
		for n in range(0, len(lns), 2):
			if lns[n][0] == 'g':
				geolattice = parseV3(lns[n+1])
			if lns[n][0] == 'p':
				boundaries = parseRawNum(lns[n+1])
			if lns[n][0] == 'r':
				res = parseRawNum(lns[n+1])
			if lns[n][0] == 's':
				sources = parseV3(lns[n+1])
			if lns[n][0] == 'f':
				fluxes = parseV3(lns[n+1])
	return(geolattice,boundaries,res,sources,fluxes)
	
def plotLineObjects(ax, obj, params):
	for n in range(0, len(obj), 6):
		
		ax.bar(obj[n],obj[n+4],obj[n+3], -obj[n+4]/2+obj[n+1], **params)
		
def plotBoundaries(ax, obj, params, eshape):
	for n in range(0, len(obj), 2):
		if int(obj[n]) == 0:
			ax.bar([-eshape[0]/(2*res)+obj[n+1]/2, eshape[0]/(2*res)-obj[n+1]/2],eshape[1]/res,obj[n+1],-eshape[1]/(2*res), **params)
		if int(obj[n]) == 1:
			ax.bar(0,obj[n+1],eshape[0]/res,eshape[1]/(2*res)-obj[n+1], **params)
			ax.bar(0,obj[n+1],eshape[0]/res,-eshape[1]/(2*res), **params)
		if int(obj[n]) == -1:
			ax.bar([-eshape[0]/(2*res)+obj[n+1]/2, eshape[0]/(2*res)-obj[n+1]/2],eshape[1]/res,obj[n+1],-eshape[1]/(2*res), **params)
			ax.bar(0,obj[n+1],eshape[0]/res,eshape[1]/(2*res)-obj[n+1], **params)
			ax.bar(0,obj[n+1],eshape[0]/res,-eshape[1]/(2*res), **params)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Plot structure.')
	parser.add_argument('--fname',
						help='Input epsilon h5 filename')
	parser.add_argument('--pname',
						help='Input structure detail filename')
	args = parser.parse_args()
	
	(eps, eshape) = load_struc(args.fname)
	res = 10
	print(eps.shape)
	(geolattice,boundaries,res,sources,fluxes) = parseStruc(args.pname)
	
	fig = plt.figure(dpi=150)
	ax = plt.gca()
	ax.imshow(eps[:,:,int(eps.shape[2]/2)].T, **default_eps_parameters, extent=[-eshape[0]/(2*res),eshape[0]/(2*res),
														-eshape[1]/(2*res),eshape[1]/(2*res)])
	
	sdata = np.zeros([eshape[0], eshape[1]])
	sdata[int(sources[0]*res+eshape[0]/2)][(int(eshape[1]/2-sources[4]*res/2)):(int(eshape[1]/2+sources[4]*res/2))] = 1
	#ax.plot(sdata, **default_source_parameters, extent=[-eshape[0]/(2*res),eshape[0]/(2*res),
														#-eshape[1]/(2*res),eshape[1]/(2*res)])

	plotLineObjects(ax, sources, default_source_parameters)
	plotLineObjects(ax, fluxes, default_monitor_parameters)
	plotBoundaries(ax, boundaries, default_boundary_parameters, eshape)
	
	plt.savefig('sim_domain.png')