from pyplasm import *
import csv

def build_ladder(fileLadder, xfactor, ladderBuilder):
	"""
	"""
	with open(fileLadder, "rb") as file:
		reader = csv.reader(file, delimiter=",")
		ladderX = 0
		ladderY = 0
		minX = 1000000
		minY = 1000000
		for row in reader:
			if(minX > float(row[0])):
				minX = float(row[0])
			elif(minX > float(row[2])):
				minX = float(row[2])
			elif(minY > float(row[1])):
				minY = float(row[1])
			elif(minY > float(row[3])):
				minY = float(row[3])
			if(float(row[0]) == float(row[2])):
				ladderY = float(row[1]) - float(row[3])
			elif(float(row[1]) == float(row[3])):
				ladderX = float(row[0]) - float(row[2])
		if(ladderX < 0):
			ladderX = -ladderX
		elif(ladderY < 0):
			ladderY = -ladderY
		ladder = ladderBuilder.ggpl_single_stair(ladderX, ladderY, 3/xfactor)
		ladder = T([1,2])([minX, minY])(ladder)
		return ladder

def build_concrete_objects(fileOpen, offset, xfactor, type, externalWalls, windowsFunction, doorsFunction): 
	"""
	"""
	with open(fileOpen, "rb") as file:
		reader = csv.reader(file, delimiter=",")
		concreteList = []
		for row in reader:
			width = 0
			if(float(row[0]) == float(row[2])):
				width = float(row[3]) - float(row[1])
			if(float(row[1]) == float(row[3])):
				width = float(row[2]) - float(row[0])
			#add the cuboid offset.
			width = width + offset 
			if(type == "window"):
				objectConcrete = windowsFunction(width, 12., (SIZE([3])(externalWalls)[0]/2.))
			elif(type == "door"):
				objectConcrete = doorsFunction(width, 12., float(2.5/xfactor))
			if(float(row[0]) == float(row[2])):
				objectConcrete = R([1,2])(-PI/2.)(objectConcrete)
				objectConcrete = T([2])(width)(objectConcrete)
			if(type == "window"):
				objectConcrete = T([1,2,3])([float(row[0]), float(row[1]), (SIZE([3])(externalWalls)[0]/4.)])(objectConcrete)
			elif(type == "door"):
				objectConcrete = T([1,2])([float(row[0]), float(row[1])])(objectConcrete)
			concreteList.append(objectConcrete)
		return concreteList

def create_walls(fileOpen):
	"""
	"""
	with open(fileOpen, "rb") as file:
		reader = csv.reader(file, delimiter=",")
		listWalls = []
		for row in reader:
			listWalls.append(POLYLINE([[float(row[0]), float(row[1])],[float(row[2]), float(row[3])]]))
		return listWalls

