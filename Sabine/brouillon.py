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


#cv2.namedWindow('Gray', cv2.WINDOW_NORMAL)
cv2.namedWindow('Contours', cv2.WINDOW_NORMAL)
cv2.namedWindow('Canny', cv2.WINDOW_NORMAL)
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
#image=img.copy()

imflou=cv2.GaussianBlur(rotation,(5,5),0)
imgray=cv2.cvtColor(imflou,cv2.COLOR_BGR2GRAY)
imcanny=cv2.Canny(imflou,50,90,(3,3))
re,imseuil=cv2.threshold(imgray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

contours, hierarchy = cv2.findContours(imcanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

ctri=sorted(contours, key=cv2.contourArea, reverse=False)
pliste=[]
for i,cnt in enumerate(ctri):
    ln=cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.02 * ln, True)
    
    #calibrage sur les bords
    if(len(approx)==4 and cv2.contourArea(cnt) > 1000.0 and cv2.contourArea(cnt)< 1200.0 ):
        (tl, tr, br, bl)=aide.order_points(approx.reshape(4,2))   
        pliste.append((tr[0],tr[1]))
        cv2.drawContours(image, [cnt], -1, (0,255,0), 2)
#rec=aide.order_points(np.array(pliste))
#paper=aide.four_point_transform(image,rec)
cv2.imshow('Canny',image)
#cv2.imshow('Gray',expe)
#cv2.imshow('Contours',paper)


cv2.waitKey(0)
cv2.destroyAllWindows()
