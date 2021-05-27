"""
// ! \\   ATTENTION : veuillez a ne pas spammer (trop appuyer sur) les touches, sinon tkinter va crash                           // ! \\
// ! \\                                                                                                                          // ! \\
// ! \\   ATTENTION : vérifiez qu'un programme python .py s'execute par défault avec python (et non visual studio par exemple),  // ! \\
// ! \\                ça sera génant lorsque vous aller perdre (le programme lance un autre programme qui gère les scores)      // ! \\

Le jeu comporte du son.

Ceci est un jeu Tetris, voici les paramètres du jeu :
    - vous gagnez un niveau toutes les 5 lignes complétés

    - le jeu augmente en vitesse pour chaque ligne complétés (les levels 10 et plus ayant la vitesse la plus rapide)

    - il y a 5 touches :
        - fleche du bas : pose la pièce au sol
        - fleche du haut : effectue une rotation de la pièce
        - gauche / droite : bouge la pièce à gauche ou à droite
        - entrée : 'range' la pièce dans la troisième frame qui contient des case case (celle du mileu à droite),
                    vous pouvez re-appuyer par la suite sur 'entrée' pour reprendre cette pièce et ainsi
                    l'échanger avec la pièce en cours de descente (je vous invite à tester si ce n'est pas clair).

    - le score, il y a deux façons d'en gagner :
        - en completant une ligne vous gagnez 100 scores
        - en utilisant la flèches du bas vous gagnez l'équivalent de votre niveau en score
          (car plus la vitesse est élevé plus il est difficile d'utiliser cette touche)

si vous voulez seulement voir si le jeu fonctionne je vous invite à remplacer la ligne '688',
    'if int(ligne.get()) == 5:'    , par
     if int(ligne.get()) == 1:     , ce qui vous feras passer un niveau à chaque ligne complétée et non toutes les 5 lignes
"""
# # # # # # # # # # # # # # inport  # # # # # # # #  # #
from tkinter import *
import random
import sys
import os
import pygame
import time


# # # # # # # # # # # # # # classe # # # # # # # # # # #

class Case:
    """ classe qui stocke les différents éléments de chaque case"""
    def __init__(self,ligne,col,frame,couleur, can=True):
        # couleur (blanc de base):
        # sert à savoir la couleur de la pièce quand on la déplace
        self.c = couleur

        # coordonnées :
        self.ligne=ligne
        self.col=col

        # si vrai : la case fais partie de la piece active (celle qui descends et que l'on peut bouger)
        self.active=False

        # si vrai : la case fais partie d'une pièce
        self.o = False

        # set sur vrai si la case est le 'milieu' d'une pièce (la seul case qui ne bougera pas lors d'une rotation)
        self.milieu=False

        # on crée ici le canvas de la pièce, c'est à dire la partie graphique de celle ci via tkinter
        if can==True:
            self.can=Canvas(frame, borderwidth=5, background=self.c,highlightthickness=1, highlightbackground="#CECECE", width=20, height=20)
            self.can.grid(row=ligne, column=col)

class Piece2:
    """ classe d'une piece de la forme:
        # #
        # #
        """

    def __init__(self):
        global tableau_case, tableau_case_invisible

        # création de la matrice contenant des cases de la pièces, appartenant à tableau_case (tableau des cases du jeu)
        # toutes les matrices contenant des cases seront triés lignes par lignes, de haut en bas, puis de gauche à droite
        # la case ayant pour coordonées (0;0) est en haut à gauche
        c1 = tableau_case[3][4] # 4eme ligne et 5eme colonne
        c2 = tableau_case[3][4+1]
        c3 = tableau_case[4][4]
        c4 = tableau_case[4][4+1]


        self.case=[
            [c1,c2],
            [c3,c4],
        ]

        # on enregistre le 'nom' de la piece ici
        self.i_d = 2

        # comme la pièce viens d'être créer, elle est active (c'est celle qui descends et que l'on peut bouger)
        self.active = True

        # modification des cases de self.case
        # on parcours la matrice des cases de la pièce de ligne en ligne
        for l in self.case:
            # on parcours les lignes de gauche à droite
            for case in l:

                # si on créer notre pièce sur une pièce déjà existante on a perdu
                if case.o:
                    fin_jeu()

                # on configure ici la couleur de fond de la case
                case.c = "#F7FF3C"

                # on mets à jour des informations de la pièces
                case.active=True
                case.o = True

    def position(self):
        """ méthode qui gère les différentes positions de la pièce, or, comme elle est carré, une seul position existe, donc
        la méthode ne fais rien, mais existe pour éviter des erreurs plus tard
        """
        pass

