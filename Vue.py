import tkinter
import PIL
from PIL import ImageTk
from PIL import Image
from PIL import ImageDraw
from tkinter.colorchooser import *


import Controleur


class VueCourbes(object):
    """ Gere l'affichage et la manipulation de courbe avec la bibliotheque Tkinter. """

    def __init__(self, largeur, hauteur):
        self.controleur = Controleur.ControleurCourbes()
        self.largeur = largeur
        self.hauteur = hauteur
        self.canvas = []
        self.image = []
        self.imageDraw = []
        self.imageTk = []
        self.outilsCourant = []
        self.outilsDeplacer = None
        # Controles Draw
        self.drawControles = []
        # Repeat Outils Courant
        self.repeatOutilsCourant = []
        self.requieredAddedControles = 0
        self.outilsSauvergarde = []
        # Color Pickers
        self.segmentColor = (128, 128, 128)

    def callbackButton1(self, event):
        """ Bouton gauche : utilise l'outils courant. """
        if not self.outilsCourant:
            if self.drawControles.get():
                self.outilsDeplacer = self.controleur.selectionnerControle(
                    (event.x, event.y))
        elif self.repeatOutilsCourant.get():
            if self.requieredAddedControles <= 0:
                if self.outilsSauvergarde:
                    self.outilsSauvergarde()

    def callbackB1Motion(self, event):
        if self.outilsDeplacer:
            self.outilsDeplacer((event.x, event.y))
            self.majAffichage()

    def callbackButtonRelease1(self, event):
        """ Bouton gauche : utilise l'outils courant. """
        print(event.x, event.y)
        if self.outilsCourant:
            self.outilsCourant((event.x, event.y))
            if self.repeatOutilsCourant.get():
                self.requieredAddedControles -= 1
            self.majAffichage()
        if self.outilsDeplacer:
            self.outilsDeplacer = None

    def callbackButtonRelease3(self, event):
        """ Bouton droit : termine l'outils courant. """
        self.outilsCourant = []
        self.outilsSauvergarde = []
        self.majAffichage()

    def callbackButton3(self, event):
        """ Bouton droit : termine l'outils courant. """
        self.outilsCourant = []
        self.outilsSauvergarde = []
        self.majAffichage()

    def callbackNouveau(self):
        """ Supprime toutes les courbes. """
        self.controleur = Controleur.ControleurCourbes()
        self.majAffichage()

    def callbackChange(self):
        """ Met a jour en cas de changement. """
        self.majAffichage()

    def callbackSegmentColorPick(self):
        """ Choisi la couleur des Segments. """
        color = tkinter.colorchooser.askcolor()
        if color[0]:
            self.segmentColor = list(color[0])
            for c in range(3):
                self.segmentColor[c] = round(self.segmentColor[c])
            self.segmentColor = tuple(self.segmentColor)

    def callbackHorizontale(self):
        """ Initialise l'outils courant pour ajouter une nouvelle horizontale. """
        self.outilsCourant = self.controleur.nouvelleHorizontale()
        self.outilsSauvergarde = lambda: self.callbackHorizontale()
        self.requieredAddedControles = 2

    def callbackVerticale(self):
        """ Initialise l'outils courant pour ajouter une nouvelle verticale. """
        self.outilsCourant = self.controleur.nouvelleVerticale()
        self.outilsSauvergarde = lambda: self.callbackVerticale()
        self.requieredAddedControles = 2

    def callbackGauche(self):
        """ Initialise l'outils courant pour ajouter une nouvelle gauche. """
        self.outilsCourant = self.controleur.nouvelleGauche()
        self.outilsSauvergarde = lambda: self.callbackGauche()
        self.requieredAddedControles = 2

    def callbackDroite(self):
        """ Initialise l'outils courant pour ajouter une nouvelle droite. """
        self.outilsCourant = self.controleur.nouvelleDroite()
        self.outilsSauvergarde = lambda: self.callbackDroite()
        self.requieredAddedControles = 2

    def callbackSegment(self):
        """ Initialise l'outils courant pour ajouter un segmant. """
        self.outilsCourant = self.controleur.nouvelleSegment()
        self.outilsSauvergarde = lambda: self.callbackSegment()
        self.requieredAddedControles = 2

    def callbackSegmentPointMilieu(self):
        """ Initialise l'outils courant pour ajouter un segmant. """
        self.outilsCourant = self.controleur.nouvelleSegmentPointMilieu(
            self.segmentColor)
        self.outilsSauvergarde = lambda: self.callbackSegmentPointMilieu()
        self.requieredAddedControles = 2

    def majAffichage(self):
        """ Met a jour l'affichage.. """
        # efface la zone de dession
        self.imageDraw.rectangle(
            [0, 0, self.largeur, self.hauteur], fill='lightgrey')
        # dessine les courbes

        def fonctionPoint(p, c): return self.imageDraw.point(
            p, c)  # p le point, c la couleur
        def fonctionControle(p): return self.imageDraw.rectangle(
            [p[0]-2, p[1]-2, p[0]+2, p[1]+2], fill='blue')
        self.controleur.dessiner(
            fonctionControle, fonctionPoint, self.drawControles.get())
        # ImageTk : structure pour afficher l'image
        self.imageTk = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(
            self.largeur/2 + 1, self.hauteur/2 + 1, image=self.imageTk)

    def executer(self):
        """ Initialise et lance le programme. """
        # fenetre principale
        fenetre = tkinter.Tk()
        fenetre.title("ASI1 : TP")
        fenetre.resizable(0, 0)
        # menu
        menu = tkinter.Menu(fenetre)
        fenetre.config(menu=menu)
        filemenu = tkinter.Menu(menu)
        menu.add_cascade(label="Fichier", menu=filemenu)
        filemenu.add_command(label="Nouveau", command=self.callbackNouveau)
        filemenu.add_separator()
        filemenu.add_command(label="Quitter", command=fenetre.destroy)
        toolsmenu = tkinter.Menu(menu)
        menu.add_cascade(label="Outils", menu=toolsmenu)
        toolsmenu.add_command(label="Ajouter une horizontale",
                              command=self.callbackHorizontale)
        toolsmenu.add_command(label="Ajouter une verticale",
                              command=self.callbackVerticale)
        toolsmenu.add_command(label="Ajouter une gauche",
                              command=self.callbackGauche)
        toolsmenu.add_command(label="Ajouter une droite",
                              command=self.callbackDroite)
        toolsmenu.add_command(label="Ajouter un segment",
                              command=self.callbackSegment)
        toolsmenu.add_command(label="Ajouter un segment",
                              command=self.callbackSegmentPointMilieu)
        ### Ajouts TPs ###
        ## Boutons ##
        togglemenu = tkinter.Menu(menu)
        menu.add_cascade(label="Boutons", menu=togglemenu)
        self.drawControles = tkinter.BooleanVar()
        self.drawControles.set(True)
        togglemenu.add_checkbutton(label="Controles", variable=self.drawControles,
                                   onvalue=True, offvalue=0, command=self.callbackChange)
        self.repeatOutilsCourant = tkinter.BooleanVar()
        self.repeatOutilsCourant.set(False)
        togglemenu.add_checkbutton(
            label="Continu", variable=self.repeatOutilsCourant, onvalue=True, offvalue=0)
        ## Editer ##
        editormenu = tkinter.Menu(menu)
        editormenu.add_command(label="Couleur des Segment",
                               command=self.callbackSegmentColorPick)
        menu.add_cascade(label="Editeur", menu=editormenu)

        # Canvas : widget pour le dessin dans la fenetre principale
        self.canvas = tkinter.Canvas(
            fenetre, width=self.largeur, height=self.hauteur, bg='white')
        self.canvas.bind("<Button-1>", self.callbackButton1)
        self.canvas.bind("<B1-Motion>", self.callbackB1Motion)
        self.canvas.bind("<ButtonRelease-1>", self.callbackButtonRelease1)
        self.canvas.bind("<ButtonRelease-3>", self.callbackButtonRelease3)
        self.canvas.bind("<Button-3>", self.callbackButton3)
        self.canvas.pack()
        # Image : structure contenant les donnees de l'image manipule
        self.image = Image.new(
            "RGB", (self.largeur, self.hauteur), 'lightgrey')
        # ImageDraw : structure pour manipuler l'image
        self.imageDraw = ImageDraw.Draw(self.image)
        # met a jour l'affichage
        self.majAffichage()
        # lance le programme
        fenetre.mainloop()
