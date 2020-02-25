import os
import tempfile
import cv2
import numpy as np

import aide

#1-convertion de pdf en images

"""from pdf2image import convert_from_path

feuille_reponse=convert_from_path('../AnswerSheet_v.pdf',dpi=200)

for i,mat in enumerate(feuille_reponse):
    mat.save(os.path.join('E:\\ING2\\Projet\\Code', 'expe'+str(i)+'.jpg'), 'JPEG')"""

#2-detection de contours

"""
1- Rendre l'image en Niveau de Gris
2-Appliquer un flou Gaussien pour éliminer les bruits
4-Appliquer un seuillage(seuillage OTSU le meilleur)

3-Faire un Canny Edge //utiliser le canny automatique de imutils pourquoi pas(car difficile de trouver le bon seuil)
5-Detecter les contours
"""


cv2.namedWindow('Gray', cv2.WINDOW_NORMAL)
cv2.namedWindow('Contours', cv2.WINDOW_NORMAL)
#cv2.namedWindow('Canny', cv2.WINDOW_NORMAL)
#cv2.namedWindow('lumi', cv2.WINDOW_NORMAL)

img=cv2.imread("../test0.jpg",cv2.IMREAD_COLOR)

"""tourner de paysage en portrait"""
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

rotation=cv2.warpAffine(img,rot,(nW,nH))
image=rotation.copy()
imm=rotation.copy()


imflou=cv2.GaussianBlur(rotation,(5,5),0)
imgray=cv2.cvtColor(imflou,cv2.COLOR_BGR2GRAY)
imcanny=cv2.Canny(imgray,50,90,(3,3))
re,imseuil=cv2.threshold(imgray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#external detecter les grandes lignes
contours, hierarchy = cv2.findContours(imcanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

ctri=sorted(contours, key=cv2.contourArea, reverse=False)
sliste=[]
"""for i,cnt in enumerate(ctri):
    ln=cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.02 * ln, True) 
    #print(cv2.contourArea(approx)) 
    #calibrage sur les bords  du nom
    if(len(approx)==4 and cv2.contourArea(cnt) > 100000.0 and cv2.contourArea(cnt)< 500000.0): 
        #print(cv2.contourArea(approx))  
        cv2.drawContours(imm, [cnt], -1, (0,255,0), 2)
        #print(approx.reshape(4,2))
        approx=approx.reshape(4,2)
        approx=aide.order_points(approx)
        #print(approx[0][1],approx[2][1],approx[0][0],approx[2][0])
        approx=approx.reshape(4,2)
        nom=image[approx[0][1]:approx[2][1],approx[0][0]:approx[2][0]]
        #cv2.imwrite('nom'+str(i)+'.jpg',nom)
        break"""

#detection des reponses
#cv2.drawContours(imm, contours, -1, (255,0,0), 2)
for i,cnt in enumerate(ctri):
    ln=cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.02 * ln, True)
    #Dans le listening ou le reading
    if(len(approx)==4 and cv2.contourArea(cnt) > 1000000.0 and cv2.contourArea(cnt)< 2500000.0):
        approx=approx.reshape(4,2)
        approx=aide.order_points(approx)
        section=image[approx[0][1]:approx[2][1],approx[0][0]:approx[2][0]]
        sliste.append(section)
        cv2.drawContours(imm, [cnt], -1, (255,0,0), 2)


imfl=cv2.GaussianBlur(sliste[0],(5,5),0)
imgry=cv2.cvtColor(imfl,cv2.COLOR_BGR2GRAY)
imcany=cv2.Canny(imgry,50,90,(3,3))
contours, hierarchy = cv2.findContours(imcany, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
questionCnts = []
# loop over the contours
for c in contours:
    (x, y, w, h) = cv2.boundingRect(c)
    #ar = w / float(h)
    #and ar >= 0.9 and ar <= 1.1
    if (w >= 35 and h >= 35 ):
        questionCnts.append(c)
        cv2.drawContours(sliste[0], [c], -1, (0,0,255), 2)

#cv2.imwrite('contours.jpg',image)

print (len(questionCnts))

for i in range(0,len(sliste)):
    cv2.namedWindow('Section'+str(i),cv2.WINDOW_NORMAL)
    cv2.imshow('Section'+str(i),sliste[i])

#cv2.imshow('Canny',image)
cv2.imshow('Gray',imm)
cv2.imshow('Contours',imseuil)


cv2.waitKey(0)
cv2.destroyAllWindows()
