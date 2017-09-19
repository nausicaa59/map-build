from PIL import Image, ImageDraw, ImageFont
import json
import os
import copy
import sys

#----------------------------------
#Define
#----------------------------------
path_data = "assets/tempo/data/"
path_test = "assets/tempo/test/"
path_police = "assets/input/nasalization-rg.ttf"
path_absolute = "C:/laragon/www/map/build/"
sectionNbPixel = 256
imFond = Image.open("assets/input/image.png")
rgb_im = imFond.convert('RGBA')
fichiers_data = os.listdir(path_data)




#----------------------------------
#Function
#----------------------------------
def parseJsonFile(path):
	cercles = []
	with open(path, 'r') as sectionFile:
		cercles = json.load(sectionFile)
	return cercles


def getCouleurCercle(cercle):
	return (int(cercle["couleur"][0]), int(cercle["couleur"][1]), int(cercle["couleur"][2]))



def extrairePixelImage(cercle):
	x = cercle["c_x0"]
	y = cercle["c_y0"]
	r, g, b, a = rgb_im.getpixel((x, y))
	if a is not 0:
		return (r, g, b)
	else:
		return (35,78,154)


def cercleDansSection(x0, y0, x1, y1, cercles):
	liste = []

	for cercle in cercles:
		#condition X
		scond_x1 = (cercle["c_x0"] > x0 and cercle["c_x1"] < x1)
		scond_x2 = (cercle["c_x0"] < x0 and cercle["c_x1"] > x1)
		scond_x3 = (cercle["c_x0"] < x0 and cercle["c_x1"] > x0)
		scond_x4 = (cercle["c_x0"] < x1 and cercle["c_x1"] > x1)
		condition_x = (scond_x1 or scond_x2 or scond_x3 or scond_x4)

		#condition y
		scond_y1 = (cercle["c_y0"] > y0 and cercle["c_y1"] < y1)
		scond_y2 = (cercle["c_y0"] < y0 and cercle["c_y1"] > y1)
		scond_y3 = (cercle["c_y0"] < y0 and cercle["c_y1"] > y0)
		scond_y4 = (cercle["c_y0"] < y1 and cercle["c_y1"] > y1)
		condition_y = (scond_y1 or scond_y2 or scond_y3 or scond_y4)

		if condition_y and condition_x :
			liste.append(cercle)

	return liste


#dessine des cercles en fonction d'une liste contenant les positions des cercles...
def tracerCercle(options, cercles):
	if os.path.isfile(options["pathOutput"]) is True:
		print(options["pathOutput"]+" existe déja...")
		return

	im = Image.new("RGB", (options["size"]*options["qualite"], options["size"]*options["qualite"]), "black")
	draw = ImageDraw.Draw(im)

	for cercle in cercles:
		X0 = (cercle["c_x0"] - options["correctionOrigine_x"]) * options["qualite"]
		Y0 = (cercle["c_y0"] - options["correctionOrigine_y"]) * options["qualite"]
		X1 = (cercle["c_x1"] - options["correctionOrigine_x"]) * options["qualite"]		
		Y1 = (cercle["c_y1"] - options["correctionOrigine_y"]) * options["qualite"]
		
		if options["imageFond"] is True:
			couleur = extrairePixelImage(cercle)
		else:
			couleur = getCouleurCercle(cercle)
		
		draw.ellipse((X0, Y0, X1, Y1), fill=couleur)

		if options["display_text"] is True:
			PseudoNbCaracte = len(cercle["id"])
			PseudoLargeurByCaract = (X1 - X0)/PseudoNbCaracte
			PseudoPoliceTaille = ((1.2755*PseudoLargeurByCaract) -0.0127)
			PseudoPoliceTaille = round(PseudoPoliceTaille)
			
			if options["force_text"] is True:
				if PseudoPoliceTaille < 15:
					PseudoPoliceTaille = 16

			font = ImageFont.truetype(path_police, PseudoPoliceTaille)
			TL, TH = font.getsize(cercle["id"])
			TX = (X0 + X1)/2 - (TL / 2)
			TY = (Y0 + Y1)/2 - (TH / 2)
		
			if PseudoPoliceTaille >= 15:		
				draw.text((TX, TY), cercle["id"], font=font)



	del draw

	repertoire = os.path.dirname(options["pathOutput"])
	if os.path.isdir(repertoire) is False:
		os.makedirs(repertoire)

	im.save(options["pathOutput"], "PNG")
	im.close()

	if options["qualite"] > 1:
		os.system('convert "' + path_absolute + options["pathOutput"] + '" -resize 256x256 -antialias "'+ path_absolute + options["pathOutput"] +'"')
	
	print("Image : " + options["pathOutput"] + "traitée !")