def ggpl_building_house(lines, windowsFunction, doorsFunction, ladderBuilder, floorNumber, totalNumberOfFloors):
	"""
	ggpl_building_house is a function that generate the HPC Model represent the house structure by the input file in .lines files.
	@return house_building: HPC Model represent the structure.
	"""
	#create external walls 
	listExternalWalls = create_walls(lines[0])
	externalWalls = STRUCT(listExternalWalls)

	#create floor
	floor = SOLIDIFY(externalWalls)
	floor = PROD([floor, Q(1)])

	#define scale factor
	xfactor = 15/SIZE([1])(externalWalls)[0]
	yfactor = 15.1/SIZE([2])(externalWalls)[0]

	#remove the space of the ladder from second to the last floor	
	if(floorNumber != 0):
		with open(lines[4], "rb") as file:
			reader = csv.reader(file, delimiter=",")
			minX = 100000
			minY = 100000
			xValue = 0
			yValue = 0
			for row in reader:
				if(minX > float(row[0])):
					minX = float(row[0])
				elif(minX > float(row[2])):
					minX = float(row[2])
				elif(minY > float(row[1])):
					minY = float(row[1])
				elif(minY > float(row[3])):
					minY = float(row[3])
				if(float(row[0]) == float(row[2])):
					yValue = float(row[1]) - float(row[3])
				elif(float(row[1]) == float(row[3])):
					xValue = float(row[0]) - float(row[2])
				if(xValue<0):
					xValue = -xValue
				elif(yValue<0):
					yValue = -yValue
			
			diffCuboid = CUBOID([xValue, yValue, 10])
			diffCuboid = T([1,2])([minX, minY])(diffCuboid)
			floor = DIFFERENCE([floor,diffCuboid])

	#apply offset to external walls
	externalWalls = OFFSET([12,12])(externalWalls)
	externalWalls = PROD([externalWalls, Q(3/xfactor)])

	#create internal walls
	listInternalWalls = create_walls(lines[1])
	internalWalls = STRUCT(listInternalWalls)
	internalWalls = OFFSET([12,12])(internalWalls)
	internalWalls = PROD([internalWalls, Q(3/xfactor)])

	#create a cuboid to remove doors space.
	with open(lines[2], "rb") as file:
		reader = csv.reader(file, delimiter=",")
		doorsList = []
		for row in reader:
			if(float(row[1]) == float(row[3])):
				#remove a bit for asix y
				doorsList.append(POLYLINE([[float(row[0]), float(row[1])-1],[float(row[2]), float(row[3])-1]]))
			else:
				doorsList.append(POLYLINE([[float(row[0]), float(row[1])],[float(row[2]), float(row[3])]]))
	doors = STRUCT(doorsList)
	doors = OFFSET([14,14])(doors)
	doors = PROD([doors, Q(2.5/xfactor)])

	#create a cuboid to remove windows space
	with open(lines[3], "rb") as file:
		reader = csv.reader(file, delimiter=",")
		windowList = []
		for row in reader:
			if(float(row[0]) == float(row[2])):
				#remove a bit for asix X
				windowList.append(POLYLINE([[float(row[0])-1, float(row[1])],[float(row[2])-1, float(row[3])]]))
			else:
				windowList.append(POLYLINE([[float(row[0]), float(row[1])],[float(row[2]), float(row[3])]]))
	windows = STRUCT(windowList)
	windows = OFFSET([14, 14])(windows)
	windows = PROD([windows, Q(SIZE([3])(externalWalls)[0]/2.)])
	windows = T(3)(SIZE([3])(externalWalls)[0]/4.)(windows)
	frame = STRUCT([externalWalls, internalWalls])
	frame = DIFFERENCE([frame, doors, windows])

	#insert the concrete doors
	doorsConcreteList = build_concrete_objects(lines[2], 14, xfactor, "door", externalWalls, windowsFunction, doorsFunction)
	doorsConcreteList = STRUCT(doorsConcreteList)

	#insert the concrete windows
	windowsConcreteList = build_concrete_objects(lines[3], 14, xfactor, "window", externalWalls, windowsFunction, doorsFunction)
	windowsConcreteList = STRUCT(windowsConcreteList)

	#insert the ladder
	if(floorNumber != totalNumberOfFloors):
		ladder = build_ladder(lines[4], xfactor, ladderBuilder)
		frame = STRUCT([frame, windowsConcreteList, doorsConcreteList, ladder])
	else:
		frame = STRUCT([frame, windowsConcreteList, doorsConcreteList])


	frame = T([3])((3/xfactor)*floorNumber)(frame)
	floor = T([3])((3/xfactor)*floorNumber)(floor)
	frame = (S([1,2,3])([xfactor,yfactor, xfactor])(frame))
	floor = (S([1,2,3])([xfactor,yfactor, xfactor])(floor))
	floor = TEXTURE("texture/parquet.jpg")(floor)
	frame = TEXTURE("texture/wall.jpg")(frame)

	floor = STRUCT([floor, frame])
	return floor
