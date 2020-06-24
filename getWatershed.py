# getWatershed.py

# This file reads in the Watersheds- Revised.shp file 
# then updates the Watershed column in the Compiled- 
# Narrowed- For Watersheds.txt file to create another
# file Compiled- Narrowed- For DB.txt that is ready 
# to be imported to the SQL server database

# Written by Casey Gierke of Lee Wilson & Associates 
# on 5/1/2020

# ------------------------------------------------------
# IMPORTS
# ------------------------------------------------------

import shapefile as shp
from shapely.geometry import Point
# import csv
from shapely.geometry.polygon import Polygon
import os
# import numpy as np

# ------------------------------------------------------
# DEFINE FUNCTIONS
# ------------------------------------------------------

# # Define last position finder
# def find_last(s,t):
	# last_pos = -1
	# while True:
		# pos = s.find(t, last_pos +1)
		# if pos == -1:
			# return last_pos
		# last_pos = pos

# ------------------------------------------------------
# OPERATIONS
# ------------------------------------------------------

# Define path
path = os.path.abspath(os.path.dirname(__file__))

# Define file name to open
fileName = 'Compiled- Narrowed- For Watersheds' 

#Open Location file to update
locationFile = open(path+os.sep+'Outputs'+os.sep+fileName + '.txt', 'r')

#Open Location file to write to
fout = open(path+os.sep+'Outputs'+os.sep+'Compiled- Narrowed- For DB.txt', 'w')

#Open Shapefile with shapes to check points against
sf = shp.Reader('C:'+os.sep+'Projects'+os.sep+'770- LANL'+os.sep+'GIS'+os.sep+'Chromium'+os.sep+'Extended Chromium Examination Area'+os.sep+"Watersheds- Revised") 
# # IEc file takes a very long time and does not populate all the fields
# sf = shp.Reader('C:'+os.sep+'Projects'+os.sep+'770- LANL'+os.sep+'GIS'+os.sep+'Chromium'+os.sep+'Extended Chromium Examination Area'+os.sep+"Watersheds_IEcD-Lat-Long") 
# sf = shp.Reader('C:'+os.sep+'Projects'+os.sep+'770- LANL'+os.sep+'GIS'+os.sep+'Chromium'+os.sep+'Extended Chromium Examination Area'+os.sep+"Watersheds_IEc_Grouped") 

#Read records in shapefile
sfRec = sf.records() 

n = 0
coorDict = {}
matplotDict = []
watershedFinal = {}

indexLocation = 1

#Iterate through shapes in shapefile
for shape in sf.shapeRecords(): 
	#Initially for use in matplotlib to check shapefile
	x = [point[0] for point in shape.shape.points[:]] 
	#Initially for use in matplotlib to check shapefile
	y = [point[1] for point in shape.shape.points[:]] 

	# Check if canyon in sfRec[n][1]
	if 'Canyon' in sfRec[n][indexLocation]:
		print('Changing '+sfRec[n][indexLocation])
		sfRec[n][indexLocation] = sfRec[n][indexLocation][:-7]
	
	# Check if polygon already exists
	if sfRec[n][indexLocation] in watershedFinal:
		
		print(sfRec[n][indexLocation]+' exists, adding to it')
		
		# Get existing array
		matplotDict = list(watershedFinal[sfRec[n][indexLocation]].exterior.coords)
		
	for point in x:
		#Convert coordinates to be read by Shapely pkg
		matplotDict.append((x[x.index(point)],y[x.index(point)])) 

	#Store shape in dictionary with key of watershedcipality
	watershedFinal[sfRec[n][indexLocation]] = Polygon(matplotDict) 

	#refresh coordinate store for next shape   
	matplotDict = [] 
	n += 1 

# Fix Mortandad spelling
watershedFinal['Mortandad'] = watershedFinal['Mortendad']
del watershedFinal['Mortendad']

# Get first line
headerLine = locationFile.readline()
cols = headerLine.split('\t')
headers = cols

# Write headers to outFile
fout.write(headerLine)

# # Get desired indices from header row
locID_index = headers.index('Location ID')
lat_index = headers.index('Latitude')
long_index = headers.index('Longitude')
type_index = headers.index('Aquifer')
ws_index = headers.index('Watershed')

# Loop through locationFile
for line in locationFile:
	
	# Split line into columns
	cols = line.split('\t')
	
	# Define location
	location = cols[locID_index]
	# Extract coordinates
	rlat = float(cols[lat_index])
	rlong = float(cols[long_index])
	coor = (rlong, rlat)

	# Build coorDict
	coorDict[cols[locID_index]] = (rlong, rlat)

	# Check watershed location is within 
	for ws in watershedFinal:
		if Point(coorDict[location]).within(watershedFinal[ws]):
			print(location, 'in', ws)
			
			# Redefine watershed
			if location[:4] == 'R-23':
				cols[ws_index] = 'Pajarito'
			else:
				cols[ws_index] = ws
	# Convert cols list to string
	outLine = '\t'.join(cols)
	fout.write(outLine)

# Close files
locationFile.close()
fout.close()

