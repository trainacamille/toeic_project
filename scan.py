import os
import cv2
from pdf2image import convert_from_path
import numpy as np
import aide
import json
import modeleexcel as ex

def pdfimg(nom,dossier):
    feuille_reponse=convert_from_path(nom,dpi=200,output_folder=dossier)
    for i,mat in enumerate(feuille_reponse):
        mat.save(os.path.join(dossier, 'epreuve'+str(i)+'.jpg'), 'JPEG')
    return i

def rotation(img,angle):
    rows, cols = img.shape[0], img.shape[1]
    rot=cv2.getRotationMatrix2D((cols / 2, rows / 2),angle,1)

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

def detectbord(img):
    #une image cany ou tresh
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ctri=sorted(contours, key=cv2.contourArea, reverse=True)
    carre=[]
    pliste=[]
    for cnt in ctri:
        ln=cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * ln, True)
        if(len(approx)==4):
            (x, y, w, h) = cv2.boundingRect(cnt)
            #si ca ressemble a un carré et que cest moyen (eviter les sections)
            if(w in range(20,50) and h in range(20,50)):
                #cv2.drawContours(image, [cnt], -1, (255,0,0), 2)
                carre.append(cnt)
                (tl, tr, br, bl)=aide.order_points(approx.reshape(4,2))   
                pliste.append((tr[0],tr[1]))
    #maintenant on veut retourner les coordonnées de ces points pour trouver l'ordre de rotation
    #ains que la liste des contours qui nous servira pour le zoom sur les bords
    #(c'est inutile de renvoyer carre car orderpoint fait le travail)
    return pliste,carre

#Pour des raisons d'amelioration, l'ancienne
#methode de detection des bords est abandonnée, on utilisera celle ci
def detecterbord(img,minp=850):
    #une image niveau de gris que je mets en tresh
    _,imseuil=cv2.threshold(img,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    #une ouverture de l'image seuillee pour reduire les possibilites
    noyeau = np.ones((3,3),np.uint8)
    resultat=cv2.morphologyEx(imseuil, cv2.MORPH_OPEN, noyeau)

    #On cherche les composants connexes
    retval, labels, stats, centroids=cv2.connectedComponentsWithStatsWithAlgorithm(	resultat, 4, cv2. CV_32S,cv2.CCL_WU)
    #minp peu varier(de 50) en fonction du nombre de contour trouvé(une amelioration)
    pliste=[]
    for i in range (1,retval):
        #On sait que les carrés du bord sont remplis en pixels(etudier le retour de stats)
        if(stats[i,4]>minp):
            if (stats[i,2] in range(20,50) and stats[i,3] in range(20,50)):
                tr=(stats[i,0]+stats[i,2],stats[i,1])
                pliste.append(tr)
    nb=0
    #pour eviter la boucle en montant et en descandant,on fixe à 7(arbitraire)
    # le max d'iterration
    while nb<7:
        if(len(pliste)==5):
            break
        elif(len(pliste)<5):
            #on diminue minp
            minp-=100
            nb+=1
        elif(len(pliste)>5):
            #on augmente minp
            minp+=100
            nb+=1
        #On refait le traitement (c'est nécessaire pour avoir les 5 carrés pour la rotation)
        pliste=[]
        for i in range (1,retval):
            if (stats[i,2] in range(20,50) and stats[i,3] in range(20,50)):
                if(stats[i,4]>minp):
                    tr=(stats[i,0]+stats[i,2],stats[i,1])
                    pliste.append(tr)
    
    return pliste    

def extraction_nom(img,i,contours,mon_dossier='correction'):
    #une image couleur    
    for cnt in contours:
        ln=cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * ln, True)
        if(len(approx)==4):
            (x, y, w, h) = cv2.boundingRect(cnt)
            #essayer de detecter le nom
            if(w in range(720,791) and h in range(160,201)):
                approx=approx.reshape(4,2)
                approx=aide.order_points(approx)
                nom=img[int(approx[0][1]):int(approx[2][1]),int(approx[0][0]):int(approx[2][0])]
                cv2.imwrite(mon_dossier+'/nom'+str(i)+'.jpg',nom)
                #Seul un contour aurait cette taille.
                return mon_dossier+'/nom'+str(i)+'.jpg'
    return None

def detection_sections(img,contours):
    sliste=[]
    for cnt in contours:
        ln=cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * ln, True)
        if(len(approx)==4):
            (x, y, w, h) = cv2.boundingRect(cnt)
            #detecter les sections
            if(w in range(975,1150) and h in range(975,1150)):
                approx=approx.reshape(4,2)
                approx=aide.order_points(approx)
                section=img[int(approx[0][1]):int(approx[2][1]),int(approx[0][0]):int(approx[2][0])]
                sliste.append(section)
    #listening puis reading            
    return sliste

def moyenne(liste):
    somme=0
    max=-1
    for i in range(0,len(liste)):
        somme+=liste[i]
    return somme/len(liste)

def bonne_reponse(liste):
    nb=0
    ln=[]
    mean=moyenne(liste)*1.15
    for u in range(0,len(liste)):
        if(liste[u]>mean ):
            rp = u+1
            nb+=1
            ln.append(liste[u])
    if nb==1:
        return rp
    elif nb>1:
        #augmenter le seuil pour les doubles reponses
        nb=0
        mean=moyenne(liste)*1.25
        for u in range(0,len(ln)):
            if(ln[u]>mean ):
                rp = u+1
                nb+=1
        if nb==1:
            return rp
    return -1


def correction_fine(image,n):
    #prend l'image en imseuil et décale pour sauter les num questions et les bords du haut
    largeur=image.shape[1]
    hauteur=image.shape[0]-4
    #n = 5 pour le listening et 4 pour le reading(a cause de la longueur des questions)
    depart_x=int(largeur/n)+1
    img=image[7:hauteur,depart_x:largeur]
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
    return bonne_reponse(proposition)

def recuperer_reponse(chemin):
    with open(chemin) as json_data:
        reponses = json.load(json_data)
        listening_r=reponses["Listening"][0]
        reading_r=reponses["Reading"][0]
    return listening_r,reading_r

def division_image(partie):
    hauteur=partie.shape[0]
    largeur=partie.shape[1]
    pas=int(largeur/4)-5
    questionsl=[]
    bloc=0
    for i in range (0,4):
        questionsl.append(partie[0:hauteur,bloc:bloc+pas])
        bloc+=pas

    blocl=[]
    pas=int(hauteur/25)-3
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
            choix.append(possibilite)
    return choix,seuillage  

def detection_rep(choix,seuillage,part_r,n):
    reponses_etud=[]
    score=0
    #1- on descend dans chacune des questions (choix)
    for e,quest in enumerate(choix):
        rponses=[]
        #parce que ça génere des probleme sinon
        if(len(quest)>2):
            quest=aide.sort_contours(quest)[0]
        #Gestion erreur pas pu avoir toutes les questions exactement
        if(len(quest)!=4):
            reponse=correction_fine(seuillage[e],n)
            #print(e+1, reponse)
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
            """if(bonne_reponse(rponses)==-1):
                print(e+1,rponses)"""
        #Pour finir on Corrige
        reponses_etud.append(reponse)
        #print("Reponse question "+ str(e+1)+": "+str(reponse) +" bonne reponse: "+str(part_r[str(e)]) ) 
        if(n==5):
            if reponse==part_r[str(e)]:
                score+=1
        elif n==4:
            if reponse==part_r[str(e+100)]:
                score+=1
    return score,reponses_etud

