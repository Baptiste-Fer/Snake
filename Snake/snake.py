from fltk import *
from time import sleep
from random import randint

#images
FOND_MENU = 'IMAGE/fond_menu.png'
IMG_PARAMETRE = 'IMAGE/reglage1.png'
FOND_1 = 'IMAGE/fond_jeu1.png'
FOND_2 = 'IMAGE/fond_jeu2.png'
FOND_3 = 'IMAGE/fond_jeu3.png'
FOND_4 = 'IMAGE/fond_jeu4.png'
ICONE_FOND1 = 'IMAGE/icone_fond1.png'
ICONE_FOND2 = 'IMAGE/icone_fond2.png'
ICONE_FOND3 = 'IMAGE/icone_fond3.png'
ICONE_FOND4 = 'IMAGE/icone_fond4.png'
IMG_BLOCK = 'IMAGE/Block.png'
IMG_TITRE = 'IMAGE/titre.png'
IMG_FLECHE = 'IMAGE/fleche1.png'
IMG_zqsd = 'IMAGE/zqsd.png'

# dimensions du jeu
taille_case = 15
largeur_plateau = 40  # en nombre de cases
hauteur_plateau = 30  # en nombre de cases


def case_vers_pixel(case):
    """
    Fonction recevant les coordonnées d'une case du plateau sous la
    forme d'un couple d'entiers (id_colonne, id_ligne) et renvoyant les
    coordonnées du pixel se trouvant au centre de cette case. Ce calcul
    prend en compte la taille de chaque case, donnée par la variable
    globale taille_case.
    """
    i, j = case
    return (i + .5) * taille_case, (j + .5) * taille_case


def affiche_pommes(pommes):
    """
    Fonction recevant les coordonnées des pommes sous forme d'une liste
    de couples d'entiers. Elle convertit les coordonées à l'aide de la
    fonction case_vers_pixel puis dessine les pommes aux coordonées donées.
    """
    for pomme in pommes:
        x, y = case_vers_pixel(pomme)
        cercle(x, y, taille_case/2,
               couleur='darkred', remplissage='red', tag = 'refresh')
        rectangle(x-2, y-taille_case*.4, x+2, y-taille_case*.7,
                  couleur='darkgreen', remplissage='darkgreen',
                  tag = 'refresh')


def affiche_block(block):
    """
    Fonction recevant les coordonnées des blocs sous forme d'une liste
    de couples d'entiers. Elle convertit les coordonées à l'aide de la
    fonction case_vers_pixel puis dessine les blocs aux coordonées donées.
    """
    for bloc in block:
        x, y = case_vers_pixel(bloc)
        image(x, y, IMG_BLOCK, ancrage = 'center')


def affiche_serpent(serpent, couleur_serpent):
    """
        Fonction recevant les coordonnées des parties du serpent sous forme
        d'une liste de couples d'entiers (et une chaine de caratère pour sa 
        couleur. Elle convertit les coordonées à l'aide de la fonction
        case_vers_pixel puis dessine les parties du serpents aux coordonées
        donées.
    """
    for rond in range(len(serpent)):
        x, y = case_vers_pixel(serpent[rond])
 
        cercle(x, y, taille_case/2 + 1,
               couleur='black', remplissage=couleur_serpent, tag = 'refresh')


def change_direction(direction, touche):
    """
    Fonction recevant une direction sous forme d'un couple d'entier, et
    une valeur d'une touche, sous forme de chaine de caractères. Elle permet
    de convertir la touche utiliser en une direction, elle renvoie ainsi
    cette nouvelle direction.
    """
    if touche == 'Up' and direction != (0, 1):
        # flèche haut pressée
        return (0, -1)
    elif touche == 'Down' and direction != (0, -1):
        return (0, 1)
    elif touche == 'Left' and direction != (1, 0):
        return (-1, 0)
    elif touche == 'Right' and direction != (-1, 0):
        return (1, 0)
    else:
        # pas de changement !
        return direction

def change_direction_2(direction_2, touche):
    """
    Fonction identique à change_direction mais avec  des touches différentes,
    afin d'avoir deux directions différentes avec 2 commandes différentes.'
    """
    if touche == 'z' and direction_2 != (0, 1):
        return (0, -1)
    elif touche == 's' and direction_2 != (0, -1):
        return (0,1)
    elif touche == 'q' and direction_2 != (1, 0):
        return (-1, 0)
    elif touche == 'd' and direction_2 != (-1, 0):
        return (1, 0)
    else:
        # pas de changement !
        return direction_2


