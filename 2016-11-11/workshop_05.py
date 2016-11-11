from pyplasm import *
import random
 
def draw_point_in_circle(radius, npoints):
	return [(COS(2*PI/npoints*x)*radius,SIN(2*PI/npoints*x)*radius) for x in range(0,npoints+1)]
 
def ggpl_circle_table(dx,dy,dz):
	"""
	ggpl_circle_table is a function that generate the circle_table based on formal parameters dx, dy, dz of the box.
	@param dx: represent a X coordinate of the box.
	@param dy: represent a Y coordinate of the box.
	@param dz: represent a Z coordinate of the box.
	@return circle_table: HPC Model represent the circle table
	"""
	tableThickness = .05
	chairThickness = .02
	supportThickness = .03
	chairSeat = .175
	grey = Color4f([184/255., 186/255., 186/255., 1])

	table = CYLINDER([dx/2. - chairSeat, tableThickness])(100)
	table = T([3])([dz - tableThickness])(table)
	table = COLOR(Color4f([38/255.,226/255.,189/255.,1]))(table)
	differenceTableChair = (dz - tableThickness - chairThickness - supportThickness)/2.
	traslations = (draw_point_in_circle((dx - 2*chairSeat)/2.,16))[::2]

	seat = CYLINDER([chairSeat,chairThickness])(100)
	seats = []

	chairSupport = CYLINDER([.03, differenceTableChair + supportThickness])(100)
	chairSupport = COLOR(grey)(chairSupport)
	mainSupport = CYLINDER([.15, dz - tableThickness])(100)
	mainSupport = COLOR(grey)(mainSupport)
	support = CYLINDER([supportThickness/2., dx/2. - 2*chairSeat/2.])(100)
	support = MAP([S3,S2,S1])(support)
	support = T([3])(differenceTableChair/2.)(support)
	support = COLOR(grey)(support)
	supports = [support, R([1,2])(2*PI/8.)]*8

	for i in traslations:
		temp = T([1,2,3])([i[0],i[1],differenceTableChair + supportThickness])(seat)
		seats.append(COLOR(Color4f([random.random()*255/255.,random.random()*255/255.,random.random()*255/255.,1]))(temp))
		seats.append(T([1,2])([i[0],i[1]])(chairSupport))

	box = SKEL_1(CUBOID([dx,dy,dz]))
	box = T([1,2])([-dx/2.,-dy/2.])(box)
	seats = seats + supports
	seats.append(mainSupport)
	seats.append(box)
	seats.append(table)
	return STRUCT(seats)
 
def ggpl_chair(dx,dy,dz):
	"""
	ggpl_chair is a function that generate the chair based on formal parameters dx, dy, dz of the box.
	@param dx: represent a X coordinate of the box.
	@param dy: represent a Y coordinate of the box.
	@param dz: represent a Z coordinate of the box.
	@return chair: HPC Model represent the chair.
	"""
	footRadius = .05
	seatHeight = .015
	seatBackThickness = .015
	seatBackHeight = dz/6.
	sphere = SPHERE(footRadius)([40,40])
	sphere = JOIN(SKEL_1(sphere))
	chair = []
	feet = [[0 + footRadius,0 + footRadius],[dx - footRadius,0 + footRadius], [dx - footRadius, dy - footRadius], [0 + footRadius, dy - footRadius]]
	support = CYLINDER([1.3*footRadius/2.,dy - 2*footRadius])(100)
	support = MAP([S1,S3,S2])(support)

	sideSupport = T([1,2,3])([footRadius,footRadius,dz/4. - footRadius])(support)
	sideSupports = [sideSupport, T([1])([dx - 2*footRadius])(sideSupport)]

	otherSideSupport = CYLINDER([1.3*footRadius/2.,dx - 2*footRadius])(100)
	otherSideSupport = MAP([S1,S3,S2])(otherSideSupport)
	otherSideSupport = R([1,2])(-PI/2.)(otherSideSupport)
	otherSideSupport = T([1,2,3])([footRadius,footRadius,7*dz/20.])(otherSideSupport)
	otherSideSupports = [otherSideSupport, T([2])([dy-2*footRadius])(otherSideSupport)]

	support = S(1)(.75)(support)
	support = T([1,2,3])([footRadius,footRadius,dz/2. - footRadius/2.])(support)
	supports = [support, T([1])([dx - 2*footRadius])(support)]

	seat = CUBOID([dx - 2*footRadius, dy - 2*footRadius, seatHeight])
	seat = T([1,2,3])([footRadius, footRadius, dz/2.-footRadius/2.])(seat)

	seatBack = CUBOID([dx - 2*footRadius, seatBackThickness, seatBackHeight])
	seatBack = T([1,2,3])([footRadius, footRadius, dz - 2*footRadius - seatBackHeight])(seatBack)

	for foot in feet:
		if(foot[1] != footRadius):
			solidFoot = CYLINDER([footRadius, dz/2.])(100)
			footSphere = T([1,2,3])([foot[0],foot[1],dz/2.])(sphere)
		else:
			solidFoot = CYLINDER([footRadius, dz - footRadius])(100)
			footSphere = T([1,2,3])([foot[0],foot[1],dz - footRadius])(sphere)
		solidFoot = T([1,2])([foot[0],foot[1]])(solidFoot)
		chair.append(solidFoot)
		chair.append(footSphere)

	box = SKEL_1(CUBOID([dx,dy,dz]))
	chair.append(box)
	chair.append(seat)
	chair.append(seatBack)
	chair = chair + supports + sideSupports + otherSideSupports
	chair = COLOR(Color4f([193/255., 154/255., 107/255., 1]))(STRUCT(chair))
	return chair

