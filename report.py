import csv
import os
import shutil
from json import dumps
import distutils.core

def createReportDirectoryTree(filePath):
	if filePath:
		os.mkdir(filePath)
		fromDirectory = "export_source"
		toDirectory = filePath
		distutils.dir_util.copy_tree(fromDirectory, toDirectory)
		
def exportReport(filePath, data):
	if filePath:
		# cree les repertoires si pas deja fait
		if not os.path.exists(filePath):
			createReportDirectoryTree(filePath)
		# copie le csv
		csvOut = csv.writer(open(filePath+"/csv/results.csv","wb"), delimiter=',',quoting=csv.QUOTE_ALL)
		csvOut.writerows(data)
		# copie le html
		htmlOut = open(filePath+"/data/data.js", "wb")
		jsonData = dumps(data, separators=(',',':'))
		htmlOut.write("data = "+jsonData)
		return filePath + "/results.html"