from pyplasm import *

def building_structure(distancesPillar, interstoryHeights, pX, pY, bY, sequence):
	""" Choose the function from sequence parameter, continuous beams or continuous pillar """
	if(sequence == "beams"):
		VIEW(building_structure_continuous_beams(distancesPillar, interstoryHeights, pX, pY, bY))
	elif(sequence == "pillar"):
		VIEW(building_structure_continuous_pillar(distancesPillar, interstoryHeights, pX, pY, bY))
	else:
		print("Wrong input")

def building_structure_continuous_beams(distancesPillar, interstoryHeights, pX, pY, bY):
	""" building structure by continuous beams """

	pillarXValue = []
	interstoryValue = []
	beamsZValue = []
	bX = 0


	for element in distancesPillar:
		bX = bX + abs(element) + pX
		pillarXValue.append(pX)
		pillarXValue.append(element)
	bX = bX + pX

	for element in interstoryHeights:
		beamsZValue.append(-element)
		beamsZValue.append(bY)
		interstoryValue.append(element)
		interstoryValue.append(-bY)


	pillarXValue.append(pX)

	pillarX = QUOTE(pillarXValue)
	pillarY = QUOTE([pY])
	pillarXY = PROD([pillarX, pillarY])

	pillar = PROD([pillarXY, QUOTE(interstoryValue)])

	beamsX = QUOTE([bX])
	beamsY = QUOTE([bY])
	beamsXY = PROD([beamsX, beamsY])

	beams = PROD([beamsXY, QUOTE(beamsZValue)])

	build = STRUCT([pillar, beams])

	return build

def drawStructure(beamDimensions, pillarDimensions, pillarDistances, interstoryHeights):
    """
    drawStructure is a function that, given beam's dimensions, pillars's dimensions, distances between the pillars (y-axis),
    interstory's heights (z-axis), return an HPC model of a space frame of reinforced concrete.
 
    @param beamDimensions: tuple, representing the dimensions of a beam (x,z)
    @param pillarDimensions: tuple, representing the dimensions of a pillar (x,y)
    @param pillarDistances: list representing the distances between pillars [dy1, dy2, ...]
    @param interstoryHeights: list representing the heights of every interstory [dz1, dz2, dz3, ...]
    @return model: HPC model of the space frame
    """
 
    def intersperse(seq, value):
        """
        intersperse is a function that, given a list and a value, intersperse the list with the value.
        If the resultant list has an odd number of elements,
        a value is appended to the end of it.
 
        @param seq: the list to intersperse
        @param value: the value to insert into the new list
        @return res: a new list interspersed
        """
        res = [value] * (2 * len(seq) - 1)
        res[::2] = seq
        if (len(res)%2 != 0):
            res.append(value)
        return res
 
    #generating values for the pillars Y-axis
    linearPillars = intersperse(pillarDistances, pillarDimensions[1])
   
    #generating pillars HPC model
    pillars3D = INSR(PROD)([QUOTE([pillarDimensions[0], -3]),QUOTE(linearPillars), QUOTE(intersperse([-interstory for interstory in interstoryHeights], -beamDimensions[1]))])
   
    #generating values for horizontal beams, perpendicular to X-axis
    #horizontalBeamXXAxis = [(pillarDimensions[0]+3)+pillarDimensions[0]]
     #horizontalBeamYXAxis = intersperse(pillarDistances,pillarDimensions[1])
   
    #generating HPC model of the beams perpendicular to the X-axis
    #beamsX3D = INSR(PROD)([QUOTE(horizontalBeamXXAxis), QUOTE(horizontalBeamYXAxis), QUOTE(intersperse(interstoryHeights,beamDimensions[1]))])
   
    #generating values for horizontal beams perpendicular to the Y-axis
    horizontalBeamXYAxis = [pillarDimensions[0],-3]
    horizontalBeamYYAxis = intersperse([-beam for beam in pillarDistances], pillarDimensions[1])
    horizontalBeamYYAxis[0] = -horizontalBeamYYAxis[0]
   
    #generating HPC model of the beams perpendicular to the Y-axis
    beamsY3D = INSR(PROD)([QUOTE(horizontalBeamXYAxis), QUOTE(horizontalBeamYYAxis), QUOTE(intersperse(interstoryHeights,beamDimensions[1]))])
   
    #assembling the HPC model
    model = STRUCT([pillars3D, beamsY3D])
    return model


building_structure([-1,-2,-3], [1,2,3], 0.4, 0.4, 0.4, 'beams');
building_structure([-1,-2,-3], [1,2,3], 0.4, 0.4, 0.4, 'pillar');

