from pyplasm import *
import numpy

verts = [[0,0,0], [0,3,0], [6,3,0], [6,9,0], [9,9,0],[9,0,0],[1.5,1.5,2],[7.5,1.5,2],[7.5,7.5,2]]
cells = [[1,7,2], [2,7,8,3], [3,8,9,4], [4,9,5], [8,6,5,9], [1,6,8,7], [1,6,3,2], [3,6,5,4]]

#verts = [[0,0,0], [0,9,0],[9,0,0],[9,3,0],[3,3,0],[3,6,0],[9,6,0],[9,9,0],[7.5,1.5,2],[1.5,1.5,2],[1.5,7.5,2],[7.5,7.5,2]]
#cells = [[3,4,9],[3,9,10,1],[1,10,11,2],[10,5,6,11],[4,9,10,5],[2,8,12,11],[6,11,12,7],[7,8,12],[1,5,4,3],[2,8,7,6]]

def normalize_value_in_list(list):
	"""
	normalize_value_in_list is a function that rounds float in list.
	Return a normalized list.
	@param list: Float's list
	@return list: Float's list, that contains the rounds float.
	"""
	for j in range(len(list)):
		for i in range(len(list[j])):
			if(abs(list[j][i]) < 0.001):
				list[j][i] = 0
			else:
				list[j][i] = round(list[j][i], 1)
	return list

def makeDictOfPoints(listUkpol):
	"""
	makeDict is a function that create a Python's dictionary, which contain verts as key, and point's lists, that incident verts, as value.
	Return a dictionary.
	@param listUkpol: List that contain verts list and cells list.
	@return dictionary: Dictionary that contain verts as key and point's list as value
	"""
	dictionary = {}
	verts = listUkpol[0]
	cells = listUkpol[1]
	for cell in cells: 
		for label in cell:
			point = str(normalize_value_in_list(verts)[int(label)-1])
			if(point not in dictionary):
				dictionary[point] = []
			dictionary[point].append(label)
	return dictionary

def verifyPlanary(verts, cells):
	"""
	verifyPlanary is a function that verify the planary of roof faces.
	Return True or False, depending on all faces is planary or not.
	@param verts: List that contain all verts.
	@param cells: List that contain all cells.
	@return bool: Boolean
	"""
	verts = normalize_value_in_list(verts)
	for cell in cells:
		if(len(cell) > 3):
			m = []
			lastPoint = cell[-1]
			for label in cell:
				point = verts[int(label)-1]
				row = [] 
				for i in range(len(point)):
					row.append(point[i]-verts[lastPoint-1][i])
				m.append(row)
				A = numpy.matrix(m)
				if(numpy.linalg.matrix_rank(A) > 2):
					return False
	return True

def ggpl_cross_hipped(verts, cells):
	"""
	ggpl_cross_hipped is a main function that return a roof HPC.
	@param verts: List that contain all verts.
	@param cells: List that contain all cells.
	@return HPC: HPC model represent the Roof or String Error.
	"""
	roof_skeleton = MKPOL([verts, cells, None])
	beams = OFFSET([.1,.1,.1])(SKEL_1(roof_skeleton))
	roof = MKPOL([verts, cells[:-2], None])
	ukpol = UKPOL(SKEL_2(roof))
	roof = OFFSET([.1,.1,.1])(roof)
	roof = T([3])([.1])(roof)
	beams = COLOR(GREEN)(beams)
	if(verifyPlanary(ukpol[0], ukpol[1])):
		return STRUCT([roof, beams])
	else: 
		print('The planary is not satisfied')


VIEW(ggpl_cross_hipped(verts, cells))
