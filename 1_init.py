import pandas as pd
import numpy as np
import time
import os
import tools
import configs


#preparation de la maps
df = pd.read_csv(configs.PATH_CLEAN_ALL_PATH, names=configs.HEADER_CSV)



#generation de la maps
for ligne in range(0, configs.NB_LIGNES):

	folder = configs.PATH_TEMPO_FILE_DIM + "0/" + str(ligne)
	if os.path.isdir(folder) == False:
		os.mkdir(folder)

	for colonne in range(0, configs.NB_COLONNES):
		x0 = colonne*configs.PIXEL_BY_SECTION
		x1 = x0 + configs.PIXEL_BY_SECTION
		y0 = ligne*configs.PIXEL_BY_SECTION
		y1 = y0 + configs.PIXEL_BY_SECTION
		name = folder + "/" + str(ligne) + "-" + str(colonne) + ".csv"
		q = tools.ConditionCercleDansSection(x0, y0, x1, y1)
		df_filtered = df.query(q)
		df_filtered.to_csv(name, header=False)


