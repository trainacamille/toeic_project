import os
import tempfile
import cv2
from pdf2image import convert_from_path
import numpy as np
import aide

random=1

def pdfimg(nom,dossier):
    feuille_reponse=convert_from_path(nom,dpi=200)
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
    return pliste,carre

def detection_nom(img,i):
    #une image couleur
    imgray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imflou=cv2.GaussianBlur(imgray,(5,5),0)
    imcanny=cv2.Canny(imflou,50,90,(3,3))
    resultat=detectcarre(imcanny)
    #calibrage sur les bords  du nom 'le 3eme plus gros contour'
    cnt=resultat[2]
    ln=cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.02 * ln, True)
    approx=approx.reshape(4,2)
    approx=aide.order_points(approx)
    nom=img[approx[0][1]:approx[2][1],approx[0][0]:approx[2][0]]
    cv2.imwrite('nom'+str(i)+'.jpg',nom)

def detection_sections(img):
    #une image couleur
    imgray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imflou=cv2.GaussianBlur(imgray,(5,5),0)
    imcanny=cv2.Canny(imflou,50,90,(3,3))
    resultat=detectcarre(imcanny)
    sliste=[]
    for i in range(1,3):
        ln=cv2.arcLength(resultat[i], True)
        approx = cv2.approxPolyDP(resultat[i], 0.02 * ln, True)
        #Dans le listening ou le reading (les 2 premiers)
        approx=approx.reshape(4,2)
        approx=aide.order_points(approx)
        section=img[approx[0][1]:approx[2][1],approx[0][0]:approx[2][0]]
        sliste.append(section)
    #listening puis reading            
    return sliste

def detection_rep(img):
    imgray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imflou=cv2.GaussianBlur(imgray,(5,5),0)
    imcanny=cv2.Canny(imflou,50,90,(3,3))
    re,imseuil=cv2.threshold(imgray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    contours, hierarchy = cv2.findContours(imcanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    ctri=sorted(contours, key=cv2.contourArea, reverse=False)

    carre=[]
    for cnt in ctri:
        ln=cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * ln, True)
        if(len(approx)==4):
            (x, y, w, h) = cv2.boundingRect(cnt)
            ar = w / float(h)
            #si ca ressemble a un caré et que cest moyen (eviter les sections)
            if(w in range(20,50) and h in range(20,50) and ar >= 0.9 and ar <= 1.1):
                carre.append(cnt)

    return carre

if __name__ == "__main__":
    #creer un repertoire dans lequel seront enregistrés les documents nécessaires à la correction
    mon_dossier='correction'+str(random)
    os.mkdir(mon_dossier)
    #prendre le nom du fichier par la prof(ici statique) et le chemin créé 
    chemin='../TOEIC2.pdf'
    nb_pages=pdfimg(chemin,mon_dossier)

    #Commencer le traitement pour chacune des pages recensées
    for i in range(0,nb_pages+1):
        img=cv2.imread(mon_dossier+'/epreuve'+str(i)+'.jpg',cv2.IMREAD_COLOR)

        #Si on n'a pas eu l'image
        if(not img.data):
            print('Oups, ton image n\'existe pas dis-donc!')
            break
        #Detecter les contours pour la rotation
        #Pour cela appliquer le prétraitement de l'image et passer l'image traitée

        imgray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        contraste=cv2.convertScaleAbs(imgray,None,0.8,0)
        imflou=cv2.GaussianBlur(contraste,(5,5),0)
        imcanny=cv2.Canny(imflou,75,150,(3,3))
        
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
        dest=cv2.dilate(imcanny,kernel)
        coord_bords,cont_bords=detectbord(dest)

        if(len(coord_bords) != 5):
            print("Oups, je n'ai pas trouvé tous les points pour faire la bonne rotation")
            break
        else:
            #On a trouve nos 5 carrés du bord et on va chercher la bonne rotation
            angle_rot=aide.rotationimage(coord_bords,5)
            print(angle_rot)
            imrote=rotation(dest,angle_rot)
            cv2.imshow('Test',imrote)
            cv2.waitKey(0)
            cv2.destroyAllWindows()     

    os.rmdir(mon_dossier)



