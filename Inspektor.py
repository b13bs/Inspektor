import os
import re
from Tkinter import Tk
from tkFileDialog import askdirectory
from OCR.OcrTools import parseTextFromImage
from report import *

exportAsCSV([["bob.jpg","bob",0.3],["jo.png","je mapelle jo blo!!",0.8]])
exportAsHTML([["bob.jpg","bob",0.3],["jo.png","je mapelle jo blo!!",0.8]])
Tk().withdraw() # pas le full GUI, temporaire..
directory = askdirectory(initialdir=".", title="Select directory to scan")
if directory:
	for root, _, files in os.walk(directory):
		for filename in files:
			if re.match("([^\\s]+(\\.(?i)(jpg|png|gif|bmp|tiff|tif))$)", filename, re.I):
				filepath = os.path.join(root, filename)
				print "\n--------- " + filepath + " ----------"
				text, conf = parseTextFromImage(filepath)
				if text and conf:
					print "Confidence: ", conf
					print unicode(text, errors='ignore')
