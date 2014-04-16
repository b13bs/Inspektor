Inspektor
=========

Description
-----------
Logiciel qui inspecte un média à la recherche d'images contenant du texte. Les images sont analysés avec un engin de reconnaissance optique de caractères. Le programme génère un rapport avec les résultats trouvés qui est portable et recherchable (expression régulière, approximative/fuzzy).

Version portable
----------------
Dernière version executable portable pour windows : https://github.com/EtiDuc/Inspektor/blob/master/Release/Inspektor_win32.zip
Aucune dépendance ne devrait être requise

Dépendances
-----------
 - Python 2.7
 - python-tesseract
 - opencv-python
 - numpy
 - PIL (Python Image Library)

Ne pas oublier de mettre C:\Python27 dans votre PATH!

Autres infos
------------
Pour créer la version portable nous utilisons PyInstaller : https://github.com/pyinstaller/pyinstaller
