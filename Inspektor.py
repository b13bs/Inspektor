import os
import re
from Tkinter import Tk
from tkFileDialog import askdirectory
from OCR.OcrTools import parseTextFromImage
from report import *

results = []

Tk().withdraw() # pas le full GUI, temporaire..
directory = askdirectory(initialdir=".", title="Select directory to scan")
if directory:
	for root, _, files in os.walk(directory):
		for filename in files:
			if re.match("([^\\s]+(\\.(?i)(jpg|png|gif|bmp|tiff|tif))$)", filename, re.I):
				filepath = os.path.join(root, filename).replace("\\","/")
				print "\n--------- " + filepath + " ----------"
				text, conf = parseTextFromImage(filepath)
				if text and conf:
					results.append([filepath, text, conf])
					print "Confidence: ", conf
					print unicode(text, errors='ignore')

	print "Saving scan results..."
	#report = exportAsCSV(results)
	report = exportAsHTML(results)
	
	if report:
		print "Done."
		
		# on essai d'ouvrir le rapport
		try:
			os.system("start " + report)
		except:
			pass
	else:
		print "Canceled."