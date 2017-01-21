from pyplasm import *
import csv
import src.workshop_08 as build_floor
import src.workshop_07 as windowsDoors
import src.workshop_03 as quarterTurnStairs
import src.workshop_09 as roof_builder

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

listExternalWalls = build_floor.create_walls('first_model_muri_esterni_1.lines')
externalWalls = STRUCT(listExternalWalls)
xfactor = 15/SIZE([1])(externalWalls)[0]
yfactor = 15.1/SIZE([2])(externalWalls)[0]
zfactor = xfactor

listExternalWalls2 = build_floor.create_walls('second_model_muri_esterni_1.lines')
externalWalls2 = STRUCT(listExternalWalls2)
xfactor2 = 15/SIZE([1])(externalWalls2)[0]
yfactor2 = 15.1/SIZE([2])(externalWalls2)[0]
zfactor2 = xfactor2

def multistorey_house(nFloors, baseString, xfactor, yfactor, zfactor):
	"""
	multistorey_house is a function that return the function that calculate the HPC Model represent the house.
	@param nFloor: represent the number of floors.
	@param baseString: String represent the prefix of the .lines files.
	@param xfactor: Float represent the factor to scale and calculate height.
	@param yfactor: Float represent the factor to scale and calculate height.
	@param zfactor: Float represent the factor to scale and calculate height.
	@return renderWindows: Function that calculate the HPC Model.
	"""
	def renderWindows(XWindow, YWindow, occurrencyWindow):
		"""
		renderWindows is a function that return the function that calculate the HPC Model represent the house.
		@param XWindow: Float list of asix X of the window cells
		@param YWindow: Float list of asix Y of the window cells
		@param occurrencyWindow: Bool matrix that represent the full cell and empty cell.
		@return renderDoors: Function that calculate the HPC Model.
		"""
		def renderDoors(XDoor, YDoor, occurencyDoor):
			"""
			renderDoors is a function that return the function that calculate the HPC Model represent the house.
			@param XDoor: Float list of asix X of the door cells.
			@param YDoor: Float list of asix Y of the door cells.
			@param occurencyDoor: Bool matrix that represent the full cells and empty cells.
			@return renderFloor: Function that calculate the HPC Model.
			"""
			def renderFloor(verts, angle, height):
				"""
				renderFloor is a function that return the HPC Model represent the house.
				@param verts: list of list of integer represent the verts that define the shape of roof bottom.
				@param angle: integer represent the angle used to rotate the planes.
				@param height: integer represent the height of the roof.
				@return house: HPC Model represent the house.
				"""
				all_floor = []
				#building roof model
				with open(verts) as file:
					reader = csv.reader(file, delimiter=",")
					new_verts = []
					for row in reader:
						new_verts.append([float(row[0]), float(row[1])])
					roofModel = roof_builder.buildRoof(new_verts, angle, height)
					roofModel = T([3])([nFloors*3/zfactor])(roofModel)
					roofModel = S([1,2,3])([xfactor*1.09, yfactor*1.09, zfactor])(roofModel)
					roofModel = T([1,2])([-SIZE([1])(roofModel)[0]*0.05, -SIZE([2])(roofModel)[0]*0.05])(roofModel)

				for i in range(nFloors):
					floor_lines = [baseString + '_muri_esterni_'+str(i+1)+'.lines', baseString + '_muri_interni_'+str(i+1)+'.lines', baseString + '_porte_'+str(i+1)+'.lines', baseString + '_finestre_'+str(i+1)+'.lines', baseString + '_scale_'+str(i)+'.lines', baseString + '_scale_'+str(i+1)+'.lines']
					floor = build_floor.ggpl_building_house(floor_lines, 
						windowsDoors.window_main(XWindow,YWindow,occurrencyWindow), 
						windowsDoors.door_main(YDoor, XDoor, occurencyDoor), 
						quarterTurnStairs, i, nFloors-1)
					all_floor.append(floor)
				
				all_floor = STRUCT(all_floor)
				return STRUCT([all_floor, roofModel])
			return renderFloor
		return renderDoors
	return renderWindows

VIEW(multistorey_house(2, 'first_model', xfactor, yfactor, zfactor)(XWindow, YWindow, occurrencyWindow)(XDoor, YDoor, occurencyDoor)('first_model_muri_esterni_1.lines', PI/5., 3/zfactor))
VIEW(multistorey_house(2, 'second_model', xfactor2, yfactor2, zfactor2)(XWindow, YWindow, occurrencyWindow)(XDoor, YDoor, occurencyDoor)('second_model_muri_esterni_1.lines', PI/5., 3/zfactor2))