class Piece1:
    def __init__(self):
        global tableau_case
        """ classe d'une piece de la forme:
          #
          @
          #
          #
        """

        c1 = tableau_case[1][4]
        c2 = tableau_case[2][4] # milieu de la case, la seul case à ne pas bouger lors d'une rotation.
        c3 = tableau_case[3][4]
        c4 = tableau_case[4][4]

        self.case=[
            [c1],
            [c2],
            [c3],
            [c4]
        ]

        self.i_d = 1

        c2.milieu = True

        # initialisation de la position de la pièce
        self.pos=1

        self.active = True

        for l in self.case:
            for case in l:

                if case.o:
                    fin_jeu()

                case.c = "#FF0000"

                case.active=True
                case.o = True

        # initialisation de tableau contenant les tuples des nouvelles coordonées de toutes les case
        # de la pièce, comparer à la case milieu (on procède à une addition)

        self.nouvelle_col_ligne1=[(0,-1),(0,0),(0,1),(0,2)] # appelé lorsque la position est 1

        self.nouvelle_col_ligne2=[(-1,0),(0,0),(1,0),(2,0)] # appelé lorsque la position est 2


    def position(self):
        """méthode qui gère les différentes positions de la pièce:

            #
            @    ou  # @ # #                @ étant le 'milieu'
            #
            #

        """
        global tableau_case

        # on cherche la case 'milieu' pour en enregistrer les coordonnées
        for l in self.case:
            for case in l:
                if case.milieu:
                    case_milieu = case
                    couleur = case.c

        # si la pièce est sur la position 1, on la passe en position 2 et inversement.
        if self.pos==1:
            # on vérifie que la pièce ne soit pas trop en haut ni trop en bas pour ne pas qu'elle dépasse.
            if 0 < case_milieu.ligne < 25:
                # verif_si_piece vérifie qu'il n'y a pas de pièce déjà présente où seront les nouvelles cases de la pièce.
                if verif_si_piece(self.nouvelle_col_ligne1, case_milieu):
                    # changement_position change la position de la pièce.
                    changement_position(self, self.nouvelle_col_ligne1, case_milieu, couleur)
                    self.pos=2


        elif self.pos==2:
            # on vérifie que la pièce ne soit pas trop à gauche ni trop à droite
            if 0 < case_milieu.col < 8:
                if verif_si_piece(self.nouvelle_col_ligne2, case_milieu):
                    changement_position(self, self.nouvelle_col_ligne2, case_milieu, couleur)
                    self.pos=1

class Piece3:
    def __init__(self):
        global tableau_case
        """ classe d'une piece de la forme:
          # #
        # #
        """
        # création de la matrice contenant des cases du tableau qui contient toutes les cases
        c1 = tableau_case[3][4]
        c2 = tableau_case[3][4+1]
        c3 = tableau_case[3+1][4-1]
        c4 = tableau_case[3+1][4]

        self.case=[
            [c1,c2],
            [c3,c4]
        ]

        c1.milieu = True

        self.i_d = 3

        self.pos=1

        self.active = True

        for l in self.case:
            for case in l:

                if case.o:
                    fin_jeu()

                case.c = "#34C924"

                case.active=True
                case.o = True

        self.nouvelle_col_ligne1 = [(-1,0),(0,0),(0,1),(1,1)] # appelé lorsque la position est 1
        self.nouvelle_col_ligne2 = [(0,0),(0,1),(1,-1),(1,0)] # appelé lorsque la position est 2


    def position(self):
        """méthode qui gère les différentes positions de la pièce, or, comme elle est une migne, deux seuls position existent :

                       #
            @ #   ou   @ #      @ --> la case 'milieu' de la pièce
          # #            #

        """
        global tableau_case

        for l in self.case:
            for case in l:
                if case.milieu:
                    case_milieu = case
                    couleur = case.c

        if self.pos==1:
            # on vérifie que la pièce ne soit pas en haut.
            if 0 < case_milieu.ligne:
                if verif_si_piece(self.nouvelle_col_ligne1, case_milieu):
                    changement_position(self, self.nouvelle_col_ligne1, case_milieu, couleur)
                    self.pos=2


        elif self.pos==2:
            # on vérifie que la pièce ne soit pas trop à gauche.
            if 0 < case_milieu.col:
                if verif_si_piece(self.nouvelle_col_ligne2, case_milieu):
                    changement_position(self, self.nouvelle_col_ligne2, case_milieu, couleur)
                    self.pos=1

class Piece4:
    def __init__(self):
        global tableau_case
        """ classe d'une piece de la forme:
          # #
            # #
        """
        c1 = tableau_case[3][4]
        c2 = tableau_case[3][4+1] # milieu
        c3 = tableau_case[3+1][4+1]
        c4 = tableau_case[3+1][4+2]

        self.case=[
            [c1,c2],
            [c3,c4]
        ]

        c2.milieu = True

        self.i_d = 4

        self.pos=1
        self.active = True

        for l in self.case:
            for case in l:

                if case.o:
                    fin_jeu()

                case.c = "#2C75FF"

                case.active=True
                case.o = True

        self.nouvelle_col_ligne1=[(-1,1),(0,0),(0,1),(1,0)]
        self.nouvelle_col_ligne2=[(0,-1),(0,0),(1,0),(1,1)]

    def position(self):
        """méthode qui gère les différentes positions de la pièce, or, comme elle est une migne, deux seuls position existent :

                         #
            # @   ou   @ #      @ --> la case 'milieu' de la pièce
              # #      #

        """

        global tableau_case

        for l in self.case:
            for case in l:
                if case.milieu:
                    case_milieu = case
                    couleur = case.c

        if self.pos==1:
            # on vérifie que la pièce ne soit pas en haut.
            if 0 < case_milieu.ligne:
                if verif_si_piece(self.nouvelle_col_ligne1, case_milieu):
                    changement_position(self, self.nouvelle_col_ligne1, case_milieu, couleur)
                    self.pos=2


        elif self.pos==2:
            # on vérifie que la pièce ne soit pas trop à droite.
            if 0 < case_milieu.col:
                if verif_si_piece(self.nouvelle_col_ligne2, case_milieu):
                    changement_position(self, self.nouvelle_col_ligne2, case_milieu, couleur)
                    self.pos=1

