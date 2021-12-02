import Modele


class ControleurCourbes(object):
    """ Gere un ensemble de courbes. """

    def __init__(self):
        self.courbes = []
        self.scene = []  # sert pour l affichage des scenes (donnees importees)

    def ajouterCourbe(self, courbe):
        """ Ajoute une courbe supplementaire.  """
        self.courbes.append(courbe)

    def dessiner(self, dessinerControle, dessinerPoint, enabled):
        """ Dessine les courbes. """
        # dessine les point de la courbe
        for courbe in self.courbes:
            courbe.dessinerPoints(dessinerPoint)

        # si la courbe peut etre remplie
        for courbe in self.courbes:
            courbe.remplir(dessinerPoint)

        # dessine les point de controle
        if enabled:
            for courbe in self.courbes:
                courbe.dessinerControles(dessinerControle)

    def deplacerControle(self, ic, ip, point):
        """ Deplace le point de controle a l'indice ip de la courbe a l'indice ic. """
        self.courbes[ic].controles[ip] = point

    def selectionnerControle(self, point):
        """ Trouve un point de controle proche d'un point donne. """
        xp, yp = point
        for ic in range(len(self.courbes)):
            for ip in range(len(self.courbes[ic].controles)):
                xc, yc = self.courbes[ic].controles[ip]
                if abs(xc-xp) < 4 and abs(yc-yp) < 4:
                    return lambda p: self.deplacerControle(ic, ip, p)
        return None

    def nouvelleHorizontale(self):
        """ Ajoute une nouvelle horizontale initialement vide.
        Retourne une fonction permettant d'ajouter les points de controle. """
        horizontale = Modele.Horizontale()
        self.ajouterCourbe(horizontale)
        return horizontale.ajouterControle

    def nouvelleVerticale(self):
        """ Ajoute une nouvelle verticale initialement vide.
        Retourne une fonction permettant d'ajouter les points de controle. """
        verticale = Modele.Verticale()
        self.ajouterCourbe(verticale)
        return verticale.ajouterControle

    def nouvelleGauche(self):
        """ Ajoute une nouvelle verticale initialement vide.
        Retourne une fonction permettant d'ajouter les points de controle. """
        gauche = Modele.Gauche()
        self.ajouterCourbe(gauche)
        return gauche.ajouterControle

    def nouvelleDroite(self):
        """ Ajoute une nouvelle verticale initialement vide.
        Retourne une fonction permettant d'ajouter les points de controle. """
        droite = Modele.Droite()
        self.ajouterCourbe(droite)
        return droite.ajouterControle

    def nouvelleSegment(self):
        """ Ajoute une nouvelle verticale initialement vide.
        Retourne une fonction permettant d'ajouter les points de controle. """
        segment = Modele.Segment()
        self.ajouterCourbe(segment)
        return segment.ajouterControle

    def nouvelleSegmentPointMilieu(self, couleur):
        """ Ajoute une nouvelle verticale initialement vide.
        Retourne une fonction permettant d'ajouter les points de controle. """
        segmentPointMilieu = Modele.SegmentPointMilieu(couleur)
        self.ajouterCourbe(segmentPointMilieu)
        return segmentPointMilieu.ajouterControle

    def nouveauTriangleRempli(self, couleur):
        triangleRempli = Modele.TriangleRempli(couleur)
        self.ajouterCourbe(triangleRempli)
        return triangleRempli.ajouterControle

    """ Read Scene Process. """

    def readScene(self, larg, haut, method):
        import Import_scene
        from tkinter import filedialog

        donnees = Import_scene.Donnees_scene(
            "ressources/scenes/Donnees_scene.sce")
        self.scene = donnees
        d = self.scene.d  # distance de la camera a l ecran

        fic = "fic"
        indcptobj = -1
        while len(fic) > 0:  # tant que des fichiers objets selectionnes
            fic = filedialog.askopenfilename(
                title="Inserer l objet:", initialdir="ressources/scenes", filetypes=[("Fichiers Objets", "*.obj")])
            if len(fic) > 0:
                indcptobj += 1
                donnees.ajoute_objet(fic, indcptobj)

                self.scene = donnees

        # mettre objet dans repere camera avec translation differente de l objet Diamant et changement axes y<->z
        listesommetsdansreperecamera = []
        for som in self.scene.listeobjets[indcptobj].listesommets:
            if self.scene.listeobjets[indcptobj].nomobj == "Diamant":
                tx = 150
                ty = 150
                tz = 2.2*d
            elif self.scene.listeobjets[indcptobj].nomobj == "Cube":
                tx = 350
                ty = 100
                tz = 2*d
            else:
                tx = 200
                ty = 0
                tz = 1.8*d

            yp = som[2]+ty
            xp = -som[1]+tx
            zp = som[0]+tz

            listesommetsdansreperecamera.append((xp, yp, zp))

        method(indcptobj, d, larg, haut, listesommetsdansreperecamera)

    """ Method of Wireframe. """

    def methodSceneFildefer(self, indcptobj, d, larg, haut, listesommetsdansreperecamera):
        listeprojete = []
        # Projection perspective des sommets 3D du polyedre exprimes dans le repere camera:
        for pt in listesommetsdansreperecamera:
            ptSx = pt[0] * d / pt[2]
            ptSy = pt[1] * d / pt[2]
            ptSx += larg / 2
            ptSy -= (haut + 1) / 2 - 1
            ptSy *= -1
            listeprojete.append([round(ptSx), round(ptSy)])

        i = -1
        # Pour chaque triangle du polyedre : construction des 3 segments par algo point milieu.
        # Ajout des courbes et des points de controle.
        for tr in self.scene.listeobjets[indcptobj].listeindicestriangle:
            i += 1
            for ii in range(len(tr)):
                seg = Modele.SegmentPointMilieu(
                    self.scene.listeobjets[indcptobj].listecouleurs[i])
                seg.ajouterControle(listeprojete[tr[ii] - 1])
                seg.ajouterControle(listeprojete[tr[(ii + 1) % len(tr)] - 1])
                self.courbes.append(seg)

    """ Create a new Wireframe Scene. """

    def nouvelleSceneFildefer(self, larg, haut):
        self.readScene(larg, haut,
                       (lambda io, d, l, h, ls:
                        self.methodSceneFildefer(io, d, l, h, ls)))