def genererDimentionInferieur(options, source):
	facteur = 2 ** options["dimension"]
	aggrandisement = copy.deepcopy(source)
	correctionOrigine_x = options["correctionOrigine_x"]
	correctionOrigine_y = options["correctionOrigine_y"]

	for i, cercle in enumerate(aggrandisement):
		aggrandisement[i]["c_x0"] = aggrandisement[i]["c_x0"]*facteur
		aggrandisement[i]["c_x1"] = aggrandisement[i]["c_x1"]*facteur
		aggrandisement[i]["c_y0"] = aggrandisement[i]["c_y0"]*facteur
		aggrandisement[i]["c_y1"] = aggrandisement[i]["c_y1"]*facteur


	for a in range(0,facteur):
		for b in range(0,facteur):
			nomY = str((options["nom_start_y"] * (2**options["dimension"])) + a)
			nomX = str((options["nom_start_x"] * (2**options["dimension"])) + b)
			nom = str(options["dimension"] + options["nom_start_dim"]) + "/" + nomY + "/" + nomX + ".png"
			options["pathOutput"] = path_test + nom
			
			options["correctionOrigine_x"] = (correctionOrigine_x*facteur) + (b * options["size"])
			options["correctionOrigine_y"] = (correctionOrigine_y*facteur) + (a * options["size"])

			zoneRx0 = options["correctionOrigine_x"] - sectionNbPixel*2;
			zoneRx1 = options["correctionOrigine_x"] + sectionNbPixel*2;
			zoneRy0 = options["correctionOrigine_y"] - sectionNbPixel*2;
			zoneRy1 = options["correctionOrigine_y"] + sectionNbPixel*2;
			selectionCercle = cercleDansSection(zoneRx0, zoneRy0, zoneRx1, zoneRy1, aggrandisement)
			tracerCercle(options, selectionCercle)



#----------------------------------
#recherche argument...
#----------------------------------
ligneCible = -1

for arg in sys.argv:
	if arg.find("-ligne=") is not -1:
		ligneCible = int(arg.replace("-ligne=",""))


if ligneCible is not -1:
	fichiers_data = [x for x in fichiers_data if x.find(str(ligneCible)+"-") is not -1]

print(fichiers_data)


for filename in fichiers_data :
	coordonnesText = filename.replace(".json","")
	coordonnesTab = coordonnesText.split("-")
	numLigne = int(coordonnesTab[0])
	numColonne = int(coordonnesTab[1])
	cercles = parseJsonFile(path_data + filename)

	
	options = {
		"size" : sectionNbPixel,
		"pathOutput" : path_test + "0/" + str(numLigne) + "/" + str(numColonne) + ".png",
		"correctionOrigine_x" : numColonne * sectionNbPixel,
		"correctionOrigine_y" : numLigne * sectionNbPixel,
		"display_text" : True,
		"force_text" : False,
		"qualite" : 4,
		"imageFond" : True
	}	
	#tracerCercle(options, cercles)


	optionsBis = copy.deepcopy(options)
	optionsBis["nom_start_dim"] = 0
	optionsBis["nom_start_y"] = numLigne
	optionsBis["nom_start_x"] = numColonne
	optionsBis["dimension"] = 1
	optionsBis["imageFond"] = False
	genererDimentionInferieur(optionsBis, cercles)

	
	'''
	optionsBis = copy.deepcopy(options)
	optionsBis["nom_start_dim"] = 0
	optionsBis["nom_start_y"] = numLigne
	optionsBis["nom_start_x"] = numColonne
	optionsBis["dimension"] = 2
	optionsBis["imageFond"] = False
	genererDimentionInferieur(optionsBis, cercles)
	'''

	'''
	optionsBis = copy.deepcopy(options)
	optionsBis["nom_start_dim"] = 0
	optionsBis["nom_start_y"] = numLigne
	optionsBis["nom_start_x"] = numColonne
	optionsBis["dimension"] = 3
	optionsBis["imageFond"] = False
	genererDimentionInferieur(optionsBis, cercles)
	'''
	
	'''
	optionsBis = copy.deepcopy(options)
	optionsBis["nom_start_dim"] = 0
	optionsBis["nom_start_y"] = numLigne
	optionsBis["nom_start_x"] = numColonne
	optionsBis["dimension"] = 4
	optionsBis["imageFond"] = False
	genererDimentionInferieur(optionsBis, cercles)
	'''

	'''
	optionsBis = copy.deepcopy(options)
	optionsBis["nom_start_dim"] = 0
	optionsBis["nom_start_y"] = numLigne
	optionsBis["nom_start_x"] = numColonne
	optionsBis["dimension"] = 5
	optionsBis["imageFond"] = False
	genererDimentionInferieur(optionsBis, cercles)
	'''

	"""
	optionsBis = copy.deepcopy(options)
	optionsBis["nom_start_dim"] = 0
	optionsBis["nom_start_y"] = numLigne
	optionsBis["nom_start_x"] = numColonne
	optionsBis["dimension"] = 6
	optionsBis["imageFond"] = False
	optionsBis["force_text"] = True
	optionsBis["qualite"] = 1
	genererDimentionInferieur(optionsBis, cercles)
	"""		

print("Traitement terminer avec succès...")