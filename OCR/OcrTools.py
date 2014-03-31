import cv2.cv as cv
import tesseract
import sys
import os
import re
from PIL import Image

def parseTextFromImage( path ):
	api = tesseract.TessBaseAPI()
	api.Init("OCR", "eng", tesseract.OEM_DEFAULT) # le path du tessdata, a partir du root/main de l'application
	api.SetPageSegMode(tesseract.PSM_AUTO)

	text = ""
	conf = 0
	if re.match("([^\\s]+(\\.(?i)(gif))$)", path, re.I):
		tmpFile = "tmp001.png"
		frame = Image.open(path)
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
			
		# on retourne le resultat
		return text, conf
	else:
		# on envoi directement l'image a tesseract
		image = cv.LoadImage(path, cv.CV_LOAD_IMAGE_GRAYSCALE)
		tesseract.SetCvImage(image, api)
		text = api.GetUTF8Text()
		conf = api.MeanTextConf()
		return text, conf