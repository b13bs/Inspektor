from csv import writer
import os
import shutil
from json import dumps
import distutils.core
from Tkinter import Tk
from tkFileDialog import asksaveasfilename

def exportAsCSV(data):
	Tk().withdraw() # pas le full GUI, temporaire..
	filePath = asksaveasfilename(initialdir=".", title="Export as CSV...")
	if filePath:
		out = writer(open(filePath,"wb"), delimiter=',',quoting=csv.QUOTE_ALL)
		out.writerows(data)
		return filePath

def exportAsHTML(data):
	Tk().withdraw() # pas le full GUI, temporaire..
	filePath = asksaveasfilename(initialdir=".", title="Export as HTML...")
	if filePath:
		os.mkdir(filePath)
		fromDirectory = "export_source"
		toDirectory = filePath
		distutils.dir_util.copy_tree(fromDirectory, toDirectory)
		# copier les images
		cpt = 0
		for entry in data:
			imageCopy = toDirectory + "/images/" + str(cpt) + os.path.splitext(entry[0])[1]
			shutil.copy2(entry[0], imageCopy)
			entry.append(imageCopy)
			cpt += 1
		# copier le data
		out = open(filePath+"/data/data.js", "wb")
		jsonData = dumps(data, separators=(',',':'))
		out.write("data = "+jsonData)
		return filePath + "/results.html"