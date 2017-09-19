PIXEL_BY_SECTION 	= 256
HAUTEUR 			= 2000
LARGEUR 			= 2000
NB_LIGNES 			= round(HAUTEUR / PIXEL_BY_SECTION)
NB_COLONNES 		= round(LARGEUR / PIXEL_BY_SECTION)

HEADER_CSV = ['id', 'x', 'y', 'r', 'c1', 'c2', 'c3', 'c_x0', 'c_y0', 'c_x1', 'c_y1']

PATH_BRUT_ALL_PATH 	= "assets/input/exemple.xml"
PATH_CLEAN_ALL_PATH = "assets/tempo/clean.csv"
PATH_TEMPO_FILE_DIM = "assets/tempo/txt/"