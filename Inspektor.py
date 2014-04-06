#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from os import walk
from os import system
from os import getcwd
import imghdr
import Tkinter as tk
import ttk
import tkFileDialog
import sys
import tkMessageBox
from OCR.OcrTools import *
from report import *

DEBUG = False

class GUI(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid(column=4, row=7)
		self.createWidgets()

	def createWidgets(self):
		#self.language = tk.StringVar()
		self.searchString = tk.StringVar()
		self.searchDirectory = ""
		self.outputLocation = ""
		rowNumber = 1

		#searchStringName = ttk.Label(self, text="String search")
		#searchStringName.grid(column=1, row=rowNumber, columnspan=2, padx=5, pady=5)
		#self.searchStringEntry = ttk.Entry(self)
		#self.searchStringEntry.grid(column=3, row=rowNumber, columnspan=2, padx=5, pady=5)
		#rowNumber += 1

		searchDirectoryName = ttk.Label(self, text="Directory to scan")
		searchDirectoryName.grid(column=1, row=rowNumber, columnspan=2, padx=5, pady=5)
		searchDirectoryButton = ttk.Button(self, text="Browse", command = lambda: self.directorySearch("input"))
		searchDirectoryButton.grid(column=3, row=rowNumber, columnspan=2, padx=5, pady=5)
		rowNumber += 1

		self.searchDirectoryLabel = ttk.Label(self, text="")
		self.searchDirectoryLabel.grid(column=1, row=rowNumber, columnspan=4, padx=5, pady=5)
		rowNumber += 1

		#reportLangName = ttk.Label(self, text="Report language")
		#reportLangName.grid(column=1, row=rowNumber, columnspan=2, padx=5, pady=5)
		#reportLangFr = ttk.Radiobutton(self, text="FR", value="fr", variable=self.language)
		#reportLangFr.grid(column=3, row=rowNumber, padx=5, pady=5)
		#reportLangEn = ttk.Radiobutton(self, text="EN", value="en", variable=self.language)
		#reportLangEn.grid(column=4, row=rowNumber, padx=5, pady=5)
		#rowNumber += 1

		outputLocationName = ttk.Label(self, text="Output location")
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
		self.progressBar["maximum"] = 10000
		if DEBUG: print "GO"

		#if DEBUG: print "searchString: " + self.searchStringEntry.get()
		#if DEBUG: print "searchDirectory: " + self.searchDirectory
		#if DEBUG: print "outputLocation: " + self.outputLocation
		#if DEBUG: print "language: " + self.language.get()


		# Verification
		errors = []
		#if not self.searchStringEntry.get():
		#	errors.append("the string search")
		if not self.searchDirectory:
			errors.append("the search directory")
		if not self.outputLocation:
			errors.append("the output directory")
		#if not self.language.get():
		#	errors.append("the report language")

		if errors:
			message = "Please fill in the following fields:\n" + "\n".join(errors)
			tkMessageBox.showinfo("Error", message)
		else:
			results = []
			for root, _, files in walk(self.searchDirectory):
				for filename in files:
					filepath = path.join(root, filename).replace("\\","/")
					#retourne "None" si c'est pas une image
					filetype = imghdr.what(filepath)
					
					if filetype != "None":
						if DEBUG: print filetype
						if DEBUG: print "\n--------- " + filepath + " ----------"
						text, conf = parseTextFromImage(filepath)
						if text and conf:
							results.append([filepath, text, conf])
							if DEBUG: print "Confidence: ", conf
							if DEBUG: print unicode(text, errors='ignore')

			if DEBUG: print "Saving scan results..."
			#report = exportAsCSV(self.outputLocation, results)
			report = exportAsHTML(self.outputLocation, results)
			if DEBUG: print "REPORT: " + report
			if report:
				if DEBUG: print "Done."
				if tkMessageBox.askyesno("Success", "The indexation is done.\nDo you want to open the resulting report in your default browser?"):
					# on essai d'ouvrir le rapport
					try:
						system("start " + report)
					except:
						pass
			else:
				if DEBUG: print "Canceled."

		#self.increment()

	def increment(self):
		self.progressBar["value"] += 100
		#if DEBUG: print self.progressBar["value"] , self.progressBar["maximum"]
		if self.progressBar["value"] < self.progressBar["maximum"]:
			self.after(1, self.increment) 

	def bye(self):
		if DEBUG: print "bye"

app = GUI()
app.master.title('Inspektor')
#app.askdirectory(initialdir=".", title="Select directory to scan")
app.mainloop()