def moove_serpent(serpent_, direction_, ieme_serpent) :
    """
    Fonction recevant 2 listes de couples d'entier, pour former 2 listes
    de coordonnées et recevant aussi un couple d'entier qui réprésente la
    direftion. Cette fonction permet de mettre fin à la partie en renvoyant
    une chaine de caractère. Elle detecte, à l'aide d'une simulation si le
    serpent touche une bordure, se touche lui-même, touche un bloc ou un
    autre serpent. Elle permet aussi, de supprimer une pommes en contact
    et de modiifer la taille du serpent.
    """
    x_tete, y_tete = serpent_[-1]
    simul_x = x_tete + direction_[0]
    simul_y = y_tete + direction_[1]
    simul = (simul_x, simul_y)

    if simul_x < 0 or simul_x > 39 or simul_y > 29 or simul_y < 0: #bordure
        return 'perdu'
    elif simul in serpent_ and len(serpent_) > 1: #se touche lui-même
        return 'perdu'

    elif simul in pommes: #touche une pommme
        pommes.remove(simul)
    elif simul in block or simul in ieme_serpent: # touche un bloc ou le 2eme
        return 'perdu'
    else :
        serpent_.pop(0)
    serpent_.append(simul) #On ajoute la tête prevu par simul


def ajouter_pomme():
    """
    Fonction qui permet créer aléatoirement un couple d'entier qui
    n'appartient à aucun élément du programme, et de l'ajouter à la liste
    contenant les coordonées des pommes.
    """
    while True:
        test = (randint(0, 39), randint(0, 29))
        if test not in serpent and test not in pommes and test not in block \
                and  test not in serpent_2:
            pommes.append(test)
            return


def ajouter_block():
    """
    Fonction qui permet créer aléatoirement un couple d'entier qui
    n'appartient à aucun élément du programme, et de l'ajouter à la liste
    contenant les coordonées des blocs.
    """
    while True:
        test = (randint(0, 39), randint(0, 29))
        if test not in serpent and test not in pommes and test not in block \
            and  test not in serpent_2 :
            block.append(test)
            return


def affiche_score (serpent1, serpent2, mode):
    """
    Focntion recevant 2 listes de couples de coordonnées (couple d'entier),
    et une chaine de caractère qui représente le mode de jeu.
    Elle permet de calculer et afficher le score du ou des joueurs, ainsi que
    de les cacher si un serpent passe dans l'affichage.
    """
    score1 = len(serpent1)-1
    score2 = len(serpent2)-1

    L = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0),
         (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0),
         (23, 0), (24, 0), (25, 0), (26, 0), (27, 0), (28, 0), (29, 0)]
    cacher = False
    for couple in L:  
        if couple in serpent1 or couple in serpent2:
            cacher = True
    if cacher == False and mode == 'Solo':
       texte(0, 0, 'Score :'+str(score1), couleur = 'black',
       taille = 12, tag = 'refresh')
       return score1
    elif cacher == False and mode != 'Solo':
        texte(150, 0, 'Joueur 1 > '+str(score1), couleur = 'black',
               taille = 12, tag = 'refresh')
        texte(350, 0, 'Joueur 2 > '+str(score2), couleur = 'black',
               taille = 12, tag = 'refresh')
    return score1, score2



