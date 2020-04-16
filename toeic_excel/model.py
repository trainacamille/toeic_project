import shutil
import Application_vue
import sys
import scan

class Model(object):

    def telecharger(path):
        #attention ici en 1er argument ilfaudra mettre le chemin relatif du pdf
        shutil.copy("qccm.png",path)

    def enregist(x,nom):
        enr = Application_vue.Application(nom)
        exit = enr.run(sys.argv)

    def corriger(nom,path):
        nom='JSON/toeic_maison.json'
        #creer un repertoire dans lequel seront enregistrés les documents nécessaires à la correction
        mon_dossier='correction'
        os.mkdir(mon_dossier)
        #prendre le nom du fichier par la prof(ici statique) et le chemin créé 
        nb_pages=scan.pdfimg(path,mon_dossier)

        #Commencer le traitement pour chacune des pages recensées
        for i in range(0,nb_pages+1):
            img=cv2.imread(mon_dossier+'/epreuve'+str(i)+'.jpg',cv2.IMREAD_COLOR)

            #Si on n'a pas eu l'image
            if(not img.data):
                print('Oups, ton image n\'existe pas dis-donc!')
                continue
            #Detecter les contours pour la rotation
            #Pour cela appliquer le prétraitement de l'image et passer l'image traitée

            imgray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            contraste=cv2.convertScaleAbs(imgray,None,0.8,0)
            imflou=cv2.GaussianBlur(contraste,(5,5),0)
            imcanny=cv2.Canny(imflou,75,150,(3,3))

            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
            dest=cv2.dilate(imcanny,kernel)
            coord_bords,cont_bords=scan.detectbord(dest)

            if(len(coord_bords) != 5):
                print("Oups, je n'ai pas trouvé tous les points pour faire la bonne rotation")
                continue
            #On a trouve nos 5 carrés du bord et on va chercher la bonne rotation

            #Penser à l'écart pour une efficacité
            angle_rot=aide.rotationimage(coord_bords,80)
            imrote=scan.rotation(dest,angle_rot)
            imflou=scan.rotation(imflou,angle_rot)
            couleur=scan.rotation(img,angle_rot)

            #Apres rotation, on redétecte les bords sur l'image pour la remetre droite
            #si elle était de travers

            #(peut etre cette partie est-elle inutile mais on verra)

            coord_bords,cont_bords=scan.detectbord(imrote)
            cont=aide.sort_contours(cont_bords)[0]
            pliste=[]
            for u,cnt in enumerate(cont):
                #on a etudie la feuille et on sait que le repere au milieu est le 3eme point
                #on veut le sauter pour calibrer sur les bords
                if (u!=2):
                    ln=cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, 0.02 * ln, True)
                    (tl, tr, br, bl)=aide.order_points(approx.reshape(4,2))   
                    pliste.append((tr[0],tr[1]))  
            rec=aide.order_points(np.array(pliste))
            paper=aide.four_point_transform(imflou,rec)
            pdest=aide.four_point_transform(imrote,rec)
            papier=aide.four_point_transform(couleur,rec)

            #On s'attaque au nom et au listening/reading
            contours, hierarchy = cv2.findContours(pdest, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            ctri=sorted(contours, key=cv2.contourArea, reverse=False)
            scan.extraction_nom(papier,i,ctri)
            parties=scan.detection_sections(paper,ctri)

            if(len(parties)!=2):
                print(len(parties))
                print("Le listening et le reading n'ont pas étés trouves")
                continue
            listening=parties[0]
            reading=parties[1]
            listening_r,reading_r=scan.recuperer_reponse(nom)
            choix1,seuillage1=scan.division_image(listening)
            choix2,seuillage2=scan.division_image(reading)

            score_l=scan.detection_rep(choix1,seuillage1,listening_r,5)
            score_r=scan.detection_rep(choix2,seuillage2,reading_r,4)

            #ici envoyer le resultat à l'excel
            print("Le score Listening de "+str(i)+" est "+str(score_l))
            print("Le score Reading de "+str(i)+" est "+str(score_r))

        print()
        print("Correction Terminee")    

        os.system("rmdir name "+mon_dossier+" /S /Q")