def ggpl_professor_desk(dx, dy, dz):
	"""
	ggpl_professor_desk is a function that generate the professor_desk based on formal parameters dx, dy, dz of the box.
	@param dx: represent a X coordinate of the box.
	@param dy: represent a Y coordinate of the box.
	@param dz: represent a Z coordinate of the box.
	@return professor_desk: HPC Model represent the professor desk.
	"""
	desk = []
	footRadius = .05
	deskThickness = .03
	border = dx/30
	knobRadius = .02
	feet = [[0 + footRadius + border,0 + footRadius + border],[dx - footRadius - border,0 + footRadius + border], [dx - footRadius - border, dy - footRadius -border], [0 + footRadius + border, dy - footRadius - border]]
	for foot in feet:
		solidFoot = CYLINDER([footRadius, dz - deskThickness])(100)
		solidFoot = T([1,2])([foot[0],foot[1]])(solidFoot)
		desk.append(solidFoot)

	deskPlane = CUBOID([dx, dy, deskThickness])
	deskPlane = T([3])(dz- deskThickness)(deskPlane)
	deskPlane = COLOR(Color4f([139/255., 232/255., 184/255., 1]))(deskPlane)
	desk.append(deskPlane)

	deskSupport = CUBOID([dx - 2*border - 2* footRadius, footRadius, 2*deskThickness])
	deskSupportFirst = T([1,2,3])([border+footRadius/2., border + footRadius/2., dz - 3*deskThickness])(deskSupport)
	deskSupports = [deskSupportFirst, T([1,2,3])([border+footRadius/2., dy-SIZE([2])(deskSupport)[0]-border-footRadius/2, dz - 3*deskThickness])(deskSupport)]

	anotherDeskSupport =  CUBOID([footRadius, dy - 2*border - 2*footRadius, 2*deskThickness])
	anotherDeskSupportFirst = T([1,2,3])([border + footRadius/2, border + footRadius/2, dz - 3*deskThickness])(anotherDeskSupport)
	anotherDeskSupports = [anotherDeskSupportFirst, T([1,2,3])([dx - SIZE([1])(anotherDeskSupport)[0]-border-footRadius/2 ,border + footRadius/2, dz - 3*deskThickness])(anotherDeskSupport)]

	drawer = CUBOID([dx/3-border-2*footRadius, dy/2., dz/10 + footRadius])
	drawer = T([1,2,3])([border + 2*footRadius, border + 2*footRadius, dz - deskThickness - 2*deskThickness - dz/10])(drawer)
	drawerWall = CUBOID([dx/3-border-2*footRadius, footRadius, dz/10])
	drawerWall = T([1,2,3])([border + 2*footRadius, 2*border, dz - deskThickness - 2*deskThickness - dz/10])(drawerWall)
	knob = SPHERE(knobRadius)([40,40])
	knob = JOIN(SKEL_1(knob))
	knob = T([1,2,3])([border + 2*footRadius + SIZE([1])(drawerWall)[0]/2, border + footRadius*.65, dz - deskThickness - 2*deskThickness - SIZE([3])(drawerWall)[0]/2])(knob)
	drawers = [drawer, drawerWall, knob, T([1])([dx - 2*border - 4*footRadius - SIZE([1])(drawer)[0]]), drawer, drawerWall, knob]

	box = SKEL_1(CUBOID([dx,dy,dz]))

	desk.append(box)
	desk = desk + deskSupports + anotherDeskSupports + drawers
	desk = COLOR(Color4f([193/255., 154/255., 107/255., 1]))(STRUCT(desk))
	return desk

