class Polyedre():
    def __init__(self):
        self.nomobj = ""
        self.listesommets = []
        self.listenormales = []
        self.listecoordtextures = []
        self.listeindicestriangle = []  # pour chaque triangle
        self.listeindicesnormales = []  # pour chaque triangle
        self.listeindicestextures = []  # pour chaque triangle
        self.listecouleurs = []
        self.listecoefs = []
        self.texture_on = False
        self.texture_ima = []
        self.texture_size = []
        self.indice_objet = -1


class Donnees_scene():

    def __init__(self, nomfic=""):

        self.Ia = 0
        self.d = 0
        self.listelum = []  # liste de quadruplets (posx,posy,posz,IS)
        self.listeobjets = []  # liste des polyedres

        fichier = open(nomfic, "r")

        for ligne in fichier:
            if (ligne[0] == 'a'):
                donnees = ligne.rstrip('\n\r').split(" ")
                self.Ia = float(donnees[1])

            if (ligne[0] == 'd'):
                donnees = ligne.rstrip('\n\r').split(" ")
                self.d = float(donnees[1])

            if (ligne[0] == 'l' and ligne[1] == ' '):
                lum = []
                donnees = ligne.rstrip('\n\r').split(" ")
                lum.append(float(donnees[1]))
                lum.append(float(donnees[2]))
                lum.append(float(donnees[3]))
                lum.append(float(donnees[4]))
                self.listelum.append(lum)

         # Fermeture du fichier
        fichier.close()

    def ajoute_objet(self, nomfic="", indcptobj=-1):
        fichier = open(nomfic, "r")
        coul = (0, 0, 0)
        coefs = (0, 0, 0, 0)

        coordonnees_texture_existent = False

        from PIL import Image
        from tkinter import filedialog

        poly = Polyedre()
        poly.indice_objet = indcptobj

        ligne1 = fichier.readline()
        ligne2 = fichier.readline()
        poly.nomobj = ligne2.strip()

        # print ligne1
        if int(ligne1) == 1:  # si le polyedre est texturable
            fichiertexture = filedialog.askopenfilename(
                title="Associer une texture a l objet?:", initialdir="../ressources/scenes", filetypes=[("Textures", "*.jpg; *.png; *.bmp")])
            if len(fichiertexture) > 0:
                poly.texture_on = True
                img = Image.open(fichiertexture)
                print("Dimensions de la texture " +
                      str(img.size[0]) + " " + str(img.size[1]))
                mat = list(img.getdata())

                poly.texture_ima = mat
                poly.texture_size = img.size

        for ligne in fichier:
            if (ligne[0] == 'v' and ligne[1] == ' '):
                sommet = []
                donnees = ligne.rstrip('\n\r').split(" ")
                sommet.append(float(donnees[1]))
                sommet.append(float(donnees[2]))
                sommet.append(float(donnees[3]))

                poly.listesommets.append(sommet)

            if (ligne[0] == 'v' and ligne[1] == 'n'):
                norm = []
                donnees = ligne.rstrip('\n\r').split(" ")
                norm.append(float(donnees[1]))
                norm.append(float(donnees[2]))
                norm.append(float(donnees[3]))

                poly.listenormales.append(norm)

            if (ligne[0] == 'v' and ligne[1] == 't'):
                txt = []
                coordonnees_texture_existent = True
                donnees = ligne.rstrip('\n\r').split(" ")
                txt.append(float(donnees[1]))
                txt.append(float(donnees[2]))
                poly.listecoordtextures.append(txt)

            if (ligne[0] == 'c'):
                nvcoul = []
                don = ligne.rstrip('\n\r').split(" ")
                for chaine in don:
                    if (chaine != "c" and chaine != ""):
                        donnees = chaine.split("/")
                        rouge = int(donnees[0])
                        vert = int(donnees[1])
                        bleu = int(donnees[2])
                        nvcoul = (rouge, vert, bleu)
                coul = nvcoul

            if (ligne[0] == 'k'):
                nvcoefs = []
                don = ligne.rstrip('\n\r').split(" ")
                for chaine in don:
                    if (chaine != "k" and chaine != ""):
                        donnees = chaine.split("/")
                        ka = float(donnees[0])
                        krd = float(donnees[1])
                        krs = float(donnees[2])
                        ns = int(donnees[3])
                        nvcoefs = (ka, krd, krs, ns)
                coefs = nvcoefs

            if (ligne[0] == 'f'):
                indicestriangle = []
                indicesnormalesautriangle = []
                indicescoordtextureautriangle = []
                don = ligne.rstrip('\n\r').split(" ")
                # n=1
                for chaine in don:
                    if (chaine != "f" and chaine != ""):
                        donnees = chaine.split("/")
                        indicestriangle.append(int(donnees[0]))
                        if coordonnees_texture_existent:
                            indicescoordtextureautriangle.append(
                                int(donnees[1]))
                        else:
                            poly.texture_on = False
                        indicesnormalesautriangle.append(int(donnees[2]))

                poly.listeindicestriangle.append(indicestriangle)
                poly.listeindicestextures.append(indicescoordtextureautriangle)
                poly.listeindicesnormales.append(indicesnormalesautriangle)
                poly.listecouleurs.append(coul)
                poly.listecoefs.append(coefs)

        # Fermeture du fichier
        self.listeobjets.append(poly)
        fichier.close()
        return poly.texture_on
