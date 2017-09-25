import json
import os
import copy
import sys

#----------------------------------
#Define
#----------------------------------
for root, subdirs, files in os.walk("C:/laragon/www/map/build/assets/output/3"):
	for filename in files:
		pathFile = os.path.join(root, filename).replace("\\","/")
		print(pathFile)
		os.system('magick convert "' + pathFile + '" -resize 256x256 -antialias "'+ pathFile +'"')