def ggpl_closet(dx, dy, dz):
	"""
	ggpl_closet is a function that generate the closet based on formal parameters dx, dy, dz of the box.
	@param dx: represent a X coordinate of the box.
	@param dy: represent a Y coordinate of the box.
	@param dz: represent a Z coordinate of the box.
	@return closet: HPC Model represent the closet.
	"""
	brown = Color4f([129/255., 65/255., 13/255., 1])
	waterGreen = Color4f([139/255., 232/255., 184/255., 1])
	closet = []
	dividerWidth = dx*.05
	mainStructureWidth = dx*.95
	box = SKEL_1(CUBOID([dx,dy,dz]))

	mainStructure = CUBOID([mainStructureWidth,dy*.95, dz*.97])
	mainStructure = T([1])([dx*.025])(mainStructure)
	mainStructure = COLOR(brown)(mainStructure)

	divider = CUBOID([dividerWidth/2., dy, dz])
	divider = COLOR(brown)(divider)
	dividers = [divider, T([1])([dx*.975])(divider)]

	door = CUBOID([mainStructureWidth/2, dy*.025, dz*.9])
	door = COLOR(waterGreen)(door)
	door = T([1,2,3])([dividerWidth/2., dy*.95, dz*.06])(door)
	doors = [door, T([1])([dividerWidth/2. + SIZE([1])(door)[0] - dx*.02]), door]

	knob = SPHERE(.02)([30,30])
	knob = JOIN(SKEL_1(knob))
	knob = COLOR(brown)(knob)
	knob = T([1,2,3])([dx*.45, dy*.99, dz*.5])(knob)

	closet.append(mainStructure)
	closet.append(box)
	closet.append(knob)
	closet = closet + dividers + doors
	closet = STRUCT(closet)
	return closet

def ggpl_main():
	"""
	ggpl_main represent the main function, that contain more HPC Model and build a classroom.
	@return classroom: HPC Model represent the classroom with more HPC Model.
	"""
	firstTable = ggpl_circle_table(2,2,1)
	firstTable = STRUCT([firstTable, T([1])([3]), firstTable])

	tables = STRUCT([firstTable, T([2])([3]), firstTable])

	desk = ggpl_professor_desk(1.5,1.,1.25)

	chair = ggpl_chair(.8,.7,1.5)
	chair = T([1,2])([.3, -.5])(chair)

	closet = ggpl_closet(2,.8,2)
	closet = T([2])([-2.5])(closet)

	chairAndDesk = STRUCT([chair, desk])
	chairAndDesk = R([1,2])(PI/2)(chairAndDesk)
	chairAndDesk = T([1,2])([5.5,.5])(chairAndDesk)

	classroom = STRUCT([tables, chairAndDesk, closet])

	platform = SIZE([1,2])(classroom)
	platform[0] = platform[0] + .3*platform[0]
	platform[1] = platform[1] + .3*platform[1]
	platform = PROD([Q(platform[0]), Q(platform[1])])
	platform = T([1,2])([-SIZE([1])(platform)[0]/2. + 2., -SIZE([2])(platform)[0]/2. + .5])(platform)
	platform = COLOR(Color4f([232/255., 168/255., 134/255., 1]))(platform)

	return STRUCT([classroom, platform])

VIEW(ggpl_main())


