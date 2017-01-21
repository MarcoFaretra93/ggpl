from pyplasm import *

def circle(r):
	def circle0(p):
		alpha = p[0]
		return [r*COS(alpha), r*SIN(alpha)]
	return circle0


def resizeXY(X, Y, occurrency, dx, dz):
	"""
	resizeXY is a function that scale the empty space of a window base on dx and dz.
	@param X: Float list of asix X of the windows cells
	@param Y: Float list of asix Y of the windows cells
	@param occurrency: Bool matrix that represent the full cell and empty cell.
	@param dx: represent a X coordinate of the box
	@param dz: represent a Z coordinate of the box	
	"""
	sumY = sum(Y) 
	sumX = sum(X)
	visitedY = [False]*len(Y)
	for y_index in range(len(Y)):
		update = True
		for x_index in range(len(X)):
			if(occurrency[x_index][y_index] == False):
				update = False 
		if(update):
			sumY = sumY - Y[y_index]
			sumX = sumX - X[y_index]
			dx = dx - X[y_index]
			dz = dz - Y[y_index]

	for x_index in range(len(X)):
		modifyX = False
		for y_index in range(len(Y)):
			if(occurrency[x_index][y_index] == False and visitedY[y_index] == False):
				Y[y_index] = (dz * Y[y_index])/sumY
				visitedY[y_index] = True
				modifyX = True
			if(occurrency[x_index][y_index] == False and visitedY[y_index] == True and not modifyX):
				modifyX = True
		if(modifyX):
			X[x_index] = (dx * X[x_index])/sumX


def window_main(X,Y,occurrency):
	"""
	window_main is a function that generate HPC Model represent the window, parametric by dx, dy and dz.
	@param X: Float list of asix X of the window cells
	@param Y: Float list of asix Y of the window cells
	@param occurency: Bool matrix that represent the full cell and empty cell.
	@return windows_aux: function that return a HPC Model.
	"""
	def window_aux(dx,dy,dz):
		"""
		window_aux is the second level function of window_main.
		@param dx: represent the X value of the box that contain the window
		@param dy: represent the Y value of the box that contain the window
		@param dz: represent the Z value of the box that contain the window
		@return HPC Model: represent the window.
		"""
		resizeXY(X,Y,occurrency, dx, dz)
		result = []
		for x_index in range(len(X)):
			y_quotes = []
			x_sum = sum(X[:x_index])
			for y_index in range(len(Y)):
				if(occurrency[x_index][y_index] == False):
					y_quotes.append(-Y[y_index])
				else:
					y_quotes.append(Y[y_index])
			result.append(PROD([ QUOTE([-x_sum, X[x_index]]), QUOTE(y_quotes)]))
		result.append(BOX([dx,dz,dy]))
		res = STRUCT(result)
		res = PROD([res, Q(dy)])
		res = MAP([S1,S3,S2])(res)
		res = STRUCT([res])
		res = COLOR(Color4f([193/255., 154/255., 107/255., 1]))(res)
		return STRUCT([res])
	return window_aux


def door_main(XDoor,YDoor,occurrency):
	"""
	door_main is a function that generate the HPC Model represent the door, parametric by dx,dy and dz.
	@param XDoor: Float list of asix X of the door cells.
	@param YDoor: Float list of asix Y of the door cells.
	@param occurency: Bool matrix that represent the full cells and empty cells.
	@return door_aux: function that return a HPC Model.
	"""
	def door_aux(dx,dy,dz):
		"""
		door_aux is the second level function of door_main. 
		@param dx: represent the X value of the box that contain the door
		@param dy: represent the Y value of the box that contain the door
		@param dz: represent the Z value of the box that contain the door
		@return HPC Model: represent the door.
		"""
		result = []
		circle_door = MAP(circle(sum(YDoor[4:9])/2.*.6))(INTERVALS(2*PI)(50))
		circle_door = JOIN(circle_door)
		circle_door = PROD([circle_door, Q(dy/4.)])
		circle_door = MAP([S1,S3,S2])(circle_door)
		circle_door = T([1,2,3])([dx/2., dy-dy/4.+0.01, dz/2.])(circle_door)
		circle_door = COLOR(Color4f([93/255., 94/255., 107/255., 1]))(circle_door)
		for x_index in range(len(XDoor)):
			y_quotes = []
			x_sum = sum(XDoor[:x_index])
			for y_index in range(len(YDoor)):
				if(occurrency[x_index][y_index] == False):
					y_quotes.append(-YDoor[y_index])
				else:
					y_quotes.append(YDoor[y_index])
			result.append(PROD([ QUOTE([-x_sum, XDoor[x_index]]), QUOTE(y_quotes)]))
		result.append(BOX([dx,dz,dy]))
		res = STRUCT(result)
		res = PROD([res, Q(dy)])
		res = MAP([S2,S3,S1])(res)
		res = S([1,2,3])([dx/SIZE([1])(res)[0], dy/SIZE([2])(res)[0], dz/SIZE([3])(res)[0]]) (res)
		res = COLOR(Color4f([93/255., 94/255., 107/255., 1]))(res)
		glass = CUBOID([SIZE([1])(res)[0]*0.9, dy/4.*0.9, SIZE([3])(res)[0]*0.9])
		glass = T([1,2,3])([dx*0.05, dy/8. + dy*0.05, dz*0.05])(glass)
		glass = COLOR(Color4f([38/255.,226/255.,189/255.,1]))(glass)
		return STRUCT([res, circle_door, glass])
	return door_aux






