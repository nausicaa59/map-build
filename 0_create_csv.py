from lxml import etree
import json
import os
import csv
import configs
import tools
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont

#----------------------------------
#Define
#----------------------------------
def extraireCerclesDuSVG(path, output, img):
	tree = etree.parse(path)
	imFond = Image.open(img)
	rgb_im = imFond.convert('RGBA')

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

			#image
			image = tools.extrairePixelImage(int(x), int(y), rgb_im)


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
				"i1": image[0],
				"i2": image[1],
				"i3": image[2]
			})



#extraction info svg
cercles = extraireCerclesDuSVG(
	configs.PATH_BRUT_ALL_PATH, 
	"assets/tempo/clean1.csv",
	"assets/input/image.png"
)

cercles = extraireCerclesDuSVG(
	configs.PATH_BRUT_ALL_PATH, 
	"assets/tempo/clean2.csv",
	"assets/input/image.png"
)

df = pd.read_csv("assets/tempo/clean2.csv", names=configs.HEADER_CSV)
df.x = df.x + 2000
df.y = df.y + 1000
df.c_x0 = df.c_x0 + 2000
df.c_y0 = df.c_y0 + 1000
df.c_x1 = df.c_x1 + 2000
df.c_y1 = df.c_y1 + 1000


df2 = pd.read_csv("assets/tempo/clean1.csv", names=configs.HEADER_CSV)
pd.concat([df, df2]).to_csv(configs.PATH_CLEAN_ALL_PATH, index=False, header=False)