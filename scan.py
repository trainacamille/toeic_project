import os
import tempfile
import cv2
from pdf2image import convert_from_path
import numpy as np
import aide

def pdfimg():
    feuille_reponse=convert_from_path('../Scan Couleur.pdf',dpi=200)
    for i,mat in enumerate(feuille_reponse):
        mat.save(os.path.join('E:\\ING2\\Projet\\Code', 'feuille'+str(i)+'.jpg'), 'JPEG')
    return i

def rotation(img):
    rows, cols = img.shape[0], img.shape[1]
    rot=cv2.getRotationMatrix2D((cols / 2, rows / 2),90,1)

    (cX, cY) = (cols // 2, rows // 2)
    cos = np.abs(rot[0, 0])
    sin = np.abs(rot[0, 1])
    # compute the new bounding dimensions of the image
    nW = int((rows * sin) + (cols * cos))
    nH = int((rows * cos) + (cols * sin))
    # adjust the rotation matrix to take into account translation
    rot[0, 2] += (nW / 2) - cX
    rot[1, 2] += (nH / 2) - cY

    return cv2.warpAffine(img,rot,(nW,nH))

def detection_nom(img,i):
    "possibilité de passer l'image propre"
    imflou=cv2.GaussianBlur(img,(5,5),0)
    imgray=cv2.cvtColor(imflou,cv2.COLOR_BGR2GRAY)
    imcanny=cv2.Canny(imflou,50,90,(3,3))
    contours, hierarchy = cv2.findContours(imcanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ctri=sorted(contours, key=cv2.contourArea, reverse=False)
    for i,cnt in enumerate(ctri):
        ln=cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * ln, True) 
        #calibrage sur les bords  du nom
        if(len(approx)==4 and cv2.contourArea(cnt) > 100000.0 and cv2.contourArea(cnt)< 500000.0):  
            approx=approx.reshape(4,2)
            approx=aide.order_points(approx)
            nom=img[approx[0][1]:approx[2][1],approx[0][0]:approx[2][0]]
            cv2.imwrite('nom'+str(i)+'.jpg',nom) 
            break

def detection_sections(img):
    imflou=cv2.GaussianBlur(img,(5,5),0)
    imgray=cv2.cvtColor(imflou,cv2.COLOR_BGR2GRAY)
    imcanny=cv2.Canny(imflou,50,90,(3,3))
    contours, hierarchy = cv2.findContours(imcanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ctri=sorted(contours, key=cv2.contourArea, reverse=False)
    sliste=[]
    for i,cnt in enumerate(ctri):
        ln=cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * ln, True)
        #Dans le listening ou le reading
        if(len(approx)==4 and cv2.contourArea(cnt) > 1000000.0 and cv2.contourArea(cnt)< 2500000.0):
            approx=approx.reshape(4,2)
            approx=aide.order_points(approx)
            section=img[approx[0][1]:approx[2][1],approx[0][0]:approx[2][0]]
            sliste.append(section)
    #listening puis reading            
    return sliste;