class Piece5:
    def __init__(self):
        global tableau_case
        """ classe d'une piece de la forme:
          # #
          @
          #
        """
        c1 = tableau_case[2][4]
        c2 = tableau_case[2][5]
        c3 = tableau_case[3][4] # milieu
        c4 = tableau_case[4][4]

        self.case=[
            [c1, c2],
            [c3],
            [c4]
        ]

        c3.milieu = True

        self.i_d = 5

        self.pos=1

        self.active = True

        for l in self.case:
            for case in l:

                if case.o:
                    fin_jeu()

                case.c = "#FF6600"

                case.active=True
                case.o = True

        self.nouvelle_col_ligne1=[(0,-1),(0,0),(0,1),(1,1)]
        self.nouvelle_col_ligne2=[(-1,0),(0,0),(1,-1),(1,0)]
        self.nouvelle_col_ligne3=[(-1,-1),(0,-1),(0,0),(0,1)]
        self.nouvelle_col_ligne4=[(-1,0),(-1,1),(0,0),(1,0)]

    def position(self):
        """méthode qui gère les différentes positions de la pièce:

            # #                    #       #
            @     ou  # @ #  ou    @   ou  # @ #
            #             #      # #

        """

        global tableau_case

        for l in self.case:
            for case in l:
                if case.milieu:
                    case_milieu = case
                    couleur = case.c

        if self.pos==1:
            # on vérifie que la pièce ne soit pas trop à gauche.
            if 0 < case_milieu.col:
                if verif_si_piece(self.nouvelle_col_ligne1, case_milieu):
                    changement_position(self, self.nouvelle_col_ligne1, case_milieu, couleur)
                    self.pos=2


        elif self.pos==2:
            # on vérifie que la pièce ne soit pas trop en haut.
            if 0 < case_milieu.ligne:
                if verif_si_piece(self.nouvelle_col_ligne2, case_milieu):
                    changement_position(self, self.nouvelle_col_ligne2, case_milieu, couleur)
                    self.pos=3

        elif self.pos==3:
            # on vérifie que la pièce ne soit pas trop à droite.
            if case_milieu.col < 9:
                if verif_si_piece(self.nouvelle_col_ligne3, case_milieu):
                    changement_position(self, self.nouvelle_col_ligne3, case_milieu, couleur)
                    self.pos=4

        elif self.pos==4:
            # on vérifie que la pièce ne soit pas trop en bas.
            if case_milieu.ligne < 26:
                if verif_si_piece(self.nouvelle_col_ligne4, case_milieu):
                    changement_position(self, self.nouvelle_col_ligne4, case_milieu, couleur)
                    self.pos=1

class Piece6:
    def __init__(self):
        global tableau_case
        """ classe d'une piece de la forme:
        # #
          @
          #
        """
        c1 = tableau_case[2][3]
        c2 = tableau_case[2][4]
        c3 = tableau_case[3][4] # milieu
        c4 = tableau_case[4][4]

        self.case=[
            [c1, c2],
            [c3],
            [c4]
        ]

        c3.milieu = True

        self.i_d = 6

        self.pos=1

        self.active = True

        for l in self.case:
            for case in l:

                if case.o:
                    fin_jeu()

                case.c = "#BB3385"

                case.active=True
                case.o = True

        self.nouvelle_col_ligne1=[(-1,1),(0,-1),(0,0),(0,1)]
        self.nouvelle_col_ligne2=[(-1,0),(0,0),(1,0),(1,1)]
        self.nouvelle_col_ligne3=[(0,-1),(0,0),(0,1),(1,-1)]
        self.nouvelle_col_ligne4=[(-1,-1),(-1,0),(0,0),(1,0)]

    def position(self):
        """méthode qui gère les différentes positions de la pièce:

        # #             #        #
          @     ou  # @ #  ou    @    ou  # @ #
          #                      # #      #

        """
        global tableau_case

        for l in self.case:
            for case in l:
                if case.milieu:
                    case_milieu = case
                    couleur = case.c

        if self.pos==1:
            # on vérifie que la pièce ne soit pas trop à droite.
            if case_milieu.col < 9:
                if verif_si_piece(self.nouvelle_col_ligne1, case_milieu):
                    changement_position(self, self.nouvelle_col_ligne1, case_milieu, couleur)
                    self.pos=2


        elif self.pos==2:
            # on vérifie que la pièce ne soit pas trop en bas.
            if case_milieu.ligne < 26:
                if verif_si_piece(self.nouvelle_col_ligne2, case_milieu):
                    changement_position(self, self.nouvelle_col_ligne2, case_milieu, couleur)
                    self.pos=3

        elif self.pos==3:
            # on vérifie que la pièce ne soit pas trop à gauche.
            if 0 < case_milieu.col:
                if verif_si_piece(self.nouvelle_col_ligne3, case_milieu):
                    changement_position(self, self.nouvelle_col_ligne3, case_milieu, couleur)
                    self.pos=4

        elif self.pos==4:
            # on vérifie que la pièce ne soit pas trop en haut.
            if 0 < case_milieu.ligne:
                if verif_si_piece(self.nouvelle_col_ligne4, case_milieu):
                    changement_position(self, self.nouvelle_col_ligne4, case_milieu, couleur)
                    self.pos=1

