import os
import tempfile
import cv2
import numpy as np
import json

import aide

def moyenne(liste):
    somme=0
    max=-1
    for i in range(0,len(liste)):
        somme+=liste[i]
    return somme/len(liste)

def bonne_reponse(liste):
    nb=0
    mean=moyenne(liste)*1.25
    for u in range(0,len(liste)):
        if(liste[u]>mean ):
            rp = u+1
            nb+=1
    if nb!=1:
        return -1
    else:
        return rp

def correction_fine(image,i):
    #prend l'image en imseuil et décale pour sauter les num questions et les bords du haut
    largeur=image.shape[1]
    hauteur=image.shape[0]
    depart_x=int(largeur/4)+1
    img=image[7:hauteur,depart_x:largeur]
    #cv2.imshow('win'+str(i),img)
    #la diviser en 4
    nv_h=img.shape[0]
    nv_l=img.shape[1]
    proposition=[]
    pas=int(nv_l/4)
    bloc=0
    for i in range(0,4):
        prop=img[0:nv_h,bloc:bloc+pas]
        bloc+=pas
        total = cv2.countNonZero(prop)
        proposition.append(total)
        #print(i, total)
    return bonne_reponse(proposition)

"""from pdf2image import convert_from_path

feuille_reponse=convert_from_path('../TOEIC2.pdf',dpi=200)

for i,mat in enumerate(feuille_reponse):
    mat.save(os.path.join('E:\\ING2\\Projet\\Code', 'scan'+str(i)+'.jpg'), 'JPEG')
"""
img=cv2.imread("../test1.jpg",cv2.IMREAD_COLOR)

#rotation 90
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
#fin rotation
###############################################################################################


########################Lecture json#################################################
########################Lecture json#######################################################
###########################################################################################
with open('../reponses.json') as json_data:
    reponses = json.load(json_data)
    listening_r=reponses["Listening"][0]
    reading_r=reponses["Reading"][0]


#OKOK################################################""



#(les valeurs sont données en fonction de notre feuille)

image=rotation.copy()
imm=rotation.copy()
#rotation=cv2.fastNlMeansDenoisingColored(image,None,10,10,7,21)

imgray=cv2.cvtColor(rotation,cv2.COLOR_BGR2GRAY)
contraste=cv2.convertScaleAbs(imgray,None,0.8,0)
imflou=cv2.GaussianBlur(contraste,(5,5),0)


imcanny=cv2.Canny(imflou,75,150,(3,3))
#detection bords et nom (sur contour canny)

#seuil =  cv2.adaptiveThreshold(imflou, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 4)

#re,imseuil=cv2.threshold(imflou,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
dest=cv2.dilate(imcanny,kernel)

#erode=cv2.erode(imseuil, kernel)
contours, hierarchy = cv2.findContours(dest, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

ctri=sorted(contours, key=cv2.contourArea, reverse=False)

colors=[(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255)]

carre=[]
sliste=[]
for cnt in ctri:
    ln=cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.02 * ln, True)
    if(len(approx)==4):
        (x, y, w, h) = cv2.boundingRect(cnt)
        #si ca ressemble a un carré et que cest moyen (eviter les sections)
        if(w in range(20,50) and h in range(20,50)):
            #cv2.drawContours(image, [cnt], -1, (255,0,0), 2)
            carre.append(cnt)

#dessin juste pour moi dans les tests
cont=aide.sort_contours(carre)[0]


for i,q in enumerate(cont):
    cv2.drawContours(image, [q], -1, colors[i], 5)

"""Reorganisation de la feuille pour zoom"""
pliste=[]
for i,cnt in enumerate(cont):
    if (i!=2):
        ln=cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * ln, True)
        (tl, tr, br, bl)=aide.order_points(approx.reshape(4,2))   
        pliste.append((tr[0],tr[1]))  
rec=aide.order_points(np.array(pliste))
paper=aide.four_point_transform(imflou,rec)    
papier=aide.four_point_transform(imm,rec) 
pcany=aide.four_point_transform(imcanny,rec)
#pseuil=aide.four_point_transform(imseuil,rec)
pdest=aide.four_point_transform(dest,rec)
#perode=aide.four_point_transform(erode,rec)
pcol=papier.copy()

"""maintenant les grandes sections et le nom"""

contours, hierarchy = cv2.findContours(pdest, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
ctri=sorted(contours, key=cv2.contourArea, reverse=False)

for cnt in ctri:
    ln=cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.02 * ln, True)
    if(len(approx)==4):
        (x, y, w, h) = cv2.boundingRect(cnt)
        #essayer de detecter le nom
        if(w in range(720,791) and h in range(160,201)):
            cv2.drawContours(papier, [cnt], -1, (13,133,165), 5)
            print("ok")
        #detecter les sections(diviser la feuille en deux car chaque crop reduit la qualité de limage)
        if(w in range(975,1150) and h in range(975,1150)):
            print("ok")
            approx=approx.reshape(4,2)
            approx=aide.order_points(approx)
            section=paper[int(approx[0][1]):int(approx[2][1]),int(approx[0][0]):int(approx[2][0])]
            sliste.append(section)
            cv2.drawContours(papier, [cnt], -1, (227,10,241), 5) 

