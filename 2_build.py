import pandas as pd
import numpy as np
import time
import os
import tools
import configs


#preparation de la maps
dim = 5
dim_folder = configs.PATH_TEMPO_FILE_DIM + str(dim)
old_dim = dim - 1
old_files = tools.filesByDim(old_dim)


if os.path.isdir(dim_folder) == False:
	os.mkdir(dim_folder)


for file in old_files:
	print(file)
	df = pd.read_csv(file["full_path"], names=configs.HEADER_CSV)
	df.x = df.x*2
	df.y = df.y*2
	df.r = df.r*2
	df.c_x0 = df.c_x0*2
	df.c_y0 = df.c_y0*2
	df.c_x1 = df.c_x1*2
	df.c_y1 = df.c_y1*2

	for a in range(0,2):
		ligne = (file["ligne"] * 2) + a
		folder = dim_folder + "/" + str(ligne)
		if os.path.isdir(folder) == False:
			os.mkdir(folder)

		for b in range(0,2):			
			colonne = (file["colonne"] * 2) + b
			nomFile = str(ligne) + "-" + str(colonne) + ".csv"
			completePath = configs.PATH_TEMPO_FILE_DIM + str(dim) + "/" + str(ligne) + "/" + nomFile

			x0 = colonne*configs.PIXEL_BY_SECTION
			x1 = x0 + configs.PIXEL_BY_SECTION
			y0 = ligne*configs.PIXEL_BY_SECTION
			y1 = y0 + configs.PIXEL_BY_SECTION

			q = tools.ConditionCercleDansSection(x0, y0, x1, y1)
			df_filtered = df.query(q)
			df_filtered.to_csv(completePath, header=False)
