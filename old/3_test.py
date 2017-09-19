from PIL import Image, ImageDraw, ImageFont
import json
import os
import copy


#----------------------------------
#Define
#----------------------------------
path_data = "assets/tempo/data/"
path_file_output = "assets/output/coordonnees.sql"
finalSql = ""

#----------------------------------
#Function
#----------------------------------
def parseJsonFile(path):
	cercles = []
	with open(path, 'r') as sectionFile:
		cercles = json.load(sectionFile)
	return cercles


for filename in os.listdir(path_data) :
	cercles = parseJsonFile(path_data + filename)
	for cercle in cercles:
		finalSql += "UPDATE auteurs SET coord_X = '"+ str((cercle["c_x0"]+cercle["c_x1"])/2) +"', coord_Y = '"+ str((cercle["c_y0"]+cercle["c_y1"])/2) +"' WHERE pseudo = '"+ str(cercle["id"]) +"';\n"


with open(path_file_output, 'w') as out_file:
	out_file.write(finalSql)