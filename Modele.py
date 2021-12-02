from tkinter.constants import ACTIVE

from PIL.Image import new


class Courbe(object):
    """ Classe generique definissant une courbe. """

    def __init__(self, _couleur=(0, 0, 0), _brush=(255, 0, 0)):
        self.controles = []
        self.couleur = _couleur
        self.brush = _brush

    def dessinerControles(self, dessinerControle):
        """ Dessine les points de controle de la courbe. """
        for controle in self.controles:
            dessinerControle(controle)

    def dessinerPoints(self, dessinerPoint):
        """ Dessine la courbe. Methode a redefinir dans les classes derivees. """
        pass

    def ajouterControle(self, point):
        """ Ajoute un point de controle. """
        # print point
        self.controles.append(point)

    def remplir(self, dessinerPoint):
        """ remplir une courbe fermee : triangle"""
        pass


class Horizontale(Courbe):
    """ Definit une horizontale. Derive de Courbe. """

    def ajouterControle(self, point):
        """ Ajoute un point de controle a l'horizontale.
        Ne fait rien si les 2 points existent deja. """
        if len(self.controles) < 2:
            Courbe.ajouterControle(self, point)

    def dessinerPoints(self, dessinerPoint):
        """ Dessine la courbe. Redefinit la methode de la classe mere. """
        if len(self.controles) == 2:
            x1 = self.controles[0][0]
            x2 = self.controles[1][0]
            y = self.controles[0][1]
            xMin = min(x1, x2)
            xMax = max(x1, x2)
            for x in range(xMin, xMax):
                dessinerPoint((x, y), self.couleur)


class Verticale(Courbe):
    """ Definit une Verticale. Derive de Courbe. """

    def ajouterControle(self, point):
        """ Ajoute un point de controle a l'horizontale.
        Ne fait rien si les 2 points existent deja. """
        if len(self.controles) < 2:
            Courbe.ajouterControle(self, point)

    def dessinerPoints(self, dessinerPoint):
        """ Dessine la courbe. Redefinit la methode de la classe mere. """
        if len(self.controles) == 2:
            y1 = self.controles[0][1]
            y2 = self.controles[1][1]
            x = self.controles[0][0]
            yMin = min(y1, y2)
            yMax = max(y1, y2)
            for y in range(yMin, yMax):
                dessinerPoint((x, y), self.couleur)


class Gauche(Courbe):

    def ajouterControle(self, point):
        if len(self.controles) < 2:
            Courbe.ajouterControle(self, point)

    def dessinerPoints(self, dessinerPoint):
        if len(self.controles) == 2:
            x1 = self.controles[0][0]
            x2 = self.controles[1][0]
            y1 = self.controles[0][1]
            y2 = self.controles[1][1]
            yMin = min(y1, y2)
            yMax = max(y1, y2)
            if yMin == y1:
                xMin = x1
                xMax = x2
            else:
                xMin = x2
                xMax = x1
            num = xMax - xMin
            den = yMax - yMin
            x = xMin
            if num > 0:
                increment = den - 1
            else:
                increment = 0

            for y in range(yMin, yMax+1):
                dessinerPoint((x, y), self.couleur)
                increment += num
                Q = increment // den
                x += Q
                increment -= Q * den


class Droite(Courbe):

    def ajouterControle(self, point):
        if len(self.controles) < 2:
            Courbe.ajouterControle(self, point)

    def dessinerPoints(self, dessinerPoint):
        if len(self.controles) == 2:
            x1 = self.controles[0][0]
            x2 = self.controles[1][0]
            y1 = self.controles[0][1]
            y2 = self.controles[1][1]
            yMin = min(y1, y2)
            yMax = max(y1, y2)
            if yMin == y1:
                xMin = x1
                xMax = x2
            else:
                xMin = x2
                xMax = x1
            num = xMax - xMin
            den = yMax - yMin
            x = xMin
            if num > 0:
                increment = -1
            else:
                increment = -den

            for y in range(yMin, yMax+1):
                dessinerPoint((x, y), self.couleur)
                increment += num
                Q = increment // den
                x += Q
                increment -= Q * den


