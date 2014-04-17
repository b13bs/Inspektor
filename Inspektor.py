#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from os import walk
from os import system
from os import getcwd
from os import mkdir
import shutil
import imghdr
import Tkinter as tk
import ttk
import tkFileDialog
import sys
import tkMessageBox
import hashlib
from OCR.OcrTools import *
from report import *

DEBUG = False

class GUI(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid(column=4, row=7)
		self.createWidgets()

	def createWidgets(self):
		self.searchString = tk.StringVar()
		self.searchDirectory = ""
		self.outputLocation = ""
		rowNumber = 1

		searchDirectoryName = ttk.Label(self, text="Directory to scan")
		searchDirectoryName.grid(column=1, row=rowNumber, columnspan=2, padx=5, pady=5)
		searchDirectoryButton = ttk.Button(self, text="Browse", command = lambda: self.directorySearch("input"))
		searchDirectoryButton.grid(column=3, row=rowNumber, columnspan=2, padx=5, pady=5)
		rowNumber += 1

		self.searchDirectoryLabel = ttk.Label(self, text="")
		self.searchDirectoryLabel.grid(column=1, row=rowNumber, columnspan=4, padx=5, pady=5)
		rowNumber += 1

		outputLocationName = ttk.Label(self, text="Report output location")
		outputLocationName.grid(column=1, row=rowNumber, columnspan=2, padx=5, pady=5)
		outputLocationButton = ttk.Button(self, text="Browse", command = lambda: self.directorySearch("output"))
		outputLocationButton.grid(column=3, row=rowNumber, columnspan=2, padx=5, pady=5)
		rowNumber += 1

		self.outputLocationLabel = ttk.Label(self, text="")
		self.outputLocationLabel.grid(column=1, row=rowNumber, columnspan=4, padx=5, pady=5)
		rowNumber += 1

		searchButton = ttk.Button(self, text="Search", command=self.search)
		searchButton.grid(column=1, row=rowNumber, columnspan=4, padx=5, pady=5)
		rowNumber += 1

		self.progressBar = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
		self.progressBar.grid(column=1, row=rowNumber, columnspan=4, padx=5, pady=5)
		rowNumber += 1

		self.status = ttk.Label(self, text="")
		self.status.grid(column=1, row=rowNumber, columnspan=4, padx=5, pady=5)

	def directorySearch(self, action):
		if action == "input":
			self.searchDirectory = tkFileDialog.askdirectory(initialdir=".", title="Select directory to scan", parent=self)
			self.searchDirectoryLabel['text'] = self.searchDirectory
		elif action == "output":
			self.outputLocation = tkFileDialog.asksaveasfilename(initialdir=os.getcwd(), title="Select the output directory", parent=self) #, mustexist=False
			self.outputLocationLabel['text'] = self.outputLocation
		else:
			if DEBUG: print "wut?"
			sys.exit()

	def search(self):
		self.progressBar["value"] = 0
		self.progressBar["maximum"] = 1000
		
		if DEBUG: print "GO"
		if DEBUG: print "searchDirectory: " + self.searchDirectory
		if DEBUG: print "outputLocation: " + self.outputLocation

		# Verification pour inputs manquants avant le debut du scan
		errors = []

		if not self.searchDirectory:
			errors.append("- The directory to scan")
		if not self.outputLocation:
			errors.append("- The report output location")

		if errors:
			message = "Please fill in the following fields:\n" + "\n".join(errors)
			tkMessageBox.showinfo("Error", message)
		else:
			# On cree le repertoire d'output du rapport
			createReportDirectoryTree(self.outputLocation)
			
			# Debut du scan
			results = []
			
			
			# On passe au travers du repertoire en question
			if DEBUG: print "Inspecting..."

			# Calcul de la valeur maximale de la progress bar
			maxValue = 0
			for root, _, files in walk(self.searchDirectory):
				for filename in files:
					maxValue += 1
			self.progressBar["maximum"] = maxValue
			
			cpt = 0
			for root, _, files in walk(self.searchDirectory):
				# Pour chaque fichier
				for filename in files:
					# Mise a jour de la progress bar
					self.progressBar["value"] += 1
					if DEBUG: print self.progressBar["value"], "/", self.progressBar["maximum"]
					self.progressBar.update_idletasks()
					self.update()

					filepath = path.join(root, filename).replace("\\","/")
					
					# On analyse l'en-tete du fichier pour determiner s'il s'agit d'une image
					# imghdr retourne "None" si ce c'est pas une image, ou sinon le format de l'image
					imgType = imghdr.what(filepath)
					
					if imgType and imgType != "None":
						# Une image!
						if DEBUG: print "\n--------- " + filepath + " ----------"
						if DEBUG: print "Type: " + imgType
						
						# On copie l'image vers le rapport avec la bonne extension
						imgCopy = self.outputLocation + "/images/" + str(cpt) + "." + imgType
						shutil.copy2(filepath, imgCopy)
						cpt += 1
						
						# On essaie d'y trouver du texte par de la ROC
						text, conf = parseTextFromImage(imgCopy)
						
						# S'il y a resultat, on l'ajoute a la liste
						if text and conf:
							# On calcule le md5 du fichier original
							md5 = hashlib.md5(open(filepath, 'rb').read()).hexdigest()
							
							results.append([filepath, text, conf, imgCopy, md5])
							if DEBUG: print "Confidence: ", conf
							if DEBUG: print unicode(text, errors='ignore')
							
			if DEBUG: print "Done."
			if DEBUG: print "Saving scan results..."
			report = exportReport(self.outputLocation, results)
			if DEBUG: print "REPORT: " + report
			if report:
				# Rapport cree
				if DEBUG: print "Done."
				# On s'assure que la progress bar est a 100%
				self.progressBar["value"] = 100
				self.progressBar["maximum"] = 100
				# On demande si l'utilisateur veut ouvrir le rapport immediatement
				if tkMessageBox.askyesno("Success", "The inspection is done.\nDo you want to open the resulting report in your default browser?"):
					# on essai d'ouvrir le rapport
					try:
						system("start " + report)
					except:
						pass
			else:
				if DEBUG: print "Canceled."

	def increment(self):
		self.progressBar["value"] += 100
		if DEBUG: print self.progressBar["value"] , self.progressBar["maximum"]
		if self.progressBar["value"] < self.progressBar["maximum"]:
			self.after(1, self.increment) 

	def bye(self):
		if DEBUG: print "bye"

app = GUI()
app.master.title('Inspektor')
app.master.iconbitmap('Inspektor.ico')
app.mainloop()