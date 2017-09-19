import os
import configs


def ConditionCercleDansSection(x0, y0, x1, y1):
	#condition X
	scond_x1 = "(c_x0 > "+str(x0)+ " and c_x1 < "+str(x1) +")"
	scond_x2 = "(c_x0 < "+str(x0)+ " and c_x1 > "+str(x1) +")"
	scond_x3 = "(c_x0 < "+str(x0)+ " and c_x1 > "+str(x0) +")"
	scond_x4 = "(c_x0 < "+str(x1)+ " and c_x1 > "+str(x1) +")"
	condition_x = "(" + scond_x1 + " or " + scond_x2 + " or " + scond_x3 + " or " + scond_x4 + ")"

	#condition y
	scond_y1 = "(c_y0 > "+str(y0)+ " and c_y1 < "+str(y1) +")"
	scond_y2 = "(c_y0 < "+str(y0)+ " and c_y1 > "+str(y1) +")"
	scond_y3 = "(c_y0 < "+str(y0)+ " and c_y1 > "+str(y0) +")"
	scond_y4 = "(c_y0 < "+str(y1)+ " and c_y1 > "+str(y1) +")"
	condition_y = "(" + scond_y1 + " or " + scond_y2 + " or " + scond_y3 + " or " + scond_y4 + ")"
	
	return condition_x + " and " + condition_y


def fileInfo(file):
 	file = file.replace(".csv", "")
 	fragments = [int(x) for x in file.split("-")]
 	return fragments



def filesByDim(dim):
	files = []
	path = configs.PATH_TEMPO_FILE_DIM + str(dim) + "/"

	for dossier, sous_dossiers, fichiers in os.walk(path):
		for file in fichiers:
			info = fileInfo(file)
			files.append({
				"name" : file,
				"full_path" : dossier + "/" + file,
				"ligne" : info[0],
				"colonne" : info[1],
			})

	return files


