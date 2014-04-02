import cv2.cv as cv
import tesseract
import os.path
import re
import numpy.core.multiarray # pour que PyInstaller aille chercher numpy pour que tesseract fonctionne
from PIL import Image

def parseTextFromImage( filepath ):
	api = tesseract.TessBaseAPI()
	api.Init("OCR", "eng", tesseract.OEM_DEFAULT) # le filepath du tessdata, a partir du root/main de l'application
	api.SetPageSegMode(tesseract.PSM_AUTO)

	try:
		text = ""
		conf = 0
		# if file is GIF, use PIL to parse each frame
		if re.match("([^\\s]+(\\.(?i)(gif))$)", filepath, re.I):
			tmpFile = "tmp001.png"
			frame = Image.open(filepath)
			i = 0
			while frame:
				frame.save(tmpFile, 'PNG')
				
				# on passe le frame dans tesseract
				image = cv.LoadImage(tmpFile, cv.CV_LOAD_IMAGE_GRAYSCALE)
				tesseract.SetCvImage(image, api)
				text += api.GetUTF8Text() + "\n"
				
				# on garde la confidence maximale d'un frame
				if api.MeanTextConf() > conf:
					conf = api.MeanTextConf()
					
				i += 1
				try:
					frame.seek(i)
				except EOFError:
					break # fin du gif
					
			# on delete le fichier temporaire
			try:
				os.remove(tmpFile)
			except OSError:
				pass
				
			# on retourne le texte si ne contient pas seulement des whitespace characters
			if re.match("^\\s*$", text, re.I):
				return None, None
			else:
				return text, conf

		else:
			# on envoi directement l'image a tesseract
			image = cv.LoadImage(filepath, cv.CV_LOAD_IMAGE_GRAYSCALE)
			tesseract.SetCvImage(image, api)
			text = api.GetUTF8Text()
			conf = api.MeanTextConf()
			# on retourne le texte si ne contient pas seulement des whitespace characters
			if re.match("^\\s*$", text, re.I):
				return None, None
			else:
				return text, conf
			
	except IOError:
		print "Error reading file " + filepath
		return None, None