def clique():
    """
    Fonction qui permet de recevoir la valeur d'une touche de l'utilisateur
    dans les menus, et de savoir si l'action est utilisable dans le programme.
    Elle sert à détecter si un clic et sur un bouton, et renvoie une chaine 
    de carectères permentant de savoir l'action à faire.'
    """
    ev = attend_ev()
    ty = type_ev(ev)
    if menu == 'Menu':
        if ty == 'Quitte':
            return 'quitte'
        elif ty == 'ClicGauche' and abscisse(ev) > 200 and abscisse(ev) < 400 \
                and ordonnee(ev) > 290 and ordonnee(ev) < 390 :
            return 'pregame'

        #Clic bouton difficulté
        elif ty == 'ClicGauche' and abscisse(ev) >100 and abscisse(ev) < 120 \
                and ordonnee(ev) > 220 and ordonnee(ev) < 250 \
                and diff == 'Normal':
           return 'Facile'
        elif ty == 'ClicGauche' and abscisse(ev) >100 and abscisse(ev) < 120 \
                and ordonnee(ev) > 220 and ordonnee(ev) < 250 \
                and diff == 'Difficile':
            return 'Normal'
        elif ty == 'ClicGauche' and abscisse(ev) > 100 and abscisse(ev) < 120 \
                and ordonnee(ev) > 220 and ordonnee(ev) < 250 \
                and diff == 'Facile':
            return 'Difficile'
        elif ty == 'ClicGauche' and abscisse(ev) > 230\
                and abscisse(ev) < 250 and ordonnee(ev) > 220 and \
                ordonnee(ev) < 250 and diff == 'Normal':
            return 'Difficile'
        elif ty == 'ClicGauche' and abscisse(ev) > 230\
                and abscisse(ev) < 250 and ordonnee(ev) > 220 and \
                ordonnee(ev) < 250 and diff == 'Difficile':
            return 'Facile'
        elif ty == 'ClicGauche' and abscisse(ev) > 230\
                and abscisse(ev) < 250 and ordonnee(ev) > 220 and \
                ordonnee(ev) < 250 and diff == 'Facile':
            return 'Normal'

        #Clic Bouton Mode
        elif ty == 'ClicGauche' and abscisse(ev) > 350 and abscisse(ev) < 370 \
                and ordonnee(ev) > 220 and ordonnee(ev) < 250\
                and mode == 'Solo':
            return '2 joueurs'
        elif ty == 'ClicGauche' and abscisse(ev) > 480 and abscisse(ev) < 500 \
                and ordonnee(ev) > 220 and ordonnee(ev) < 250\
                and mode == 'Solo':
            return '2 joueurs'
        elif ty == 'ClicGauche' and abscisse(ev) > 350 and abscisse(ev) < 370 \
                and ordonnee(ev) > 220 and ordonnee(ev) < 250\
                and mode == '2 joueurs':
            return 'Solo'
        elif ty == 'ClicGauche' and abscisse(ev) > 480 and abscisse(ev) < 500 \
                and ordonnee(ev) > 220 and ordonnee(ev) < 250\
                and mode == '2 joueurs':
            return 'Solo'
        elif ty == 'ClicGauche' and abscisse(ev) > 455 and abscisse(ev) < 505\
                and ordonnee(ev) > 340 and ordonnee(ev) < 388:
            return 'parametre'
        else:
            return 'Menu'

        #Menu défaite
    if ty == 'Quitte':
            return 'quitte'
    elif menu == 'perdu' :
        if ty == 'ClicGauche' and abscisse(ev) > 200 and abscisse(ev) < 390 \
                and ordonnee(ev) > 290 and ordonnee(ev) < 390 :
            return 'play'
        elif ty == 'ClicGauche' and abscisse(ev) > 200 and abscisse(ev) < 400\
                and ordonnee(ev) > 200 and ordonnee(ev) < 270:
            return 'Menu'
        else:
            return 'perdu'

        #Menu paramètre
    elif menu == 'parametre':
        if ty == 'Quitte':
            return 'quitte'
        elif ty == 'ClicGauche' and abscisse(ev) > 60 and abscisse(ev) < 110\
                and ordonnee(ev) > 50 and ordonnee(ev) < 86:
            return 'Menu'
        elif ty == 'ClicGauche' and abscisse(ev) > 60 and abscisse(ev) < 160\
                and ordonnee(ev) > 130 and ordonnee(ev) < 200 :
            return 'fond_jeu1'
        elif ty == 'ClicGauche' and abscisse(ev) > 187 and abscisse(ev) < 287\
                and ordonnee(ev) > 130 and ordonnee(ev) < 200 :
            return 'fond_jeu2'
        elif ty == 'ClicGauche' and abscisse(ev) > 312 and abscisse(ev) < 412\
                and ordonnee(ev) > 130 and ordonnee(ev) < 200 :
            return 'fond_jeu3'
        elif ty == 'ClicGauche' and abscisse(ev) > 440 and abscisse(ev) < 540\
                and ordonnee(ev) > 130 and ordonnee(ev) < 200 :
            return 'fond_jeu4'
        elif ty == 'ClicGauche' and abscisse(ev) > 60 and abscisse(ev) < 160\
                and ordonnee(ev) > 260 and ordonnee(ev) < 330:
            return 'serpent_vert'
        elif ty == 'ClicGauche' and abscisse(ev) > 187 and abscisse(ev) < 287\
                and ordonnee(ev) > 260 and ordonnee(ev) < 330:
            return 'serpent_rouge'
        elif ty == 'ClicGauche' and abscisse(ev) > 312 and abscisse(ev) < 412\
                and ordonnee(ev) > 260 and ordonnee(ev) < 330:
            return 'serpent_bleu'
        elif ty == 'ClicGauche' and abscisse(ev) > 440 and abscisse(ev) < 540\
                and ordonnee(ev) > 260 and ordonnee(ev) < 330:
            return 'serpent_violet'
        
        #menu avant-partie
    elif menu == 'pregame':
        if ty == 'Quitte':
            return 'quitte'
        elif touche(ev) == 'space':
            return 'play'
                
