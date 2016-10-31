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

def ggpl_quarter_turn_stairs(dx, dy, dz):
	"""
	ggpl_quarter_turn_stairs is a function, that generate a Quarter Turn Stairs, this function given a dx represent the X value of the box 
	that contain the stairs, dy represent the Y value of the box, and at the end dz that represent the Z value of the box.
	Return a HPC Model.
	@param dx: Number, represent the X value of the box.
	@param dy: Number, represent the Y value of the box.
	@param dz: Number, represent the Z value of the box.
	@return quarterTurnStairs: HPC Model of the space frame.
	"""
	riser = .2
	stairsHeight = dz - (riser*2)
	firstRamp = stairsHeight/3.
	secondRamp = stairsHeight/3.
	thirdRamp = stairsHeight/3.
	stepNumberFirst = math.ceil(firstRamp / riser)
	stepNumberSecond = math.ceil(secondRamp / riser) 
	stepNumberThird = math.ceil(thirdRamp / riser)

	firstTread = dx / (stepNumberFirst + 4)

	firstPlatformX = (dx / 3.)

	stairs = generate_steps(stepNumberFirst, firstTread, riser, firstPlatformX)

	firstPlatformY = firstTread*4

	platform = CUBOID([firstPlatformY, riser, firstPlatformX])
	stairs.append(T([1,2])([firstTread*stepNumberFirst, riser*stepNumberFirst-riser])(platform))

	secondTread = (dy - firstPlatformX*2) / (stepNumberSecond-1)

	secondStair = generate_steps(stepNumberSecond, secondTread, riser, firstPlatformY)[1:]
	secondStair = R([1,3])(PI/2)(STRUCT(secondStair))
	secondStair = T([1,2,3])([dx, riser*stepNumberFirst-riser, firstPlatformX-secondTread])(secondStair)
	stairs.append(secondStair)

	stairs.append(T([1,2,3])([firstTread*stepNumberFirst, (riser*stepNumberFirst)-(riser*2)+(riser*stepNumberSecond), (firstPlatformX - secondTread + secondTread*stepNumberSecond)])(platform))

	thirdTread = dx / (stepNumberThird + 4)

	thirdStair = generate_steps(stepNumberThird+1, thirdTread, riser, firstPlatformX)[1:]
	thirdStair = R([1,3])(PI)(STRUCT(thirdStair))
	thirdStair = T([1,2,3])([thirdTread*stepNumberFirst + thirdTread, (riser*stepNumberFirst)-(riser*2)+(riser*stepNumberSecond), ((firstPlatformX*2) -secondTread + secondTread*stepNumberSecond)])(thirdStair)
	stairs.append(thirdStair)

	stairs.append(SKEL_1(BOX([1,2,3])(CUBOID([dx,dz,dy]))))

	quarterTurnStairs = MAP([S1,S3,S2])(STRUCT(stairs))

	return quarterTurnStairs

VIEW(ggpl_quarter_turn_stairs(5,5,5))