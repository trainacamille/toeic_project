import shutil
import Application_vue
import sys

import numpy as np
import scan
import os
import cv2
import aide
import modeleexcel as ex

class Model(object):

    def telecharger(x,path):
        #attention ici en 1er argument ilfaudra mettre le chemin relatif du pdf
        shutil.copy("feuille_vierge/AnswerSheet_v.pdf",path)

    def enregist(x,nom):
        enr = Application_vue.Application(nom)
        exit = enr.run(sys.argv)

    def corriger(x,nom,path):
        nom='JSON/'+nom+'.json'
        #pour chaque pdf du dossier
        listening_r,reading_r=scan.recuperer_reponse(nom)
        #on parcours tous les fichiers du domaine
        for fichier in os.listdir(path):
            if fichier.endswith('.pdf'):        
                #creer un repertoire dans lequel seront enregistrés les documents nécessaires à la correction
                mon_dossier='correction'
                #Si le dossier existe on le supprime avant de le (re)creer
                if os.path.exists(mon_dossier):
                    os.system("rmdir "+mon_dossier+"/S/Q")
    
                os.mkdir(mon_dossier)
                #prendre le nom du fichier par la prof(ici statique) et le chemin créé 
                try:
                    nb_pages=scan.pdfimg(path+'/'+fichier,mon_dossier)
                except:
                    name=fichier.split('.')
                    ex.excel_final(path+"/"+name[0]+".xlsx",[],[],[],[(fichier,'Une erreur est survenue lors de la lecture')])
                    continue
                    #print("Pb rencontre lors de la lecture du fichier "+ fichier)

                #Commencer le traitement pour chacune des pages recensées
                reponses_fichier=[]
                noms_fichier=[]
                score_fichier=[]
                liste_erreurs=[]
                
                for i in range(0,nb_pages+1):
                    reponses_etud=[]
                    img=cv2.imread(mon_dossier+'/epreuve'+str(i)+'.jpg',cv2.IMREAD_COLOR)

                    #Si on n'a pas eu l'image
                    if(img is None):
                        liste_erreurs.append(('feuille '+str(i),"L'image associée à cette feuille n'a pas été trouvé"))
                        continue
                    #Detecter les contours pour la rotation
                    #Pour cela appliquer le prétraitement de l'image et passer l'image traitée

                    #La ligne commentee ci dessous permet de nettoyer une image trop bruitee
                    # img = cv2.fastNlMeansDenoisingColored(img,None,15,10,7,21)

                    imgray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    #plus besojn du contraste avec les composantes connexes
                    #contraste=cv2.convertScaleAbs(imgray,None,0.8,0)
                    #imflou=cv2.GaussianBlur(contraste,(5,5),0)
                    
                    imflou=cv2.GaussianBlur(imgray,(5,5),0)
                    imcanny=cv2.Canny(imflou,75,150,(3,3))

                    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
                    dest=cv2.dilate(imcanny,kernel)


                    try:
                        #coord_bords,cont_bords=scan.detectbord(dest)
                        coord_bords=scan.detecterbord(imgray)

                        if(len(coord_bords) != 5):
                            #On essaye de detecter les bords avec la 2eme methode
                            coord_bords,cont_bords=scan.detectbord(dest)
                            if(len(coord_bords) != 5):
                                liste_erreurs.append(('feuille '+str(i),"Les bords de la feuilles n'ont pas été trouvés, essayez un meilleur scan"))
                                #angle_rot=-90
                                continue
                        #On a trouve nos 5 carrés du bord et on va chercher la bonne rotation

                        #Penser à l'écart pour une efficacité
                        #l'écart dépend de l'alignement des points

                        angle_rot=aide.rotationimage(coord_bords,80)
                        """#cette partie etait pour les copies de l3 a 4 carres
                        if(len(coord_bords) == 5):
                            #l'écart dépend de l'alignement des points
                            angle_rot=-90"""
                        imrote=scan.rotation(dest,angle_rot)
                        imflou=scan.rotation(imflou,angle_rot)
                        couleur=scan.rotation(img,angle_rot)
                        imgray=scan.rotation(imgray,angle_rot)

                        #Apres rotation, on redétecte les bords sur l'image pour la remetre droite
                        #si elle était de travers

                        #(peut etre cette partie est-elle inutile mais on verra)

                        #coord_bords,cont_bords=scan.detectbord(imrote)
                        coord_bords=scan.detecterbord(imgray)
                        if(len(coord_bords) < 4):
                            #On essaye d'appeler la fonction de detection de bord qui utilise les contours
                            coord_bords,cont_bords=scan.detectbord(imrote)
                            if(len(coord_bords)<4):
                                #si malgré ça on n'a pas de solution on abandonne
                                liste_erreurs.append(('feuille '+str(i+1),'Impossible de bien cadrer la feuille pour la correction, essayez un meilleur scan'))
                                continue
                        #Les parties commentées sont de l'ancienne version
                        """cont=aide.sort_contours(cont_bords)[0]
                        pliste=[]
                        for u,cnt in enumerate(cont):
                            #on a etudie la feuille et on sait que le repere au milieu est le 3eme point
                            #on veut le sauter pour calibrer sur les bords
                            if (u!=2):
                                ln=cv2.arcLength(cnt, True)
                                approx = cv2.approxPolyDP(cnt, 0.02 * ln, True)
                                (tl, tr, br, bl)=aide.order_points(approx.reshape(4,2))   
                                pliste.append((tr[0],tr[1]))  
                        rec=aide.order_points(np.array(pliste))"""
                        #On veut remettre la feuille a l'endroit
                        rec=np.array(coord_bords)
                        paper=aide.four_point_transform(imflou,rec)
                        pdest=aide.four_point_transform(imrote,rec)
                        papier=aide.four_point_transform(couleur,rec)

                        #On s'attaque au nom et au listening/reading
                        contours, hierarchy = cv2.findContours(pdest, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                        ctri=sorted(contours, key=cv2.contourArea, reverse=False)
                        chemin=scan.extraction_nom(papier,i,ctri)
                        parties=scan.detection_sections(paper,ctri)

                        if(len(parties)!=2):
                            #Si on n'a pas trouvé les 2 parties distinctement
                            #On refait le traitement en augmentant le noyau
                            #le but etant d'augmenter la dilatation pour fermer le carres
                            val=5
                            ok=False
                            while val<11:
                                val+=2
                                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (val,val))
                                dest=cv2.dilate(imcanny,kernel)
                                imrote=scan.rotation(dest,angle_rot)
                                pdest=aide.four_point_transform(imrote,rec)
                                contours, hierarchy = cv2.findContours(pdest, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                                ctri=sorted(contours, key=cv2.contourArea, reverse=False)
                                parties=scan.detection_sections(paper,ctri)
                                if(len(parties)==2):
                                    ok=True
                                    break
                                else:
                                    pass 
                            if not ok:
                                #On essaye d'appeler la fonction de detection de bord qui utilise les contours
                                # on refait ce debut juste parce que le kernel a ete modifie precedement 
                                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
                                dest=cv2.dilate(imcanny,kernel)
                                imrote=scan.rotation(dest,angle_rot)

                                coord_bords,cont_bords=scan.detectbord(imrote)
                                rec=np.array(coord_bords)
                                paper=aide.four_point_transform(imgray,rec)
                                pdest=aide.four_point_transform(imrote,rec)
                                papier=aide.four_point_transform(couleur,rec)
                                rec=np.array(coord_bords)

                                #On s'attaque au nom et au listening/reading
                                contours, hierarchy = cv2.findContours(pdest, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                                ctri=sorted(contours, key=cv2.contourArea, reverse=False)
                                resu=scan.extraction_nom(papier,i,ctri)
                                parties=scan.detection_sections(paper,ctri)
                                if(len(parties)!=2):
                                    #si malgré ça on n'a pas de solution on abandonne
                                    liste_erreurs.append(('feuille '+str(i+1),'Impossible recuperer distinctement le listening et le reading, essayez un meilleur scan'))
                                    continue

                        listening=parties[0]
                        reading=parties[1]
                        
                        choix1,seuillage1=scan.division_image(listening)
                        choix2,seuillage2=scan.division_image(reading)

                        score_l,rep_list=scan.detection_rep(choix1,seuillage1,listening_r,5)
                        score_r,rep_read=scan.detection_rep(choix2,seuillage2,reading_r,4)

                        noms_fichier.append(chemin)
                        reponses_etud=rep_list+rep_read
                        reponses_fichier.append(reponses_etud)
                        score_fichier.append((score_l,score_r))

                    except:
                        liste_erreurs.append(('feuille '+str(i+1),'Une erreur est survenue en corrigeant cette feuille, essayez un meilleur scan'))
                        #e= sys.exc_info()[0]
                        #print(e)

                #ici envoyer le resultat à l'excel
                name=fichier.split('.')
                ex.excel_final(path+"/"+name[0]+".xlsx",noms_fichier,reponses_fichier,score_fichier,liste_erreurs)

                #print(reponses_fichier)

                #print()
                #print("Correction Terminee")    

                os.system("rmdir "+mon_dossier+"/S/Q")