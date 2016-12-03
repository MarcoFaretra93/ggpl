from pyplasm import *
import csv

def ggpl_building_house():
	"""
	ggpl_building_house is a function that generate the HPC Model represent the house structure by the input file in .lines files.
	@return house_building: HPC Model represent the structure.
	"""
	with open("muri_esterni.lines", "rb") as file:
		reader = csv.reader(file, delimiter=",")
		listExternalWalls = []
		for row in reader:
			listExternalWalls.append(POLYLINE([[float(row[0]), float(row[1])],[float(row[2]), float(row[3])]]))
	externalWalls = STRUCT(listExternalWalls)
	floor = SOLIDIFY(externalWalls)
	xfactor = 15/SIZE([1])(externalWalls)[0]
	yfactor = 15.1/SIZE([2])(externalWalls)[0]
	externalWalls = OFFSET([12,12])(externalWalls)
	externalWalls = PROD([externalWalls, Q(3/xfactor)])

	with open("muri_interni.lines", "rb") as file:
		reader = csv.reader(file, delimiter=",")
		listInternalWalls = []
		for row in reader:
			listInternalWalls.append(POLYLINE([[float(row[0]), float(row[1])],[float(row[2]), float(row[3])]]))
	internalWalls = STRUCT(listInternalWalls)
	internalWalls = OFFSET([7,7])(internalWalls)


	internalWalls = PROD([internalWalls, Q(3/xfactor)])

	with open("porte.lines", "rb") as file:
		reader = csv.reader(file, delimiter=",")
		doorsList = []
		cuboid = []
		acc = 0
		for row in reader:
			acc = acc + 1
			cuboid.append([float(row[0]),float(row[1])])
			if(acc == 4):
				doorsList.append(MKPOL([cuboid,[[1,2,3,4]],None]))
				cuboid = []
				acc = 0
	doors = STRUCT(doorsList)
	doors = PROD([doors, Q(2.5/xfactor)])

	with open("finestre.lines", "rb") as file:
		reader = csv.reader(file, delimiter=",")
		windowList = []
		cuboid = []
		acc = 0
		for row in reader:
			acc = acc + 1
			cuboid.append([float(row[0]),float(row[1])])
			if(acc == 4):
				windowList.append(MKPOL([cuboid,[[1,2,3,4]],None]))
				cuboid = []
				acc = 0
	windows = STRUCT(windowList)
	windows = PROD([windows, Q(SIZE([3])(externalWalls)[0]/2.)])
	windows = T(3)(SIZE([3])(externalWalls)[0]/4.)(windows)

	frame = STRUCT([externalWalls, internalWalls])
	frame = DIFFERENCE([frame, doors, windows])

	frame = (S([1,2,3])([xfactor,yfactor, xfactor])(frame))
	floor = (S([1,2,3])([xfactor,yfactor, xfactor])(floor))
	floor = TEXTURE("texture/parquet.jpg")(floor)
	frame = TEXTURE("texture/wall.jpg")(frame)

	return STRUCT([floor, frame])

VIEW(ggpl_building_house())