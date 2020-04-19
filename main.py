import application
import application_aide
import sys
import cv2
import os
import json
import pdf2image
#from pdf2image import convert_from_path
import numpy as np
import openpyxl


#Lancementde l'application
app = application.Application()
exit_status3 = app.run(sys.argv)
sys.exit(exit_status3)
