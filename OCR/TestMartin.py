import os
import re
from OcrTools import parseTextFromImage

directory = "TestFolder";

for filename in os.listdir(directory):
	if re.match("([^\\s]+(\\.(?i)(jpg|png|gif|bmp))$)", filename, re.I):
		print "\n--------- " + directory + "/" + filename + " ----------"
		text, conf = parseTextFromImage(directory + "/" + filename);
		print "Confidence: ", conf
		print unicode(text, errors='ignore')