#fin detec bord et nom
###########################################################################################
###########################################################################################
###########################################################################################

print(paper.shape)

hauteur=paper.shape[0]
largeur=paper.shape[1]
listening=paper[0:hauteur,0:int(largeur/2)]
reading=paper[0:hauteur,int(largeur/2):largeur]

##################################################
###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################

part1=sliste[0].copy()
part2=sliste[1].copy()
hauteur=part2.shape[0]
largeur=part2.shape[1]

pas=int(largeur/4)-5

questionsl=[]
#pas=int(largeur/4)-3
bloc=0
for i in range (0,4):
    questionsl.append(part2[0:hauteur,bloc:bloc+pas])
    bloc+=pas
"""    
if (len(questionsl)!=0):
    for i in range(0,len(questionsl)):
        cv2.namedWindow('Bloc'+str(i),cv2.WINDOW_AUTOSIZE)
        cv2.imshow('Bloc'+str(i),questionsl[i])"""
blocl=[]

pas=int(hauteur/25)-3
pasl=int(hauteur/25)-3

for i in range(0,len(questionsl)):    
    depart=int(hauteur/16)+5
    hb=questionsl[i].shape[0]
    lb=questionsl[i].shape[1]
    for j in range(0,25):
        blocl.append(questionsl[i][depart:depart+pas,0:lb])
        depart=depart+pas

choix=[]

seuillage=[]
if (len(blocl)!=0 ):
    for i in range(0,len(blocl)):
        possibilite=[]
        question=blocl[i]
        re,imseuil=cv2.threshold(question,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        seuillage.append(imseuil)
        contours, hierarchy = cv2.findContours(imseuil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            (x, y, w, h) = cv2.boundingRect(c)
            if (w >= 24 and h >= 24):
                possibilite.append(c)
                cv2.drawContours(question, [c], -1, (255), 2)        
        choix.append(possibilite)  

print("La longueur est "+str(len(choix)))
"""
if (len(blocl)!=0 and len(blocl)>=11):
    for i in range(0, 12):
        cv2.namedWindow('Question'+str(i),cv2.WINDOW_AUTOSIZE)
        cv2.imshow('Question'+str(i),blocl[i])"""

#####################################################################################
#                #""" Corection   """
# Correction 'A la main'
##################################################################################   
score_r=0
score_l=0
#1- on descend dans chacune des questions (choix)
for e,quest in enumerate(choix):
    rponses=[]
    if(len(quest)>2):
        quest=aide.sort_contours(quest)[0]
    #Gestion erreur pas pu avoir toutes les questions exactement
    if(len(quest)!=4):
        #cv2.imshow('Question'+str(e+1),blocl[e])
        #cv2.imshow('Seuillage'+str(e+1),seuillage[e])
        print("Erreur a la question "+str(e+1)+" correction fine utilisée")
        reponse=correction_fine(seuillage[e],e+1)
        print(e+1, reponse)
        #definir le traitement à faire(en fonction de la vue)
        #pour le moment un 0 automatique
    #2-pour chaque question on boucle sur les 4 possibilités
    else:
        for j,c in enumerate(quest):
            mask=np.zeros(seuillage[e].shape,dtype=np.uint8)
            cv2.drawContours(mask, [c], -1, 255, -1)
            #Pour chaque possibilité compter la valeur
            mask = cv2.bitwise_and(seuillage[e], seuillage[e], mask=mask)
            total = cv2.countNonZero(mask)

            #On met a jour le total
            rponses.append(total)
        reponse=bonne_reponse(rponses)
    #print("Reponse question "+ str(e+1)+": "+str(reponse) +" total: "+str(total) )
    #Pour finir on Corrige
    #print("Reponse question "+ str(e+1)+": "+str(reponse) +" bonne reponse: "+str(reading_r[str(e+100)]) ) 
    if reponse==listening_r[str(e)]:
        score_r+=1
        #print(rponses)
print("Ton résultat est "+str(score_r))


####################################################


########################Correspondance grille toeic#################################################
########################Correspondance grille toeic#######################################################
###########################################################################################

resultat={"0":5,"1":5,"2":5,"3":5,"4":5,"5":5,"6":5,"7":10}



#cv2.namedWindow('Gray', cv2.WINDOW_NORMAL)
#cv2.namedWindow('Contours', cv2.WINDOW_NORMAL)
cv2.namedWindow('Canny', cv2.WINDOW_NORMAL)
#cv2.namedWindow('lumi', cv2.WINDOW_NORMAL)
cv2.imshow('Canny',papier)
#cv2.imshow('Gray',sliste[1])
#cv2.imshow('Contours',sliste[0])


cv2.waitKey(0)
cv2.destroyAllWindows()            