class Segment(Courbe):

    def ajouterControle(self, point):
        if len(self.controles) < 2:
            Courbe.ajouterControle(self, point)

    def dessinerPoints(self, dessinerPoint):
        if len(self.controles) == 2:
            x1 = self.controles[0][0]
            x2 = self.controles[1][0]
            y1 = self.controles[0][1]
            y2 = self.controles[1][1]
            yMin = min(y1, y2)
            yMax = max(y1, y2)
            if yMin == y1:
                xMin = x1
                xMax = x2
            else:
                xMin = x2
                xMax = x1
            num = xMax - xMin
            den = yMax - yMin
            xGauche = xMin
            xDroite = xMin
            if num > 0:
                incrementDroite = -1
                incrementGauche = den - 1
            else:
                incrementDroite = -den
                incrementGauche = 0

            for y in range(yMin, yMax+1):
                dessinerPoint((xDroite, y), (255, 0, 0))
                incrementDroite += num
                QDroite = incrementDroite // den
                xDroite += QDroite
                incrementDroite -= QDroite * den

                dessinerPoint((xGauche, y), (0, 255, 0))
                incrementGauche += num
                QGauche = incrementGauche // den
                xGauche += QGauche
                incrementGauche -= QGauche * den


class SegmentPointMilieu(Courbe):

    def ajouterControle(self, point):
        if len(self.controles) < 2:
            Courbe.ajouterControle(self, point)

    def dessinerPoints(self, dessinerPoint):
        if len(self.controles) == 2:
            x1 = self.controles[0][0]
            x2 = self.controles[1][0]
            y1 = self.controles[0][1]
            y2 = self.controles[1][1]
            yMin = min(y1, y2)
            yMax = max(y1, y2)
            if yMin == y1:
                xMin = x1
                xMax = x2
            else:
                xMin = x2
                xMax = x1

            x = xMin
            y = yMin

            dessinerPoint((x, y), self.couleur)
            if xMax >= xMin:
                dx = xMax - xMin
                dy = yMax - yMin
                if dx >= dy:
                    dp = 2*dy-dx
                    deltaE = 2*dy
                    deltaNE = 2*(dy-dx)
                    while x < xMax:
                        if dp <= 0:
                            dp += deltaE
                            x += 1
                        else:
                            dp += deltaNE
                            x += 1
                            y += 1
                        dessinerPoint((x, y), self.couleur)
                else:
                    dp = 2*dx-dy
                    deltaE = 2*dx
                    deltaNE = 2*(dx-dy)
                    while y < yMax:
                        if dp <= 0:
                            dp += deltaE
                            y += 1
                        else:
                            dp += deltaNE
                            x += 1
                            y += 1
                        dessinerPoint((x, y), self.couleur)
            else:
                dx = xMin - xMax
                dy = yMax - yMin
                if dx >= dy:
                    dp = 2*dy-dx
                    deltaE = 2*dy
                    deltaNE = 2*(dy-dx)
                    while x > xMax:
                        if dp <= 0:
                            dp += deltaE
                            x -= 1
                        else:
                            dp += deltaNE
                            x -= 1
                            y += 1
                        dessinerPoint((x, y), self.couleur)
                else:
                    dp = 2*dx-dy
                    deltaE = 2*dx
                    deltaNE = 2*(dx-dy)
                    while y < yMax:
                        if dp <= 0:
                            dp += deltaE
                            y += 1
                        else:
                            dp += deltaNE
                            x -= 1
                            y += 1
                        dessinerPoint((x, y), self.couleur)


class Arrete():

    def __init__(self, yhaut1=0, x1=0, num1=0, den1=0, inc1=0):
        self.yhaut = yhaut1
        self.x = x1
        self.num = num1
        self.den = den1
        self.inc = inc1

    def mise_a_jour(self):
        self.inc += self.num
        Q = self.inc/self.den
        self.x += Q
        self.inc -= Q*self.den


