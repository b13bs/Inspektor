from os import path
from os import walk
from os import system
import re
from Tkinter import Tk
from tkFileDialog import askdirectory
from OCR.OcrTools import *
from report import *
import imghdr

results = []

Tk().withdraw() # pas le full GUI, temporaire..
directory = askdirectory(initialdir=".", title="Select directory to scan")

if directory:
	for root, _, files in walk(directory):
		for filename in files:
			filepath = path.join(root, filename).replace("\\","/")
			#retourne "None" si c'est pas une image
			filetype = imghdr.what(filepath)
			
			if filetype != "None":
				print filetype
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
			system("start " + report)
		except:
			pass
	else:
		print "Canceled."