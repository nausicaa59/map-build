from lxml import etree
import json
import os

#----------------------------------
#Define
#----------------------------------
path_input = "assets/input/"
path_svg = path_input + "exemple.xml"
path_data = "assets/tempo/data/"
sectionNbPixel = 256

#----------------------------------
#Function
#----------------------------------
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


def extraireDimentionDuSVG(path):
	tree = etree.parse(path)
	racine = tree.getroot()
	return int(racine.get("width")), int(racine.get("height"))


def extraireCerclesDuSVG(path):
	cercles = []	
	tree = etree.parse(path)

	for user in tree.xpath("g"):
		#data
		idCercle = user.find("circle").get("id")
		rayon = float(user.find("circle").get("r"))

		#couleur
		couleurText = user.find("circle").get("style")
		couleurText = couleurText.replace("fill: rgb(", "")
		couleurText = couleurText.replace(");", "")
		couleurTab = couleurText.split(',')
		couleur = []
		couleur.append(couleurTab[0])
		couleur.append(couleurTab[1])
		couleur.append(couleurTab[2])

		#coordonnee
		coordonneeText = user.get("transform")
		coordonneeText = coordonneeText.replace(")", "");
		coordonneeText = coordonneeText.replace("translate(", "");
		coordonneeTab = coordonneeText.split(',')
		x = float(coordonneeTab[0])
		y = float(coordonneeTab[1])


		cercles.append({
			"id":idCercle,
			"c_x0": x - rayon,
			"c_y0": y - rayon,
			"c_x1": x + rayon,
			"c_y1": y + rayon,
			"r": rayon,
			"couleur" : couleur
		})

	return cercles


#on clean le repertoire data
for filename in os.listdir(path_data) :
    os.remove(path_data + filename)


#extraction info svg
cercles = extraireCerclesDuSVG(path_svg)
largeur, hauteur = extraireDimentionDuSVG(path_svg)


#preparation de la maps
lignes = round(hauteur / sectionNbPixel)
colonnes = round(largeur / sectionNbPixel)


#generation de la maps
for ligne in range(0, lignes):
	for colonne in range(0, colonnes):
		x0 = colonne*sectionNbPixel
		x1 = x0 + sectionNbPixel
		y0 = ligne*sectionNbPixel
		y1 = y0 + sectionNbPixel
		cerclesInclus = cercleDansSection(x0, y0, x1, y1, cercles)
		
		nomFichier = path_data + str(ligne) + "-" + str(colonne)+".json"
		with open(nomFichier, 'w') as out_file:
			out_file.write(json.dumps(cerclesInclus))


print("Traitement terminer avec succès...")