class TriangleRempli(Courbe):
    """remplir le triangle de la couleur passee au constructeur"""

    def __init__(self, couleur):
        Courbe.__init__(self, (0, 0, 0), couleur)

    def ajouterControle(self, point):
        """ Ajoute un point de controle.Ne fait rien si les 3 points existent deja."""
        if len(self.controles) < 3:
            Courbe.ajouterControle(self, point)

    def remplir(self, dessinerPoint):
        if len(self.controles) == 3:
            Pmax = [0, 1]
            Pmoy = [0, 1]
            Pmin = [0, 1]
            if (self.controles[0][1] >= self.controles[1][1]) and (self.controles[0][1] >= self.controles[2][1]):
                Pmax = self.controles[0]
                if self.controles[1][1] >= self.controles[2][1]:
                    Pmoy = self.controles[1]
                    Pmin = self.controles[2]
                else:
                    Pmoy = self.controles[2]
                    Pmin = self.controles[1]
            elif (self.controles[1][1] >= self.controles[0][1]) and (self.controles[1][1] >= self.controles[2][1]):
                Pmax = self.controles[1]
                if self.controles[0][1] >= self.controles[2][1]:
                    Pmoy = self.controles[0]
                    Pmin = self.controles[2]
                else:
                    Pmoy = self.controles[2]
                    Pmin = self.controles[0]
            else:
                Pmax = self.controles[2]
                if self.controles[0][1] >= self.controles[1][1]:
                    Pmoy = self.controles[0]
                    Pmin = self.controles[1]
                else:
                    Pmoy = self.controles[1]
                    Pmin = self.controles[0]

            y = Pmin[1]

            dxMinMax = Pmax[0] - Pmin[0]
            dyMinMax = Pmax[1] - Pmin[1]

            # Pmoy est a gauche
            if (dyMinMax * (Pmoy[0] - Pmin[0]) - dxMinMax * (Pmoy[1] - Pmin[1])) < 0:
                print("Pmoy est a gauche")
                # [yhaut, x, num, den, inc]
                # [Pmin,Pmoy] arête gauche  et [Pmin,Pmax] arête droite
                num = Pmoy[0] - Pmin[0]
                den = Pmoy[1] - Pmin[1]
                if num > 0:
                    increment = den - 1
                else:
                    increment = 0
                AActiveGauche = Arrete(Pmoy[1], Pmin[0], num, den, increment)

                num = Pmax[0] - Pmin[0]
                den = Pmax[1] - Pmin[1]
                if num > 0:
                    increment = -1
                else:
                    increment = -den
                AActiveDroite = Arrete(Pmax[1], Pmin[0], num, den, increment)

                while y < Pmoy[1]:
                    for i in range(int(AActiveGauche.x), int(AActiveDroite.x)):
                        dessinerPoint((i, y), self.brush)
                    AActiveDroite.mise_a_jour()
                    AActiveGauche.mise_a_jour()
                    y += 1

                # Redefinition AActiveGauche

                num = Pmax[0] - Pmoy[0]
                den = Pmax[1] - Pmoy[1]
                if num > 0:
                    increment = den - 1
                else:
                    increment = 0
                AActiveGauche = Arrete(Pmax[1], Pmoy[0], num, den, increment)

                while y < Pmax[1]:
                    for i in range(int(AActiveGauche.x), int(AActiveDroite.x)):
                        dessinerPoint((i, y), self.brush)
                    AActiveDroite.mise_a_jour()
                    AActiveGauche.mise_a_jour()
                    y += 1

            elif (dyMinMax * (Pmoy[0] - Pmin[0]) - dxMinMax * (Pmoy[1] - Pmin[1])) > 0:
                print("Pmoy est a droite")
                # [yhaut, x, num, den, inc]
                # [Pmin,Pmax] arête gauche  et [Pmin,Pmoy] arête droite
                num = Pmax[0] - Pmin[0]
                den = Pmax[1] - Pmin[1]
                if num > 0:
                    increment = den - 1
                else:
                    increment = 0
                AActiveGauche = Arrete(Pmax[1], Pmin[0], num, den, increment)

                num = Pmoy[0] - Pmin[0]
                den = Pmoy[1] - Pmin[1]
                if num > 0:
                    increment = -1
                else:
                    increment = -den
                AActiveDroite = Arrete(Pmoy[1], Pmin[0], num, den, increment)

                while y < Pmoy[1]:
                    print("premiere")
                    for i in range(int(AActiveGauche.x), int(AActiveDroite.x)):
                        dessinerPoint((i, y), self.brush)
                    AActiveDroite.mise_a_jour()
                    AActiveGauche.mise_a_jour()
                    y += 1

                # Redefinition AActiveDroite

                num = Pmax[0] - Pmoy[0]
                den = Pmax[1] - Pmoy[1]
                if num > 0:
                    increment = -1
                else:
                    increment = -den
                AActiveDroite = Arrete(Pmax[1], Pmoy[0], num, den, increment)

                while y < Pmax[1]:
                    for i in range(int(AActiveGauche.x), int(AActiveDroite.x)):
                        dessinerPoint((i, y), self.brush)
                    AActiveDroite.mise_a_jour()
                    AActiveGauche.mise_a_jour()
                    y += 1