class Piece7:
    def __init__(self):
        global tableau_case
        """ classe d'une piece de la forme:
            #
          # @ #
        """
        c1 = tableau_case[3][4]
        c2 = tableau_case[4][3]
        c3 = tableau_case[4][4] # milieu
        c4 = tableau_case[4][5]

        self.case=[
            [c1],
            [c2, c3, c4]
        ]

        c3.milieu = True

        self.i_d = 7

        self.pos=1

        self.active = True

        for l in self.case:
            for case in l:

                if case.o:
                    fin_jeu()

                case.c = "#2BFAFA"

                case.active=True
                case.o = True

        self.nouvelle_col_ligne4=[(-1,0),(0,-1),(0,0),(0,1)]
        self.nouvelle_col_ligne3=[(-1,0),(0,-1),(0,0),(1,0)]
        self.nouvelle_col_ligne2=[(0,-1),(0,0),(0,1),(1,0)]
        self.nouvelle_col_ligne1=[(-1,0),(0,0),(0,1),(1,0)]

    def position(self):
        """méthode qui gère les différentes positions de la pièce:

            #        #                      #
          # @ #  ou  @ #  ou  # @ #  ou   # @
                     #          #           #
        """

        global tableau_case

        for l in self.case:
            for case in l:
                if case.milieu:
                    case_milieu = case
                    couleur = case.c

        if self.pos==1:
            # on vérifie que la pièce ne soit pas trop en bas.
            if case_milieu.ligne < 26:
                if verif_si_piece(self.nouvelle_col_ligne1, case_milieu):
                    changement_position(self, self.nouvelle_col_ligne1, case_milieu, couleur)
                    self.pos=2


        elif self.pos==2:
            # on vérifie que la pièce ne soit pas trop à gauche.
            if 0 < case_milieu.col:
                if verif_si_piece(self.nouvelle_col_ligne2, case_milieu):
                    changement_position(self, self.nouvelle_col_ligne2, case_milieu, couleur)
                    self.pos=3

        elif self.pos==3:
            # on vérifie que la pièce ne soit pas trop en haut.
            if 0 < case_milieu.ligne:
                if verif_si_piece(self.nouvelle_col_ligne3, case_milieu):
                    changement_position(self, self.nouvelle_col_ligne3, case_milieu, couleur)
                    self.pos=4

        elif self.pos==4:
            # on vérifie que la pièce ne soit pas trop à droite.
            if case_milieu.col < 9:
                if verif_si_piece(self.nouvelle_col_ligne4, case_milieu):
                    changement_position(self, self.nouvelle_col_ligne4, case_milieu, couleur)
                    self.pos=1

# # # # # # # # # # # # # # fonction # # # # # # # # # #

def verif_si_piece(tableau, case_milieu):
    """ cette fonction vérifie qu'il n'y a pas de pièce déjà présente où seront les nouvelles cases de la pièce.
    """
    continuer = True
    for coord in tableau:
        i=coord[0]
        y=coord[1]
        # si une case de la futur position est déjà occupé par une piece
        if tableau_case[case_milieu.ligne+i][case_milieu.col+y].o:
            # si une piece l'occuppe, et si elle ne fais pas partie de la piece active (celle en cours de traitement)
            if not tableau_case[case_milieu.ligne+i][case_milieu.col+y].active:
                continuer=False
    return continuer

def changement_position(piece, tab, case_milieu, couleur):
    """ cette fonction change la position d'une piece en modifiant sa matrice de cases et les cases de tableau_case

    tab est un tableau contenant des tuples de coordonnées
    """

    global tableau_case

    # on appelle une fonction qui va réinitialiser toutes les cases de la pièce
    reset_case_piece()

    # on reset la matrice contenant les pièces de la fonction
    piece.case= []

    for coord in tab:
        i=coord[0]
        y=coord[1]

        tableau_case[case_milieu.ligne+i][case_milieu.col+y].o = True
        tableau_case[case_milieu.ligne+i][case_milieu.col+y].c = couleur

        # comme les 5 premières lignes (de 0 à 4) sont invisible, elles n'ont pas de canvas donc on ne doit pas les modifiers
        if tableau_case[case_milieu.ligne+i][case_milieu.col+y].ligne >4:
            tableau_case[case_milieu.ligne+i][case_milieu.col+y].can.config(bg=couleur)

        tableau_case[case_milieu.ligne+i][case_milieu.col+y].active=True

    # comme les matrices sont triés lignes par lignes (de haut en bas), puis de gauche à droite, et que un tableau dans la matrice correspond à une ligne,
    # alors à chaque fois que tab[i][0] est différents de tab[i-1][0], on a changer de ligne, donc on doit rajouter un tableau dans la matrice

    piece.case.append([])
    # x sert à savoir dans quel tableau de la matrice on doit ajouter une case, il est donc incrémenté à chaque fois que lon rajoute un tableau.
    x=0

    for i in range (len(tab)):
        if i != 0:
            if tab[i][0] != tab[i-1][0]:
                piece.case.append([])
                x+=1
        piece.case[x].append(tableau_case[case_milieu.ligne+tab[i][0]][case_milieu.col+tab[i][1]])

def fonction_score_niveau(nouvelle_ligne=False):
    """ cette fonction sert à gérer les niveaux, lignes et le score
    """
    global vitesse

    # si on appelle la fonction avec comme parametre nouvelle_ligne = True, le score gagne 100 et le nombre de ligne augmente de 1
    if nouvelle_ligne:
        score.set(int(score.get()) + 100)
        score_phrase.set(" Score : {}  ".format(score.get()))

        ligne.set(int(ligne.get())+1)
        ligne_phrase.set(" Ligne : {} / 5 ".format(ligne.get()))

    #sinon, le score gagne un nombre équivalent au niveau
    else:
        score.set(int(score.get())+ int(niveau.get()))
        score_phrase.set(" Score : {}  ".format(score.get()))

    # si on as complétés 5 lignes
    if int(ligne.get()) == 5:
        ligne.set(0)
        ligne_phrase.set(" Ligne : {} / 5 ".format(ligne.get()))
        niv = int(niveau.get())

        # si on arrive au niveau 5 on change de music
        if niv + 1 == 5:
            pygame.mixer.music.load(directory + r"\theme2.wav")
            pygame.mixer.music.play(-1)

        # si on arrive au niveau 10 on change de music
        if niv + 1 == 10:
            pygame.mixer.music.load(directory + r"\level10.wav")
            pygame.mixer.music.play(-1)

        # on gagne 1 niveau
        niveau.set(niv +1)
        niveau_phrase.set(" Niveau : {}  ".format(niveau.get()))

        # on augmente la vitesse de 50 milisecondes si on a pas atteint le niveau 10
        if niv + 1 <=10:
            vitesse -= 50

