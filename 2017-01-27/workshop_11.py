from pyplasm import *
import csv
import helpers.workshop_10 as houseBuilder
import helpers.src.workshop_08 as build_floor

XWindow = [2,3,2,3,2]
YWindow = [2,3,2,3,2]
occurrencyWindow = [[True, True, True, True, True],
			  [True, False, True, False, True],
			  [True, True, True, True, True],
			  [True, False, True, False, True],
			  [True, True, True, True, True]]

XDoor = [.2, .2, .05, .2, .05, .2, .3, .2, .05, .2 ,.05, .2, .2]
YDoor = [.2, .2, .05, .2, .05, 1, .05, .2, .05, .2, .2]
occurencyDoor = [[True, True, True, True, True, True, True, True, True, True, True, True, True],
				[True, False, False, False, False, False, True, False, False, False, False, False, True],
				[True, False, True, True, True, True, True, True, True, True, True, False, True], 
				[True, False, True, False, False, False, True, False, False, False, True, False, True],
				[True, False, True, False, True, True, True, True, True, False, True, False, True],
				[True, False, True, False, True, False, True, False, True, False, True, False, True], 
				[True, False, True, False, True, True, True, True, True, False, True, False, True],
				[True, False, True, False, False, False, True, False, False, False, True, False, True],
				[True, False, True, True, True, True, True, True, True, True, True, False, True],
				[True, False, False, False, False, False, True, False, False, False, False, False, True],
				[True, True, True, True, True, True, True, True, True, True, True, True, True]]

listExternalWalls = build_floor.create_walls('helpers/first_model_muri_esterni_1.lines')
externalWalls = STRUCT(listExternalWalls)
xfactor = 15/SIZE([1])(externalWalls)[0]
yfactor = 15.1/SIZE([2])(externalWalls)[0]
zfactor = xfactor

listExternalWalls2 = build_floor.create_walls('helpers/second_model_muri_esterni_1.lines')
externalWalls2 = STRUCT(listExternalWalls2)
xfactor2 = 15/SIZE([1])(externalWalls2)[0]
yfactor2 = 15.1/SIZE([2])(externalWalls2)[0]
zfactor2 = xfactor2

def create_enclosure(dx, dy, dz):
	"""
	create_enclosure is a function that return a HPC Model represent the enclosure with dx (width), dy (depth), dz (height)
	@param dx: Integer represent the width of the enclosure.
	@param dy: Integer represent the depth of the enclosure.
	@param dz: Integer represent the height of the enclosure.
	@return enclosure: HPC Model represent the enclosure. 
	"""
	enclosure = []
	cont = dx
	while(cont > 0):
		tile = CUBOID([.5, dy, dz])
		tile = T([1])(dx - cont)(tile)
		enclosure.append(tile)
		cont = cont - 1
	bigTileUp = CUBOID([dx, dy/2, dz*.1])
	bigTileUp = T([3])(dz*.7)(bigTileUp)
	bigTileDown = CUBOID([dx, dy/2, dz*.2])
	bigTileDown = T([3])(dz*.2)(bigTileDown)
	enclosure.append(bigTileDown)
	enclosure.append(bigTileUp)
	return STRUCT(enclosure)

def create_and_position_house(rotate, model, transX, transY):
	"""
	create_and_position_house is a function that create and translate the house by rotate, type of model, trans for asix x and trans for asix y.
	@param rotate: angle for rotation of the house.
	@param model: String represent the type of the model.
	@param transX: Float, represent the translation for asix x
	@param transY: Float, represent the translation for asix y
	@return house: HPC Model in the correct position.
	"""
	house = R([1,2])(rotate)(model)
	if rotate == PI:
		house = T([1,2])([SIZE([1])(house)[0], SIZE([2])(house)[0]])(house)
	elif rotate == PI/2:
		house = T([1])(SIZE([1])(house)[0])(house)
	elif rotate == PI/4:
		house = T([1])(SIZE([1])(house)[0]/2)(house)
	elif rotate == -PI/2:
		house = T([2])(SIZE([2])(house)[0])(house)
	house = T([1,2])([transX,transY])(house)
	return house

