import shutil
import Application_vue
import sys

class Model(object):

    def telecharger(path):
        #attention ici en 1er argument ilfaudra mettre le chemin relatif du pdf
        shutil.copy("qccm.png",path)

    def enregist(x,nom):
         enr = Application_vue.Application(nom)
         exit = enr.run(sys.argv)
