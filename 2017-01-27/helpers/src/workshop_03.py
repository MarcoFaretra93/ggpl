from pyplasm import *
import math

def generate_steps(stepNumber, tread, riser, stepWidth):
	"""
	generate_steps is a function that, given a stepNumber represent the number of the step, tread represent the depth of the step, 
	riser represent the height of the step and at the end stepWidth that represent the width of the step. 
	Return a list that contain the steps.
	@param stepNumber: Number of the steps
	@param tread: Number, represent depth of the step
	@param riser: Number, represent height of the single step
	@param stepWidth: Number, represent width of the all step
	@return steps: List, that contain all steps.
	"""
	step2d = MKPOL([[[tread, 0],[tread, riser*2], [tread*2, riser*2], [tread*2, riser]], [[1,2,3,4]], None])
	steps = []
	firstStep = CUBOID([tread, riser, stepWidth])
	steps.append(firstStep)

	for i in range(int(stepNumber-1)):
		steps.append(T([1,2])([(tread*i), riser*i])(PROD([step2d, Q(stepWidth)])))

	return steps

def ggpl_single_stair(dx, dy, dz):
	"""
	ggpl_quarter_turn_stairs is a function, that generate a Single Stairs, this function given a dx represent the X value of the box 
	that contain the stairs, dy represent the Y value of the box, and at the end dz that represent the Z value of the box.
	Return a HPC Model.
	@param dx: Number, represent the X value of the box.
	@param dy: Number, represent the Y value of the box.
	@param dz: Number, represent the Z value of the box.
	@return singleStairs: HPC Model of the space frame.
	"""
	riser = dz/20.
	stepNumber = 20

	if(dx > dy):
		firstTread = dx / (stepNumber)
		stepWidth = dy
	else:
		firstTread = dy / (stepNumber)
		stepWidth = dx

	stairs = generate_steps(stepNumber, firstTread, riser, stepWidth)

	singleStairs = MAP([S1,S3,S2])(STRUCT(stairs))
	singleStairs = COLOR(Color4f([193/255., 154/255., 107/255., 1]))(singleStairs)

	return singleStairs
