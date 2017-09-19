from lxml import etree
import json
import os
import csv
import configs

#----------------------------------
#Define
#----------------------------------
def extraireCerclesDuSVG(path, output):
	cercles = []	
	tree = etree.parse(path)

	with open(output, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=configs.HEADER_CSV)		

		for user in tree.xpath("g"):
			#data
			idCercle = user.find("circle").get("id")
			rayon = float(user.find("circle").get("r"))

			#couleur
			couleurText = user.find("circle").get("style")
			couleurText = couleurText.replace("fill: rgb(", "")
			couleurText = couleurText.replace(");", "")
			couleurTab = couleurText.split(',')

			#coordonnee
			coordonneeText = user.get("transform")
			coordonneeText = coordonneeText.replace(")", "");
			coordonneeText = coordonneeText.replace("translate(", "");
			coordonneeTab = coordonneeText.split(',')
			x = float(coordonneeTab[0])
			y = float(coordonneeTab[1])


			writer.writerow({
				"id":idCercle,
				"x": x,
				"y": y,
				"r": rayon,
				"c1" : couleurTab[0],
				"c2" : couleurTab[1],
				"c3" : couleurTab[2],
				"c_x0": x - rayon,
				"c_y0": y - rayon,
				"c_x1": x + rayon,
				"c_y1": y + rayon,
			})

	return cercles



#extraction info svg
cercles = extraireCerclesDuSVG(configs.PATH_BRUT_ALL_PATH, configs.PATH_CLEAN_ALL_PATH)