def ligne_fonction():
    """ fonction qui va gérer les lignes pleines, c'est à dire les supprimer une par une
    """
    global tableau_case, all_piece, ligne_pleine, score

    # on initialize le numéro de ligne pleine à 100 --> il n'y en a pas
    ligne_pleine = 100

    # on parcours les lignes du bas en haut
    for l in range(len(tableau_case)-1,-1,-1):
        c=0
        for case in tableau_case[l]:
            if case.o and not case.active:
                c+=1
        # si les 10 cases de la ligne font parties d'une pièce, mais pas de la pièce active
        if c == 10 :
            # on enregistre le numéro de la ligne pleine
            ligne_pleine = l

            break

    # si une ligne est pleine
    if ligne_pleine != 100:

        # on mets à jour le score / nombre de ligne / niveau
        fonction_score_niveau(nouvelle_ligne=True)

        # on réinitialize les cases de la ligne
        for case in tableau_case[ligne_pleine]:
            case.c = '#555B61'
            case.can.config(bg='#555B61')
            case.active=False
            case.o = False
            case.milieu=False

        # on parcours toutes les pièces du jeu
        for piece in all_piece:

            t=0
            tmax = len(piece.case)

            # on parcours ligne par ligne notre tableau_case
            while t < tmax:

                # imax = nombre de case appartenant à la piece sur la ligne de piece.case[t]
                imax=len(piece.case[t])

                # on commence à parcours à gauche, donc à l'indice 0
                i=0

                # on parcours les colonnes de la matrice des cases de la pièce
                while i < imax:

                    # on supprimme toutes les cases qui font parties de la ligne pleine
                    if piece.case[t][i].ligne==ligne_pleine:
                        # les cases ont étés réinitialiser mais elles sont encore présentes dans la matrice des cases de la piece
                        del piece.case[t][i]

                        # comme on viens de supprimer une pièce de la ligne, on soustrait 1 au nombre de pièce dans la ligne
                        imax-=1
                        i-=1
                    i+=1
                t+=1

        # on parcours toutes les pièces du jeu
        for piece in all_piece:
            if not piece.active:

                # on parcours du bas de la piece au haut de la piece
                for i in range(len(piece.case)-1,-1,-1):
                    # on parcours de gauche à droite
                    for y in range(len(piece.case[i])):

                        ligne = piece.case[i][y].ligne

                        # si la ligne de la case est au dessus de la ligne pleine
                        if ligne < ligne_pleine:
                            # on déplace ici la ligne d'une ligne vers le bas

                            col = piece.case[i][y].col
                            c = piece.case[i][y].c
                            milieu = piece.case[i][y].milieu

                            tableau_case[ligne+1][col].c = c
                            tableau_case[ligne+1][col].can.config(bg=c)
                            tableau_case[ligne+1][col].o = True
                            tableau_case[ligne+1][col].milieu = milieu

                            piece.case[i][y] = tableau_case[ligne+1][col]

                            tableau_case[ligne][col].c = '#555B61'
                            tableau_case[ligne][col].can.config(bg='#555B61')
                            tableau_case[ligne][col].o = False
                            tableau_case[ligne][col].milieu = False

        # on joue un effet sonore
        son = pygame.mixer.Sound(directory + r"\ligne.wav")
        son.set_volume(0.5)
        son.play()


    # on appelle une fonction qui supprimme les pièces qui n'ont plus de case
    verif_piece()


def verif_piece():
    """fonction qui supprimme les pièces qui n'ont plus de case
    """
    global all_piece

    # on parcours les pièces du tableau contenant toutes les pièces
    i=0
    imax=len(all_piece)

    while i < imax:
        c=0

        # on parcours la pièce de haut en bas
        for t in all_piece[i].case:
            for case in t:
                c+=1

        # si la pièce ne possède pas de case on la supprimme
        if c == 0:
            del all_piece[i]
            i-=1
            imax-=1
        i+=1

def move():
    """ fonction qui fais bouger les pieces et qui s'execute toute les x secondes (x=vitesse)"""
    global tableau_case, all_piece, ligne_pleine, fonction_bas_bool, vitesse

    if not fonction_bas_bool:

        # on vérifie qu'il n'y ai pas de ligne pleine
        ligne_fonction()

        # on vérifie si on a perdu
        verif_fin_jeu()

        if ligne_pleine == 100:

            # on appelle une fonction qui fera descendre la pièce active d'une ligne et qui renvoie 1 si il reste une pièce active et 0 sinon dans un tuple
            compte_active=descendre_active()[0]

            # si il n'y a plus de piece active, on en fais spawn une autre
            if compte_active == 0:
                random_piece()

    # on rappelle cette fonction dans 'vitesse' milisecondes
    root.after(vitesse, move)

def verif_fin_jeu():
    global tableau_case, all_piece

    # si une pièce autre que la piece active possede une case dans une ligne invisible (ligne 0 à 4), alors on arretes le jeu car le joueur a perdu
    for piece in all_piece:
        if not piece.active:
            for l in piece.case:
                for case in l:
                    if case.ligne <5:
                        fin_jeu()