def suburban_neighborhood():
	"""
	suburban_neighborhood is a function that return a HPC Model represent the complete suburban_neighborhood.
	@return model: HPC Model represent the complete suburban_neighborhood.
	"""
	houses = []
	alleyways = []
	enclosures = []
	#create the models of the house (workshop_10), scale for dimension 10X9.
	firstHouseModel = houseBuilder.multistorey_house(2, 'helpers/first_model', xfactor, yfactor, zfactor)(XWindow, YWindow, occurrencyWindow)(XDoor, YDoor, occurencyDoor)('helpers/first_model_muri_esterni_1.lines', PI/5., 3/zfactor)
	firstHouseModel = S([1,2])([10/SIZE([1])(firstHouseModel)[0], 10/SIZE([2])(firstHouseModel)[0]])(firstHouseModel)

	secondHouseModel = houseBuilder.multistorey_house(2, 'helpers/second_model', xfactor2, yfactor2, zfactor2)(XWindow, YWindow, occurrencyWindow)(XDoor, YDoor, occurencyDoor)('helpers/second_model_muri_esterni_1.lines', PI/5., 3/zfactor2)
	secondHouseModel = S([1,2])([10/SIZE([1])(secondHouseModel)[0], 10/SIZE([2])(secondHouseModel)[0]])(secondHouseModel)

	#create the istances of model houses
	houses.append(create_and_position_house(PI/2, firstHouseModel, 3, 5))
	houses.append(create_and_position_house(PI, secondHouseModel, 3, 25))
	houses.append(create_and_position_house(PI, secondHouseModel, 3, 45))
	houses.append(create_and_position_house(PI/4, firstHouseModel, 3,70))
	houses.append(create_and_position_house(0, firstHouseModel, 23, 5))
	houses.append(create_and_position_house(PI/2, secondHouseModel, 23, 25))
	houses.append(create_and_position_house(PI/2, secondHouseModel, 23, 45))
	houses.append(create_and_position_house(PI/2, secondHouseModel, 41, 5))
	houses.append(create_and_position_house(0, firstHouseModel, 41, 25))
	houses.append(create_and_position_house(0, firstHouseModel, 41, 45))
	houses.append(create_and_position_house(0, secondHouseModel, 61, 5))
	houses.append(create_and_position_house(-PI/2, firstHouseModel, 61, 25))
	houses.append(create_and_position_house(-PI/2, firstHouseModel, 61, 45))
	angularHouse = create_and_position_house(PI/4, secondHouseModel, 61, 70)
	angularHouse = T([1])(-SIZE([1])(angularHouse)[0]/2)(angularHouse)
	houses.append(angularHouse)

	#create alleyways left
	alleyway = CUBOID([7, 1, .1])
	alleyway = T([1,2])([13-5, 6.7])(alleyway)
	alleyways.append(alleyway)

	alleyway = CUBOID([3, 1, .1])
	alleyway = T([1,2])([12, 35-3.3])(alleyway)
	alleyways.append(alleyway)

	alleyway = CUBOID([3, 1, .1])
	alleyway = T([1,2])([12, 55-3.3])(alleyway)
	alleyways.append(alleyway)

	alleyway = CUBOID([10, 1, .1])
	alleyway = R([1,2])(-PI/4)(alleyway)
	alleyway = T([1,2])([8, 74.5])(alleyway)
	alleyways.append(alleyway)

	#create alleyways right
	alleyway = CUBOID([4, 1, .1])
	alleyway = T([1,2])([58, 7.3])(alleyway)
	alleyways.append(alleyway)

	alleyway = CUBOID([8, 1, .1])
	alleyway = T([1,2])([58, 32.3])(alleyway)
	alleyways.append(alleyway)

	alleyway = CUBOID([8, 1, .1])
	alleyway = T([1,2])([58, 52.3])(alleyway)
	alleyways.append(alleyway)

	alleyway = CUBOID([4.5, 1, .1])
	alleyway = R([1,2])(PI/4)(alleyway)
	alleyway = T([1,2])([57, 69])(alleyway)
	alleyways.append(alleyway)

	#create central alleyways with BEZIER pyplasm function
	alleyway = MAP(BEZIERCURVE([[20, 3], [24.5, 3], [24.5, 9]]))(INTERVALS(1)(32))
	alleyway = OFFSET([1,1])(alleyway)
	alleyway = PROD([alleyway, Q(.1)])
	alleyways.append(alleyway)

	alleyway = MAP(BEZIERCURVE([[20, 22], [30, 22], [30, 25]]))(INTERVALS(1)(32))
	alleyway = OFFSET([1,1])(alleyway)
	alleyway = PROD([alleyway, Q(.1)])
	alleyways.append(alleyway)

	alleyway = MAP(BEZIERCURVE([[20, 42], [30, 42], [30, 45]]))(INTERVALS(1)(32))
	alleyway = OFFSET([1,1])(alleyway)
	alleyway = PROD([alleyway, Q(.1)])
	alleyways.append(alleyway)	

	alleyway = MAP(BEZIERCURVE([[47.8, 5], [47.8, 3], [53, 3]]))(INTERVALS(1)(32))
	alleyway = OFFSET([1,1])(alleyway)
	alleyway = PROD([alleyway, Q(.1)])
	alleyways.append(alleyway)

	alleyway = MAP(BEZIERCURVE([[43, 29], [42, 19], [53, 20]]))(INTERVALS(1)(32))
	alleyway = OFFSET([1,1])(alleyway)
	alleyway = PROD([alleyway, Q(.1)])
	alleyways.append(alleyway)

	alleyway = MAP(BEZIERCURVE([[43, 49], [42, 39], [53, 40]]))(INTERVALS(1)(32))
	alleyway = OFFSET([1,1])(alleyway)
	alleyway = PROD([alleyway, Q(.1)])
	alleyways.append(alleyway)

	#base of the model
	base = CUBOID([73, 85, -5]);
	base = MATERIAL([.05,.05,.05,1,  .4,.2,0,1,  0,0,0,0, 0,0,0,1, 100])(base)

	#create a grass of model 
	xValue = QUOTE([73])
	yValue = QUOTE([85])
	grass = PROD([xValue, yValue])
	grass = TEXTURE("texture/texture_erba.jpg")(grass)

	# first straight street
	straightStreet = CUBOID([5, 60, .5])
	straightStreet = T([1])([15])(straightStreet)

	#second straight street
	straightStreet2 = CUBOID([3, 85, .5])
	straightStreet2 = T([1])([35])(straightStreet2)

	#third straight street
	straightStreet3 = CUBOID([5, 60, .5])
	straightStreet3 = T([1])([53])(straightStreet3)

	#fourth straight street
	straightStreet4 = CUBOID([23, 5, .5])
	straightStreet4 = T([1,2])([25,70])(straightStreet4)

	#first curve street
	curveStreet = MAP(BEZIERCURVE([[15, 60], [15, 70], [25, 70]]))(INTERVALS(1)(32))
	curveStreet = OFFSET([5,5])(curveStreet)
	curveStreet = PROD([curveStreet, Q(.5)])

	#second curve street
	curveStreet2 = MAP(BEZIERCURVE([[48, 70], [58, 70], [58, 60]]))(INTERVALS(1)(32))
	curveStreet2 = OFFSET([-5,5])(curveStreet2)
	curveStreet2 = PROD([curveStreet2, Q(.5)])

	#create enclosure
	enclosure = create_enclosure(85, .1, 1.5)
	enclosure = R([1,2])(PI/2)(enclosure)
	enclosures.append(enclosure)

	enclosure = create_enclosure(85, .1, 1.5)
	enclosure = R([1,2])(PI/2)(enclosure)
	enclosure = T([1])(73)(enclosure)
	enclosures.append(enclosure)

	enclosure = create_enclosure(15, .1, 1.5)
	enclosures.append(enclosure)

	enclosure = create_enclosure(35, .1, 1.5)
	enclosure = T([2])(85)(enclosure)
	enclosures.append(enclosure)

	enclosure = create_enclosure(15, .1, 1.5)
	enclosure = T([1])(20)(enclosure)
	enclosures.append(enclosure)

	enclosure = create_enclosure(15, .1, 1.5)
	enclosure = T([1])(38)(enclosure)
	enclosures.append(enclosure)

	enclosure = create_enclosure(35, .1, 1.5)
	enclosure = T([1,2])([38, 85])(enclosure)
	enclosures.append(enclosure)

	enclosure = create_enclosure(15, .1, 1.5)
	enclosure = T([1])(58)(enclosure)
	enclosures.append(enclosure)

	enclosure = create_enclosure(15, .1, 1.5)
	enclosure = T([2])(20)(enclosure)
	enclosures.append(enclosure)

	enclosure = create_enclosure(15, .1, 1.5)
	enclosure = T([2])(40)(enclosure)
	enclosures.append(enclosure)

	enclosure = create_enclosure(15, .1, 1.5)
	enclosure = T([2])(60)(enclosure)
	enclosures.append(enclosure)

	enclosure = create_enclosure(15, .1, 1.5)
	enclosure = T([1,2])([20, 20])(enclosure)
	enclosures.append(enclosure)

	enclosure = create_enclosure(15, .1, 1.5)
	enclosure = T([1,2])([20, 40])(enclosure)
	enclosures.append(enclosure)

	enclosure = create_enclosure(15, .1, 1.5)
	enclosure = T([1,2])([20, 60])(enclosure)
	enclosures.append(enclosure)

	enclosure = create_enclosure(15, .1, 1.5)
	enclosure = T([1,2])([38, 20])(enclosure)
	enclosures.append(enclosure)

	enclosure = create_enclosure(15, .1, 1.5)
	enclosure = T([1,2])([38, 40])(enclosure)
	enclosures.append(enclosure)

	enclosure = create_enclosure(15, .1, 1.5)
	enclosure = T([1,2])([38, 60])(enclosure)
	enclosures.append(enclosure)

	enclosure = create_enclosure(15, .1, 1.5)
	enclosure = T([1,2])([58, 20])(enclosure)
	enclosures.append(enclosure)

	enclosure = create_enclosure(15, .1, 1.5)
	enclosure = T([1,2])([58, 40])(enclosure)
	enclosures.append(enclosure)

	enclosure = create_enclosure(15, .1, 1.5)
	enclosure = T([1,2])([58, 60])(enclosure)
	enclosures.append(enclosure)

	streets = STRUCT([straightStreet, straightStreet2, straightStreet3, straightStreet4,curveStreet, curveStreet2])
	streets = TEXTURE("texture/texture_asfalto.jpg")(streets)

	enclosures = STRUCT(enclosures)
	enclosures = MATERIAL([.05,.05,.05,1,  .4,.2,0,1,  0,0,0,0, 0,0,0,1, 100])(enclosures)
	houses = STRUCT(houses)
	alleyways = STRUCT(alleyways)
	alleyways = MATERIAL([.05,.05,.05,1,  .25,.25,.25,1,  0,0,0,0, 0,0,0,1, 100])(alleyways)

	return STRUCT([houses, base, grass, streets, alleyways, enclosures])

VIEW(suburban_neighborhood())