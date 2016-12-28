from pyplasm import *
from sympy import *
import numpy as np

def transformList2CoupledList(initList):
	"""
	transformList2CoupledList is a function that return a list containing, for every element in the initList, a couple (python tuple)
	made by the original element and its successor.
	Example : [1,2,3] -> [[1,2], [2,3], [3,1]]
	@param initList: integer list represent the initial list.
	@return coupleList: list of list of integer, represent the couple list.
	"""
	result = []
	for element in range(len(initList)-1):
		result.append([initList[element], initList[element+1]])
	result.append([initList[-1], initList[0]])
	return result

def get4CoefficientsOfThePlane(angle, line):
	"""
	get4CoefficientsOfThePlane is a function that from angle and line, return a list containing the 4 coefficients that describe 
	a plane passing through the line.
	@param angle: integer represent the angle used to rotate the planes.
	@param line: couple represent the verts of the line.
	@return planesParam: list that contain the 4 coefficients. 
	"""
	partialPlane = PROD([POLYLINE(line), QUOTE([2])])
	partialPlane = T([1,2])([-line[0][0], -line[0][1]])(partialPlane)
	partialPlane = ROTN([-angle, [line[1][0] - line[0][0], line[1][1] - line[0][1], 0]])(partialPlane)
	partialPlane = T([1,2])([+line[0][0], +line[0][1]])(partialPlane)

	#obtain 3 points 
	points = []
	points.append(UKPOL(partialPlane)[0][0])
	points.append(UKPOL(partialPlane)[0][1])
	points.append(UKPOL(partialPlane)[0][2])

	x1 = points[0][0]
	x2 = points[1][0]
	x3 = points[2][0]
	y1 = points[0][1]
	y2 = points[1][1]
	y3 = points[2][1]
	z1 = points[0][2]
	z2 = points[1][2]
	z3 = points[2][2]

	#calculate the vectors
	p1 = np.array([x1, y1, z1])
	p2 = np.array([x2, y2, z2])
	p3 = np.array([x3, y3, z3])

	v1 = p3 - p1
	v2 = p2 - p1 
	# this is a vector normal to the plane
	cp = np.cross(v1, v2)
	a, b, c = cp 

	# This evaluates a * x3 + b * y3 + c * z3 which equals d
	d = np.dot(cp, p3)

	return [a,b,c,d]


def buildRoof(verts, angle, height):
	"""
	buildRoof is a function that return a HPC Model represent the roof from the verts, angle and height.
	@param verts: list of list of integer represent the verts that define the shape of roof bottom.
	@param angle: integer represent the angle used to rotate the planes.
	@param height: integer represent the height of the roof.
	@return roof: HPC Model represent the roof.
	"""
	lines = transformList2CoupledList(verts)

	base = SOLIDIFY(POLYLINE(verts + [verts[0]]))

	planes = []

	for line in lines:
		planes.append(get4CoefficientsOfThePlane(angle, line))

	couplePlanes = transformList2CoupledList(planes)

	roofTop = []
	linesEquations = []

	# calculating equations with planes intersection
	for couple in couplePlanes:
		x, y, z = symbols('x y z')
		solved = solve([Eq(couple[0][0]*x+couple[0][1]*y+couple[0][2]*z, couple[0][3]), 
						Eq(couple[1][0]*x+couple[1][1]*y+couple[1][2]*z, couple[1][3])])
		linesEquations.append(solved)
		roofTop.append([round(float(solved[x].subs(z,roofHeight)),2), round(float(solved[y].subs(z,roofHeight)),2)])

	roofTop.append(roofTop[0])
	terrace = T([3])([roofHeight])(SOLIDIFY(POLYLINE(roofTop)))

	coupleLines = transformList2CoupledList(linesEquations)
	roofPitch = []

	#building roof pitches
	for couple in coupleLines:
		base1 = [round(float((couple[0])[x].subs(z,0)),2),round(float((couple[0])[y].subs(z,0)),2),0]
		base2 = [round(float((couple[1])[x].subs(z,0)),2),round(float((couple[1])[y].subs(z,0)),2),0]
		top1 = [round(float((couple[0])[x].subs(z,roofHeight)),2),round(float((couple[0])[y].subs(z,roofHeight)),2),roofHeight]
		top2 = [round(float((couple[1])[x].subs(z,roofHeight)),2),round(float((couple[1])[y].subs(z,roofHeight)),2),roofHeight]
		points = [base1, base2, top2, top1, base1]
		faces = [[1,2,3,4]]
		roofPitch.append(TEXTURE("textures/roof.jpg")(MKPOL([points, faces, 1])))

	roofPitch = STRUCT(roofPitch)

	return STRUCT([TEXTURE("textures/surface.jpg")(terrace), base, roofPitch])
	
#roof vertices
v1 = [0,0]
v2 = [7,0]
v3 = [7,5]
v4 = [6,5]
v5 = [7,7]
v6 = [3,8]
v7 = [0,7]

roofHeight = 1

angle = PI/3.

VIEW(buildRoof([v1,v2,v3,v4,v5,v6,v7], angle, roofHeight))