def descendre_active():
    """ fonction qui fera descendre la pièce active d'une ligne
    """
    global tableau_case, all_piece, reserve_booleen

    continuer = True

    compte_active=0

    for piece in all_piece:
        if piece.active:

            compte_active=1

            # on vérifie des prérequis

            # on parcours du bas de la piece au haut de la piece
            for i in range(len(piece.case)-1,-1,-1):
                for y in range(len(piece.case[i])):

                    # si la pièce est sur la dernière ligne, donc si elle ne peux pas descendre plus bas
                    if piece.case[i][y].ligne == 21+5:
                        continuer = False

                    ligne = piece.case[i][y].ligne
                    col = piece.case[i][y].col

                    if continuer:

                        # si la prochaine case fais partie d'une piece
                        if tableau_case[ligne+1][col].o:
                            # si la case ne fais pas partie de la piece active
                            if not tableau_case[ligne+1][col].active:
                                continuer = False

            if continuer:

                # on parcours du bas de la piece au haut de la piece
                for i in range(len(piece.case)-1,-1,-1):
                    for y in range(len(piece.case[i])):

                        # on descends chaque case de la pièce d'une ligne

                        ligne = piece.case[i][y].ligne
                        col = piece.case[i][y].col
                        c = piece.case[i][y].c
                        milieu = piece.case[i][y].milieu

                        tableau_case[ligne+1][col].c = c
                        tableau_case[ligne+1][col].active=True
                        tableau_case[ligne+1][col].o = True
                        tableau_case[ligne+1][col].milieu = milieu

                        tableau_case[ligne][col].c = '#555B61'
                        tableau_case[ligne][col].active=False
                        tableau_case[ligne][col].o = False
                        tableau_case[ligne][col].milieu = False

                        piece.case[i][y] = tableau_case[ligne+1][col]

                        # les 5 premieres lignes étant invisibles, elles n'ont donc pas de canvas
                        if ligne > 3:
                            tableau_case[ligne+1][col].can.config(bg=c)
                        if ligne > 4:
                            tableau_case[ligne][col].can.config(bg='#555B61')

            else:
                # si les prérequis ne sont pas valides la pièce n'est plus active
                piece.active=False

                # on peut a nouveau ranger une piece dans la reserve si on ne pouvais pas avant
                reserve_booleen = False

                # on parcours du bas de la piece au haut de la piece
                for i in range(len(piece.case)-1,-1,-1):
                    for y in range(len(piece.case[i])):
                        piece.case[i][y].active=False
                compte_active = 0

    return (compte_active, continuer)


def bas(_):
    """ fonction qui descends la piece active au maximum si on touche sur la fleche du bas
    """
    global tableau_case, all_piece, ligne_pleine, fonction_bas_bool, reserve_booleen

    # fonction_bas_bool permettera à ne pas executer une fonction tant que le programme execute celle ci
    fonction_bas_bool = True

    if ligne_pleine == 100:
        continuer = True

        while continuer:

            continuer= descendre_active()[1]

    # on augmente notre score
    fonction_score_niveau()

    fonction_bas_bool = False


def gauche_droite(direction):
    """ fonction qui bouge la pièce active d'une colonne vers la gauche
    """
    global tableau_case, all_piece

    if direction.keysym == 'Left':
        x=-1
    elif direction.keysym == 'Right':
        x=1

    # on parcours toutes les pièces du tableau contenant toutes les pièces
    for piece in all_piece:
        if piece.active:

            continuer = True

            # on parcours la piece de gauche à droite et de haut en bas
            for l in piece.case:
                for case in l:
                    if x == -1:
                        if case.col == 0:
                            continuer = False
                    elif x == 1:
                        if case.col == 9:
                            continuer = False

            if continuer:

                # on parcours la piece de gauche à droite et de haut en bas
                for l in piece.case:
                    for case in l:
                        ligne = case.ligne
                        col = case.col
                        c = case.c

                        # si la case à gauche fais partie d'une piece
                        if tableau_case[ligne][col+x].o:
                            # si la case de fais pas partie de la piece active
                            if not tableau_case[ligne][col+x].active:
                                continuer = False

            # si les prérequis ci-dessus sont respectés
            if continuer:

                # on parcours la piece de gauche à droite et de haut en bas
                if x == -1:
                    for l in range(len(piece.case)):
                        # on parcours la matrice des cases de la piece de gauche à droite
                        for case in range(len(piece.case[l])):
                            # on bouge la case d'une case à gauche
                            gauche_droite_complement(piece,l,case,x)

                elif x == 1:
                    for l in range(len(piece.case)):
                        # on parcours la matrice des cases de la piece de droite à gauche
                        for case in range(len(piece.case[l])-1,-1,-1):
                            # on bouge la case d'une case à droite
                            gauche_droite_complement(piece,l,case,x)

def gauche_droite_complement(piece,l,case,x):
    """ fonction qui complete la fonction droite_gauche en bougeant la case en paramètre
    d'une case à droite ou d'une case à gauche
    """
    ligne = piece.case[l][case].ligne
    col = piece.case[l][case].col
    c = piece.case[l][case].c
    milieu = piece.case[l][case].milieu

    tableau_case[ligne][col+x].c = c
    tableau_case[ligne][col+x].active=True
    tableau_case[ligne][col+x].o = True
    tableau_case[ligne][col+x].milieu = milieu
    piece.case[l][case] = tableau_case[ligne][col+x]

    tableau_case[ligne][col].c = '#555B61'
    tableau_case[ligne][col].active=False
    tableau_case[ligne][col].o = False
    tableau_case[ligne][col].milieu = False

    if ligne > 4:
        tableau_case[ligne][col+x].can.config(bg=c)
        tableau_case[ligne][col].can.config(bg='#555B61')