def bouton_play(txt, x, y):
    """
    Fonction recevant une chaine de caractère, et 2 entiers.
    Elle permet de créer un bouton avec le texte rentrant dedans, avec
    les coordonées données. ELle est utiliser pour créer le bouton jouer 
    et rejouer.
    """
    rectangle(200, 290, 400, 390, couleur = 'black', remplissage = 'red',
              epaisseur = 1)
    texte(x, y, txt, couleur = 'black', taille = 27)


def bouton_difficulte(diff):
    """
    Focntion recevant une chaine de carectère qui représente la difficulté.
    Elle permet de créer un bouton affichant la difficulté, et de changer 
    la couleur en fonction de cette dernière.
    """
    rectangle(100, 200, 250, 270, remplissage = 'green')   #Bouton Difficulté
    if diff == 'Facile':
        color = 'lightblue'
    elif diff == 'Normal':
        color = 'black'
    else :
        color = 'red'
    texte(175, 235, diff, couleur = color, taille = 20, ancrage = 'center')
    #rectangle(230, 220, 250, 250)  #Bouton fleche droite
    #rectangle(100, 220, 120, 250)  #Bouton fleche gauche
    fleche_d = [(235, 225),(235, 245), (245, 235)]
    fleche_g = [(115, 225), (115, 245), (105, 235)]
    polygone(fleche_d , remplissage = 'black')
    polygone(fleche_g , remplissage = 'black')
    

def bouton_mode(mode):  
    """
    Focntion recevant une chaine de caractères qui réprésente le mode.
    Elle permet de créer un bouton affichant le mode.
    """
    rectangle(350, 200, 500, 270, remplissage = 'green')
    texte(425, 235, mode, couleur = 'black', taille = 20, ancrage = 'center')
    #rectangle(480, 220, 500, 250)  #Bouton fleche droite
    #rectangle(350, 220, 370, 250)  #Bouton fleche gauche
    fleche_d = [(485, 225), (485, 245), (495, 235)]
    fleche_g = [(365, 225), (365, 245), (355, 235)]
    polygone(fleche_d , remplissage = 'black')
    polygone(fleche_g , remplissage = 'black')

def menu_pre_game(FOND, mode):
    """
    Fonction recevant 2 chaines de caractères, qui représentent le fond 
    d'écran et le mode de jeu. Elle dessine un affichage de avant-partie où
    il est indiqué le but et les touches.
    """
    image(300, 225, FOND, ancrage = 'center')
    texte(300, 70, '\tVotre but :\n Mangez le plus de pommes !',
          couleur = 'red', taille = 20, ancrage = 'center')
    texte(300, 400, 'Appuyer sur Espace pour lancer',
          couleur = 'black', taille = 20, ancrage = 'center')
    #rectangle(200, 200, 400, 350)
    if mode == 'Solo':
        image(300, 275, IMG_FLECHE, ancrage = 'center')
    else :
        image(100, 275, IMG_FLECHE, ancrage = 'center')
        image(500, 290, IMG_zqsd, ancrage = 'center')
        texte(50, 220, 'Joueur 1', taille = 16, ancrage = 'center')
        texte(550, 220, 'Joueur 2', taille = 16, ancrage = 'center')
        


def MENU(diff, mode):
    """
    Fonction recevant 2 chaines de caractères qui réprésentent la difficultés,
    ainsi que le mode.
    ELle permet d'afficher un menu possédant des images et des boutons.
    """
    image(300, 225, FOND_MENU, ancrage = 'center')
    cercle(480, 364, 23, couleur = 'beige', remplissage = 'beige')
    image(480, 365, IMG_PARAMETRE, ancrage = 'center') #Reglage
    image(307, 115, IMG_TITRE, ancrage = 'center') #Titre
    texte(60, 410, 'GRANDI Mathieu, FERNANDES Baptiste', taille = 6)
    bouton_play('PLAY', 255, 320)
    bouton_difficulte(diff)
    bouton_mode(mode)
    
    
