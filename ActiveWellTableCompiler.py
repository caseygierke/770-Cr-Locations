# ActiveWellTableCompiler.py

# This script compiles well information from the 
# Active, Exceedance and Substantial Data files 
# created by the SummaryStats.py file. 

# Written by Casey Gierke of Lee Wilson & Associates
# on 4/23/2020

# With Notepad++, use F5 then copy this into box
# C:\Users\Casey\Anaconda3\python.exe -i "$(FULL_CURRENT_PATH)"

# ------------------------------------------------------
# IMPORTS
# ------------------------------------------------------

import os
import glob

# ------------------------------------------------------
# DEFINE FUNCTIONS
# ------------------------------------------------------

# Define last position finder
def find_last(s,t):
	last_pos = -1
	while True:
		pos = s.find(t, last_pos +1)
		if pos == -1:
			return last_pos
		last_pos = pos
		
# Define getLocations
def getLocations(filePath):
	# Define input file
	WI_In = open(filePath, 'r')
	# Define wellInfo dictionary
	wellInfo = {}
	# Loop through wellInfoIn
	for line in WI_In:
		# Split up input line
		cols = line.split('\t')
		if cols[0] not in wellInfo:
			wellInfo[cols[0]] = {}
	return wellInfo
	
def dictOut(dict, path):
	fout = open(path, 'w')
	# Write header line
	fout.write(headers[:-1]+'\tReason Code\n')
	# Loop through dictionary to write to file
	for item in dict:
		fout.write(dict[item])
	fout.close()
	
def addToDict(inFile, source, dict, reasonCode):
	for location in inFile:
		if location not in wellInfo:
			print(reasonCode)
			dict[location] = source[location][:-1]+reasonCode+'\n'
			# print(source[location][:-1])
		else:
			dict[location] = dict[location][:-1]+', '+reasonCode+'\n'
	
# ------------------------------------------------------
# INPUTS
# ------------------------------------------------------

# Define path
path = os.path.abspath(os.path.dirname(__file__))
# Shorten path to one folder up
path = path[:find_last(path,os.sep)]

# Define parameters you are using
# parameter = 'Chromium'
# Which file type are you using
type = 'Compiled- Narrowed'
# # type = 'Active'

# Define dictionary
wellInfo = {}

# Create wellData dictionary
wellData = getLocations(path+os.sep+'Locations'+os.sep+'Outputs'+os.sep+type+'.txt')

# Open Well Info source file
compiledIn = open(path+os.sep+'Locations'+os.sep+'Outputs'+os.sep+type+'.txt', 'r')

# Get first line
cols = compiledIn.readline()
headers = cols

# Populate wellData dictionary
for line in compiledIn:
	cols = line.split('\t')
	location = cols[0]
	
	wellData[location] = line

# ------------------------------------------------------
# Get wells from Active
activeInfo = getLocations(path+os.sep+'Locations'+os.sep+'Outputs'+os.sep+'Active- '+type+'.txt')

# Add locations from active to the wellInfo dictionary
addToDict(activeInfo, wellData, wellInfo, 'Active')

# ------------------------------------------------------
# Get wells from Exceedance
exceedanceInfo = getLocations(path+os.sep+'Locations'+os.sep+'Outputs'+os.sep+'Exceedance- '+type+'.txt')

# Add locations from exceedance to the wellInfo dictionary
addToDict(exceedanceInfo, wellData, wellInfo, 'Exceedance')

# ------------------------------------------------------
# Get wells from Substantial Data
substantialInfo = getLocations(path+os.sep+'Locations'+os.sep+'Outputs'+os.sep+'Substantial Data- '+type+'.txt')

# Add locations from substantial to the wellInfo dictionary
addToDict(substantialInfo, wellData, wellInfo, 'Substantial')

# ------------------------------------------------------
# Write to outfiles
# ------------------------------------------------------

# Write to outfile
dictOut(wellInfo, path+os.sep+'Locations'+os.sep+'Outputs'+os.sep+'Final- '+type+'.txt')