def reset_case_piece(milieu_bool = False):
    """ fonction qui réinitialise toutes les cases de la pièce active
    cette fonction est utilisé dans le changement de position des pièces et pour la 'réserve'
    """
    global all_piece

    # on va reset les cases de la piece
    for piece in all_piece:
        if piece.active:

            # on parcours du bas de la piece au haut de la piece
            for i in range(len( piece.case)-1,-1,-1):
                for y in range(len( piece.case[i])):
                    ligne =  piece.case[i][y].ligne
                    col =  piece.case[i][y].col

                    # on réinitialize les information
                    tableau_case[ligne][col].c = '#555B61'
                    if ligne > 4:
                        tableau_case[ligne][col].can.config(bg='#555B61')
                    tableau_case[ligne][col].active=False
                    tableau_case[ligne][col].o = False

                    # lorsqu'on utilise cette fonction pour un changement de position on a pas besoin de réinitialisé le milieu car il ne bouge pas.
                    if milieu_bool:
                        tableau_case[ligne][col].milieu = False

def random_piece():
    """ fonction qui créer une pièce en choisissant aléatoirement entre les différentes pièces
    """
    global prochaine_piece

    # pour la premiere piece du jeu
    if not prochaine_piece:

        choix=random.randint(1,7)
        if choix == 1:
            all_piece.append(Piece1())
        if choix == 2:
            all_piece.append(Piece2())
        if choix == 3:
            all_piece.append(Piece3())
        if choix == 4:
            all_piece.append(Piece4())
        if choix == 5:
            all_piece.append(Piece5())
        if choix == 6:
            all_piece.append(Piece6())
        if choix == 7:
            all_piece.append(Piece7())

    else:
        # si on avait choisis à lavance la prochaine pièce, on la fais apparaître
        if prochaine_piece == 1:
            all_piece.append(Piece1())
        if prochaine_piece == 2:
            all_piece.append(Piece2())
        if prochaine_piece == 3:
            all_piece.append(Piece3())
        if prochaine_piece == 4:
            all_piece.append(Piece4())
        if prochaine_piece == 5:
            all_piece.append(Piece5())
        if prochaine_piece == 6:
            all_piece.append(Piece6())
        if prochaine_piece == 7:
            all_piece.append(Piece7())

    # on choisis la prochaine pièce
    prochaine_piece = random.randint(1,7)

    # on dessine la prochaine pièce
    dessiner_piece(tableau_case_a_venir, prochaine_piece)



def dessiner_piece(tab, i_d):
    """dessine la piece d'id = i_d dans le tableau de case en parametre"""

    # on réinitialize la couleur des canvas du tableau
    for i in tab:
        for case in i:
            case.can.config(bg='#888888')

    # on dessinne une pièce en fonction de l'i_d en paramètre
    if i_d == 1:
        tab[1][2].can.config(bg="#FF0000")
        tab[2][2].can.config(bg="#FF0000")
        tab[3][2].can.config(bg="#FF0000")
        tab[4][2].can.config(bg="#FF0000")
    if i_d == 2:
        tab[3][2].can.config(bg="#F7FF3C")
        tab[3][3].can.config(bg="#F7FF3C")
        tab[4][2].can.config(bg="#F7FF3C")
        tab[4][3].can.config(bg="#F7FF3C")
    if i_d == 3:
        tab[3][3].can.config(bg="#34C924")
        tab[3][4].can.config(bg="#34C924")
        tab[4][3].can.config(bg="#34C924")
        tab[4][2].can.config(bg="#34C924")
    if i_d == 4:
        tab[3][2].can.config(bg="#2C75FF")
        tab[3][3].can.config(bg="#2C75FF")
        tab[4][3].can.config(bg="#2C75FF")
        tab[4][4].can.config(bg="#2C75FF")
    if i_d == 5:
        tab[2][3].can.config(bg="#FF6600")
        tab[2][2].can.config(bg="#FF6600")
        tab[3][2].can.config(bg="#FF6600")
        tab[4][2].can.config(bg="#FF6600")
    if i_d == 6:
        tab[2][2].can.config(bg="#BB3385")
        tab[2][3].can.config(bg="#BB3385")
        tab[3][3].can.config(bg="#BB3385")
        tab[4][3].can.config(bg="#BB3385")
    if i_d == 7:
        tab[3][1].can.config(bg="#2BFAFA")
        tab[3][2].can.config(bg="#2BFAFA")
        tab[3][3].can.config(bg="#2BFAFA")
        tab[2][2].can.config(bg="#2BFAFA")

def fin_jeu():
    """ fonction qui arrètes le jeu si on perd
    """
    global tableau_case, all_piece, directory

    # on mets un effet sonore
    son = pygame.mixer.Sound(directory + r"\game_over.wav")
    son.set_volume(1)
    son.play()

    # le score est écrit dans un fichier texte
    with open(directory + r"\last_score.txt", "w") as f:
        f.write(score.get())

    # on execute le programme qui affiche le score, l'enregistre si besoin et qui peut également éxecuter ce programme
    os.startfile(directory + r"\score.py")

    # on enlève la musique
    pygame.mixer.music.stop()

    time.sleep(5)

    # on arrète le programme
    root.destroy()
    sys.exit()