def MENU_param():
    """
    Fonction créant une interface ou permetant de choisir des détails 
    graphiques avec des boutons et des images.
    """
    image(300, 225, FOND_MENU, ancrage = 'center')
    texte(300, 77, "Fond d'écran", ancrage = 'center', taille = 19)
    ligne(54, 100, 549, 100, epaisseur = 5)

    rectangle(60, 130, 160, 200, epaisseur = 3)
    rectangle(187, 130, 287, 200, epaisseur = 3)
    rectangle(312, 130, 412, 200, epaisseur = 3)
    rectangle(440, 130, 540, 200, epaisseur = 3)
    #image fond
    ligne(54, 230, 549, 230, epaisseur = 5)
    image(110, 166, ICONE_FOND1, ancrage = 'center')
    image(237, 166, ICONE_FOND2, ancrage = 'center')
    image(312, 130, ICONE_FOND3, ancrage = 'nw')
    image(440, 130, ICONE_FOND4, ancrage = 'nw')

    #Bouton retour menu
    rectangle(80, 63, 110, 73, remplissage = 'black')
    fleche = [(80, 53), (80, 83), (60, 67)]
    polygone(fleche, remplissage = 'black')

    rectangle(60, 260, 160, 330, epaisseur = 3, remplissage = 'black')
    rectangle(187, 260, 287, 330, epaisseur = 3, remplissage = 'black')
    rectangle(312, 260, 412, 330, epaisseur = 3, remplissage = 'black')
    rectangle(440, 260, 540, 330, epaisseur = 3, remplissage = 'black')
    ligne(54, 360, 549, 360, epaisseur = 5)
    texte(300, 380, "Couleur du serpent", ancrage = 'center', taille = 19)
    x = 80
    y = 295
    for i in range(3):
        x += 15
        cercle(x, y, taille_case/2 + 1, couleur='black', remplissage='green')
    x = 207
    for i in range(3):
        x += 15
        cercle(x, y, taille_case/2 + 1, couleur='black', remplissage='red')
    x = 332
    for i in range(3):
        x += 15
        cercle(x, y, taille_case/2 + 1, couleur='black', remplissage='blue')
    x = 460
    for i in range(3):
        x += 15
        cercle(x, y, taille_case/2 + 1, couleur='black', remplissage='purple')


    
def MENU_perdu(mode, serpent, serpent_2):
    """
    Fonction recevant une chaine de caractère, ainsi que 2 listes de couples 
    d'entier, représentant le mode, et les coordonnées des 2 serpents.
    Elle permet d'afficher un menu de défaite qui affiche le ou les scores,
    un message, ainsi que 2 boutons.'
    """
    image(300, 225, FOND_MENU, ancrage = 'center')
    bouton_play('REJOUER',217, 320)
    #Affichage Score
    if mode == 'Solo':
        score = affiche_score(serpent, serpent_2, mode)
        if score == (0,0):
            score = 0
        texte(300, 130, 6*" "+"Fin de partie !\nVotre score est de : "\
              +str(score), couleur = 'black',ancrage = 'center', taille = 26)
    else :
        score_1, score_2 = affiche_score(serpent, serpent_2, mode)
        if score_1 > score_2 :
            texte(305, 120, "Le joueur 1 gagne !\n "+\
              str(score_1) + " points / " + str(score_2) + " points", \
              couleur = 'black',ancrage = 'center', taille = 20)
        elif score_2 > score_1 :
            texte(305, 120, "Le joueur 2 gagne !\n "+\
              str(score_2) + " points / " + str(score_1) + " points", \
              couleur = 'black',ancrage = 'center', taille = 20)
        elif score_2 == score_1:
             texte(300, 120, "     Egalité !\n avec " + str(score_1) \
                   + " points",
              couleur = 'black', ancrage = 'center', taille = 20)      
    #Bouton Menu
    rectangle(200, 200, 400, 270, remplissage = 'green')
    texte(300, 235, 'MENU', ancrage = 'center')


