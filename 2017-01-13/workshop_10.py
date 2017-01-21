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

listExternalWalls = build_floor.create_walls('muri_esterni_1.lines')
externalWalls = STRUCT(listExternalWalls)
xfactor = 15/SIZE([1])(externalWalls)[0]
yfactor = 15.1/SIZE([2])(externalWalls)[0]
zfactor = xfactor

def multistorey_house(nFloors):

	def renderWindows(XWindow, YWindow, occurrencyWindow):

		def renderDoors(XDoor, YDoor, occurencyDoor):
			"""
			"""
			def renderFloor(verts, angle, height):
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
					floor_lines = ['muri_esterni_'+str(i+1)+'.lines', 'muri_interni_'+str(i+1)+'.lines', 'porte_'+str(i+1)+'.lines', 'finestre_'+str(i+1)+'.lines', 'scale_'+str(i+1)+'.lines']
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

VIEW(multistorey_house(2)(XWindow, YWindow, occurrencyWindow)(XDoor, YDoor, occurencyDoor)('muri_esterni_1.lines', PI/5., 3/zfactor))