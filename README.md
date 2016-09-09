Inspektor
=========

Description
-----------
Harvest media looking for images containing text and parse it. Those images are analyzed with an optical caracter recognition engine. The results from the text image are presented in report and searchable with regular expression or with fuzzy string search.


Portable version
----------------
The program is multi-platform because it uses Python scripting language and Web technologies. However, there is a Windows portable executable released: https://github.com/b13bs/Inspektor/tree/master/Release

If the program stops working on Windows, try in compatibility mode Windows XP SP3.


Dependencies
-----------
 - Python 2.7
 - python-tesseract
 - opencv-python
 - numpy
 - PIL (Python Image Library)

On Windows, add "C:\Python27" to your PATH.


Additionnal informations
------------
To create the Windows PE file, we used PyInstaller: https://github.com/pyinstaller/pyinstaller
