from csv import writer
from os import mkdir
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
		mkdir(filePath)
		fromDirectory = "export_source"
		toDirectory = filePath
		distutils.dir_util.copy_tree(fromDirectory, toDirectory)
		out = open(filePath+"/data/data.js", "wb")
		jsonData = dumps(data, separators=(',',':'))
		out.write("data = "+jsonData)
		return filePath + "/results.html"