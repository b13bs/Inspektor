import cv2.cv as cv
import tesseract
import sys

def parseTextFromImage( path ):
	api = tesseract.TessBaseAPI();
	api.Init("OCR", "eng", tesseract.OEM_DEFAULT); # le path du tessdata, a partir du root/main de l'application
	api.SetPageSegMode(tesseract.PSM_AUTO);

	image = cv.LoadImage( path, cv.CV_LOAD_IMAGE_GRAYSCALE);
	tesseract.SetCvImage(image, api);
	text = api.GetUTF8Text();
	conf = api.MeanTextConf();
	return text, conf;
	