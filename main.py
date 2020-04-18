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



app = application.Application()
#app2 = application_aide.Application("qccm.png",198)
#app3 = application_aide.Application("qccm.png",199)
#exit_status = app2.run(sys.argv)
#exit_status2 = app3.run(sys.argv)
exit_status3 = app.run(sys.argv)
#sys.exit(exit_status)
#sys.exit(exit_status2)
sys.exit(exit_status3)