# programme principal
if __name__ == "__main__":

    menu = 'Menu'
    cree_fenetre(taille_case * largeur_plateau,
                     taille_case * hauteur_plateau)
    # Difficulté, mode, fond d'écran  et couleur du serpent par défaut.
    diff = 'Normal'
    mode = 'Solo'   
    FOND = FOND_1
    couleur_serpent = 'green'
    while menu != 'quitte': #Boucle du programme

        while menu == 'Menu': #Boucle du menu principal
            efface_tout()
            MENU(diff, mode)
            clic = clique()
            if clic == 'Facile' or clic == 'Normal'\
                    or clic == 'Difficile':
                diff = clic     
            elif clic == 'Solo' or clic == '2 joueurs':
                mode = clic
            elif clic == 'pregame' or clic == 'Menu' or clic == 'quitte' :
                menu = clic
            elif clic == 'parametre':
                menu = 'parametre'
            mise_a_jour()
        

        while menu == 'parametre': # Boucle de l'interface paramètre
            efface_tout()
            MENU_param()
            clic = clique()
            if clic == 'Menu' or clic == 'quitte':
                menu = clic
            elif clic == 'fond_jeu1':
                FOND = FOND_1
            elif clic == 'fond_jeu2':
                FOND = FOND_2
            elif clic == 'fond_jeu3':
                FOND = FOND_3
            elif clic == 'fond_jeu4':
                FOND = FOND_4
            elif clic == 'serpent_vert':
                couleur_serpent = 'green'
            elif clic == 'serpent_rouge':
                couleur_serpent = 'red'
            elif clic == 'serpent_bleu':
                couleur_serpent = 'blue'
            elif clic == 'serpent_violet':
                couleur_serpent = 'purple'
            mise_a_jour()


        while menu == 'pregame':
            efface_tout()
            menu_pre_game(FOND, mode)
            mise_a_jour()
            clic = clique()
            if clic == 'quitte' or clic == 'play':
                menu = clic
            

        while menu == 'play' :    #Boucle de la partie
            # initialisation du jeu
            efface_tout()
            if diff != 'Facile':
                framerate = 8  # taux de rafraîchissement du jeu en images/s
            else :
                framerate = 5 # ips en facile
            direction = (0, 0)  # direction initiale du serpent
            if mode == '2 joueurs':
                direction_2 = (0, 0)
                serpent = [(0, 15)]
            else:
                serpent = [(0, 0)] # liste des coordonnées de cases
            serpent_2 = [(39, 15)]
                                    #adjacentes décrivant le serpent
            pommes = [] # liste des coordonnées des cases contenant des pommes
            block = []
            image(300, 225, FOND, ancrage = 'center')

            # boucle principale

            cmpt_pommes = 0
            cmpt_block = 0
            cmpt_speed = 0
            jouer = True
            while jouer:
                # affichage des objets
                efface('refresh')
                affiche_pommes(pommes)
                affiche_block(block)
                affiche_serpent(serpent, couleur_serpent)
                if mode == '2 joueurs':
                    affiche_serpent(serpent_2, couleur_serpent)
                affiche_score(serpent, serpent_2, mode)
                mise_a_jour()

                # gestion des événements
                ev = donne_ev()
                ty = type_ev(ev)
                if ty == 'Quitte':
                    menu = 'quitte'
                    break
                elif ty == 'Touche':
                    direction = change_direction(direction, touche(ev))
                    if mode == '2 joueurs':
                        direction_2 = change_direction_2\
                        (direction_2, touche(ev))
                if moove_serpent(serpent, direction, serpent_2) == 'perdu':
                    menu = 'perdu'
                    break
                if mode == '2 joueurs':
                    if moove_serpent(serpent_2, direction_2, serpent)\
                        == 'perdu':
                        menu = 'perdu'
                        break
                if cmpt_pommes == 15:
                    ajouter_pomme()
                    cmpt_pommes = 0
                if cmpt_block == 30 and diff != 'Facile':
                    ajouter_block()
                    cmpt_block = 0
                if cmpt_speed == 60 and diff == 'Difficile':
                    framerate += 1
                    cmpt_speed = 0
                # attente avant rafraîchissement
                sleep(1/framerate)

                cmpt_pommes += 1
                cmpt_block += 1
                cmpt_speed += 1

        while menu == 'perdu': #Boucle du menu de défaite
            efface_tout()
            MENU_perdu(mode, serpent, serpent_2)
            efface('refresh')
            clic = clique()
            if clic == 'play' or clic == 'quitte' or clic == 'Menu':
                menu = clic
            mise_a_jour()


    # fermeture et sortie
    ferme_fenetre()