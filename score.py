""" Ce programme s'execute seul quand on perds une partie de tetris
    il permets d'enregistrer nos scores dans un fichier texte, de les afficher et de relancer une partie de tetris
    pour enregistrer votre score il suffit de rentrer un pseudo puis de cliquer sur le bouton enregistrer
"""

from tkinter import *
import os

# on enregistre le chemin vers le dossier où est le fichier
directory = os.path.dirname(os.path.realpath(__file__))

# on ouvre le fichier texte contenant le score de la dernière partie joué
with open(directory + r"\last_score.txt", "r") as f:
        score = int(f.readlines()[0])

# on ouvre le fichier contenant tous les scores
try:
    with open(directory + r'\score_joueur.txt', 'r') as f:
        dico = f.readlines()[0]
        dico = eval(dico)

# mais si il y a une erreur, donc si le fichier est corrompu ou si il n'existe pas, on en crée un nouveau
except:
    with open(directory + r'\score_joueur.txt', 'w') as f:
        dico = {}
        f.write(str(dico))

# on initialise un booléen qui servira à savoir si le dernier score est un record
record = False

# on mets record à True si tous les scores du fichiers contenant tous les scores sont inférieurs au dernier score
for scores in dico.values():
    if score > scores:
        record = True

# on crée notre fenêtre tkinter
root = Tk()
root.geometry("600x500")
root.configure(bg='#DDDDDD')

# on fais apparaître une phrase différente si on a un record ou pas
if record :
    Label(root, text = 'Nouveau record !', font = ("Lucida Grande", 30), bg = '#DDDDDD', fg='#000000').pack(side = TOP,padx=5,pady=5)
else:
    Label(root, text = 'Essaye encore !', font = ("Lucida Grande", 30), bg = '#DDDDDD', fg='#000000').pack(side = TOP,padx=5,pady=5)

# on affiche le dernier score
Label(root, text = 'Score : {}'.format(score), font = ("Lucida Grande", 30), bg = '#DDDDDD', fg='#000000').pack(side = TOP,padx=5,pady=5)

# on crée l'endroit pour rentrer votre pseudo
Label(root, text = 'Votre pseudo :', font = ("Lucida Grande", 30), bg = '#DDDDDD', fg='#000000').pack(side = TOP,padx=5,pady=5)
entree = Entry(root, text = 'Pseudo', font = ("Lucida Grande", 30), bg = '#FFFFFF', fg='#000000')
entree.pack(padx=5,pady=5)

# si le joueur clique sur le bouton rejouer ce programme s'auto détruira après avoir executé le tetris
def rejouer():
    os.startfile(directory + r"\tetris.py")
    root.destroy()
    sys.exit()

# bouton rejouer
Button(root, text = 'rejouer', font = ("Lucida Grande", 30), bg = '#FFFFFF', fg='#000000',command=rejouer).pack(padx=5,pady=5)

# fonction qui enregistre le score du joueur si le joueur a rentré un pseudo
def save():
    global score
    pseudo = entree.get()

    if pseudo != "":
        dico[pseudo] = score

        with open(directory + r'\score_joueur.txt', 'w') as f:
            f.write(str(dico))

# bouton enregistrer
Button(root, text = 'enregistrer', font = ("Lucida Grande", 30), bg = '#FFFFFF', fg='#000000',command=save).pack(padx=5,pady=5)

# la fonction voir execute simplement le fichier texte contenant les scores
def voir():
    os.startfile(directory + r"\score_joueur.txt")

# bonton voir les scores
Button(root, text = 'Voir tous les scores', font = ("Lucida Grande", 20), bg = '#FFFFFF', fg='#000000',command=voir).pack(padx=5,pady=5)

root.mainloop()