def rotation(_):
    """ fonction qui appelle la méthode position de la pièce active
    """
    for piece in all_piece:
        if piece.active:
            piece.position()

def reserve(_):
    """ fonction qui gère la 'réserve'
    """
    global all_piece, tableau_reserve, piece_reserve, reserve_booleen

    # si on a pas déjà utilisé la réserve avant qu'une pièce active se pose
    if not reserve_booleen:
        spawn = False

        # si on a pas de pièce dans la réserve
        if piece_reserve == 0:
            spawn = True
        else:
            # sinon, on enregistre l'id de la pièce présente pour la faire spawn
            piece_a_spawn = piece_reserve

        # on dessinne la pièce active dans la réserve et on enregistre son id
        for piece in all_piece:
            if piece.active:
                i_d = piece.i_d
                dessiner_piece(tableau_reserve, i_d)

        # on reset les cases de la pièces active
        reset_case_piece(milieu_bool=True)

        # la pièce n'est plus active et sa matrice de case est vide
        for piece in all_piece:
            if piece.active:
                piece.active = False
                piece.case = []

        # la fonction va supprimer la pièce
        verif_piece()

        # on enregistre l'id de la pièce anciennement active dans la réserve
        piece_reserve = i_d

        # si aucune pièce n'était dans la réserve on en fais spawn une
        if spawn:
            random_piece()

        # sinon on fais spawn la pièce qui était dans la réserve
        else:
            if piece_a_spawn == 1:
                all_piece.append(Piece1())
            if piece_a_spawn == 2:
                all_piece.append(Piece2())
            if piece_a_spawn == 3:
                all_piece.append(Piece3())
            if piece_a_spawn == 4:
                all_piece.append(Piece4())
            if piece_a_spawn == 5:
                all_piece.append(Piece5())
            if piece_a_spawn == 6:
                all_piece.append(Piece6())
            if piece_a_spawn == 7:
                all_piece.append(Piece7())

        reserve_booleen = True



# # # # # # # # # # # # # # programme principale # # # # # # # #


# on crée notre fenêtre tkinter
root = Tk()
root.geometry("830x710")
root.configure(bg='#DDDDDD')

# on crée une 'frame' qui va contenir nos cases
frame_case=Frame(root)
frame_case.place(x=280, y=0)

# on crée une frame avec le score et le niveau
frame_score = Frame(root, bg='#DDDDDD', highlightthickness=4)
frame_score.config(highlightbackground='#000000')
frame_score.place(x=5,y=0)

score = StringVar()
score.set("0")
score_phrase = StringVar()
score_phrase.set(" Score : {}  ".format(score.get()))
label_score = Label(frame_score, textvariable = score_phrase, font = ("Lucida Grande", 30), bg = '#DDDDDD', fg='#000000')
label_score.pack()

niveau = StringVar()
niveau.set("1")
niveau_phrase = StringVar()
niveau_phrase.set(" Niveau : {} ".format(niveau.get()))
label_niveau = Label(frame_score, textvariable = niveau_phrase, font = ("Lucida Grande", 30), bg = '#DDDDDD', fg='#000000')
label_niveau.pack()

ligne = StringVar()
ligne.set("0")
ligne_phrase = StringVar()
ligne_phrase.set(" Ligne : {} / 5 ".format(ligne.get()))
label_ligne = Label(frame_score, textvariable = ligne_phrase, font = ("Lucida Grande", 30), bg = '#DDDDDD', fg='#000000')
label_ligne.pack()

# création de la frame 'pièce à venir'

frame_a_venir = Frame(root, bg='#DDDDDD', highlightthickness=4 )
frame_a_venir.config(highlightbackground='#000000')
frame_a_venir.place(x=620,y=0)

# création d'une matrice de cases
tableau_case_a_venir = []
for i in range(6):
    tableau_case_a_venir.append([])
    for y in range(6):
        tableau_case_a_venir[i].append(Case(i,y,frame_a_venir, '#888888'))

# création de la frame 'réserve'

frame_reserve = Frame(root, bg='#DDDDDD', highlightthickness=4 )
frame_reserve.config(highlightbackground='#000000')
frame_reserve.place(x=620,y=220)

# création d'une matrice de cases
tableau_reserve = []
for i in range(6):
    tableau_reserve.append([])
    for y in range(6):
        tableau_reserve[i].append(Case(i,y,frame_reserve, '#888888'))

piece_reserve = 0

# création de la matrice de cases principales
# les 5 première lignes de cases seront invisible

tableau_case=[]

for i in range(22+5):
    tableau_case.append([])
    for y in range(10):
        if i < 5:
            tableau_case[i].append(Case(i,y, frame_case,'#555B61',can=False))
        else:
            tableau_case[i].append(Case(i,y,frame_case, '#555B61'))

# partie son

# on enregistre le chemin du fichier en execution
directory = os.path.dirname(os.path.realpath(__file__))

pygame.mixer.init()

# on mets la première musique
pygame.mixer.music.load(directory + r"\theme1.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

# on initialize différentes variables

ligne_pleine=100
all_piece=[]
fonction_bas_bool = False
vitesse = 500
prochaine_piece = None
reserve_booleen = False

# on crée notre première pièce
random_piece()

move()

# on lie différentes fonctions à des touches

#--> si on appuie sur la flèche de gauche la fonction gauche va être appelé, etc
root.bind('<Left>', gauche_droite)
root.bind('<Right>', gauche_droite)
root.bind('<Up>', rotation)
root.bind('<Down>', bas)
root.bind('<Return>', reserve)

# mainloop mettera à jour la fenêtre tkinter
root.mainloop()
