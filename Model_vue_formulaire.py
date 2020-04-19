
import shutil
class Model(object):

        def ecriture_fichier(self,reponse,nom_fichier):

            #dans le nom du fichier faudra mettre la concatenation avec le path
            #Ouverture du fichier
            nom_de_fichier = "JSON/"+nom_fichier +".json"
            fichier = open(nom_de_fichier,'w')
            #Ecriture de la partie Listening
            fichier.write('{''"''Listening''"' ':[{' )
            for i in range(100):
                if reponse[i] == "A" :
                    fichier.write( '"' + str(i)+'"' +': 1')
                elif reponse[i] == "B":
                    fichier.write( '"' + str(i)+'"' +': 2')
                elif reponse [i] == "C" :
                    fichier.write( '"' + str(i)+'"' +':3')
                elif reponse[i] == "D" :
                    fichier.write('"' + str(i)+'"' +': 4')

                if (i != 99):
                    fichier.write(",")


            #Ecriture partie reading
            fichier.write('}],''"''Reading''"' ':[{')
            for i in range(100,200):
                if reponse[i] == "A" :
                    fichier.write( '"' + str(i)+'"' +': 1')
                elif reponse[i] == "B":
                    fichier.write( '"' + str(i)+'"' +': 2')
                elif reponse [i] == "C" :
                    fichier.write( '"' + str(i)+'"' +':3')
                elif reponse[i] == "D" :
                    fichier.write('"' + str(i)+'"' +': 4')

                if (i != 199):
                    fichier.write(",")
            fichier.write("}]}")
            #fermeture fichier 
            fichier.close()
