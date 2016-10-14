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

def building_structure_continuous_pillar(distancesPillar, interstoryHeights, pX, pY, bY):
	""" building structure by continuous pillar """	

	pillarXValue = []
	interstoryValue = []
	beamsZValue = []
	bX = []


	for element in distancesPillar:
		bX.append(-pX)
		bX.append(-element)
		pillarXValue.append(pX)
		pillarXValue.append(element)

	for element in interstoryHeights:
		beamsZValue.append(-element)
		beamsZValue.append(bY)
		interstoryValue.append(element + bY)

	pillarXValue.append(pX)

	pillarX = QUOTE(pillarXValue)
	pillarY = QUOTE([pY])
	pillarXY = PROD([pillarX, pillarY])

	pillar = PROD([pillarXY, QUOTE(interstoryValue)])

	beamsX = QUOTE(bX)
	beamsY = QUOTE([bY])
	beamsXY = PROD([beamsX, beamsY])

	beams = PROD([beamsXY, QUOTE(beamsZValue)])

	build = STRUCT([pillar, beams])

	return build


building_structure([-1,-2,-3], [1,2,3], 0.4, 0.4, 0.4, 'beams');
building_structure([-1,-2,-3], [1,2,3], 0.4, 0.4, 0.4, 'pillar');

