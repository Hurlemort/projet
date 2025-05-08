import os
import sys
import pygame
import win32gui
from random import randint, choice, uniform
from math import cos, sin, sqrt, pi

from param import *

# Fixe le répertoire de travail à celui du script
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(script_dir)

pygame.mixer.pre_init(44100, -16, 2, 256)

pygame.init()

# Résolution écran
largeurEC, hauteurEC = pygame.display.Info().current_w, pygame.display.Info().current_h
largeur, hauteur = 800, 600

retour = {"scoreg": 0, "scored": 0, "hauteur": hauteur, "largeur": largeur, "jeu": True}

decalement = 20
reduction = 2

joueMusique=False
canal_rebond_raq = pygame.mixer.Channel(1)
canal_rebond_bord = pygame.mixer.Channel(2)
musique = pygame.mixer.Sound(os.path.join("assets", "sons", "musique.mp3"))
rebonds = [
    pygame.mixer.Sound(os.path.join("assets", "sons", "rebond1.mp3")),
    pygame.mixer.Sound(os.path.join("assets", "sons", "rebond2.mp3")),
    pygame.mixer.Sound(os.path.join("assets", "sons", "rebond3.mp3")),
    pygame.mixer.Sound(os.path.join("assets", "sons", "rebond4.mp3")),
]


def signe(n):
    return n/abs(n)

def grandit_fenetre(pointeur, largeur, hauteur, decalage_haut=False, decalage_gauche=False):
    monEcran = pygame.display.set_mode((largeur, hauteur))
    dimensions = win32gui.GetWindowRect(pointeur)

    if (decalage_haut):
        win32gui.MoveWindow(pointeur, dimensions[0], dimensions[1]-decalement, dimensions[2]-dimensions[0], dimensions[3]-dimensions[1], True)
    elif (decalage_gauche):
        win32gui.MoveWindow(pointeur, dimensions[0]-decalement, dimensions[1], dimensions[2]-dimensions[0], dimensions[3]-dimensions[1], True)

    return monEcran

def reduit_fenetre(pointeur, largeur, hauteur):
    monEcran = pygame.display.set_mode((largeur, hauteur))
    dimensions = win32gui.GetWindowRect(pointeur)

    x = dimensions[0]+reduction//2
    y = dimensions[1]+reduction//2
    win32gui.MoveWindow(pointeur, x, y, dimensions[2]-dimensions[0], dimensions[3]-dimensions[1], True)

    return monEcran

def menu():
    pygame.init()
    largeur, hauteur = 800, 600
    fenetre = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption("Entree des noms")

    police = pygame.font.Font(None, 60)
    petite_police = pygame.font.Font(None, 40)
    couleur_fond = GRIS_FONCE
    couleur_texte = BLANC

    joueurg = ""
    joueurd = ""
    entrer_compteur = 0
    texte_actif = "gauche"

    bouton_start_visible = False
    bouton_rect = pygame.Rect(largeur // 2 - 100, hauteur // 2 + 100, 200, 60)

    while True:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_RETURN:
                    entrer_compteur += 1
                    if entrer_compteur == 1:
                        texte_actif = "droite"
                    elif entrer_compteur == 2:
                        if joueurg.strip() == "":
                            joueurg = "flibidi"
                        if joueurd.strip() == "":
                            joueurd = "zagrub"
                        bouton_start_visible = True

                elif evenement.key == pygame.K_BACKSPACE:
                    if texte_actif == "gauche":
                        joueurg = joueurg[:-1]
                    else:
                        joueurd = joueurd[:-1]
                else:
                    caractere = evenement.unicode
                    if caractere.isprintable():
                        if texte_actif == "gauche":
                            joueurg += caractere
                        else:
                            joueurd += caractere

            if evenement.type == pygame.MOUSEBUTTONDOWN and bouton_start_visible:
                if bouton_rect.collidepoint(evenement.pos):
                    return joueurg, joueurd

        fenetre.fill(couleur_fond)

        if texte_actif == "gauche":
            texte_affiche = "Nom du joueur de gauche: " + joueurg
        elif texte_actif == "droite" and not bouton_start_visible:
            texte_affiche = "Nom du joueur de droit: " + joueurd
        else:
            texte_affiche = "Cliquez sur START pour commencer"

        rendu_texte = police.render(texte_affiche, True, couleur_texte)
        rect_texte = rendu_texte.get_rect(center=(largeur // 2, hauteur // 2 - 100))
        fenetre.blit(rendu_texte, rect_texte)

        if bouton_start_visible:
            souris_pos = pygame.mouse.get_pos()
            x, y = souris_pos
            x1 = largeur // 2 - 100
            x2 = largeur // 2 + 100
            y1 = hauteur // 2 + 100
            y2 = hauteur // 2 + 160

            if x1 <= x <= x2 and y1 <= y <= y2:
                couleur_bouton = GRIS_CLAIR
                couleur_texte_bouton = BLANC
            else:
                couleur_bouton = BLANC
                couleur_texte_bouton = GRIS_FONCE

            pygame.draw.rect(fenetre, couleur_bouton, bouton_rect)
            texte_bouton = petite_police.render("START", True, couleur_texte_bouton)
            fenetre.blit(texte_bouton, texte_bouton.get_rect(center=bouton_rect.center))

        pygame.display.flip()


    
def powerup(hauteur, largeur):
    ecart=60
    powx=randint(ecart, largeur-ecart)
    powy=randint(ecart, hauteur-ecart)
    diff_powerup=[ROUGE,VERT,BLEU,JAUNE]
    rep=[(powx, powy), RAYON_POWERUP]
    rep.append(choice(diff_powerup))
    return rep

def num_powerup(dico) :
    n = 0
    for element in dico["cercle"].keys() :
        if "powerup" in element :
            n += 1
    return n

def collision_powerup(dico_dessin,posx,posy):
    distance_min = RAYON_BALLE+RAYON_POWERUP
    for element in dico_dessin["cercle"].items():
        if "powerup" in element[0] and sqrt((posx-element[1][0][0])**2 + (posy-element[1][0][1])**2) <= distance_min:
            return element


def afficher(dico_dessin, monEcran) :
    for element in dico_dessin["rectangle"].values() :
        pygame.draw.rect(monEcran,element[1],element[0])
    for element in dico_dessin["cercle"].values() :
        pygame.draw.circle(monEcran,element[2],element[0],element[1])

def jeu(scoreg, scored, largeur, hauteur):
    # Paramètres initiaux
    os.environ['SDL_VIDEO_WINDOW_POS'] = f"{(largeurEC - largeur) // 2},{(hauteurEC - hauteur) // 2}"
    monEcran = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption("Super Pong")

    pointeur = win32gui.FindWindow(None, "Super Pong")

    jeu_en_cours = True
    vitesse = 0.1

    # Balle
    posx, posy = largeur // 2, hauteur // 2
    direction = choice([[cos(pi/4), sin(pi/4)],
                        [cos(-pi/4), sin(-pi/4)],
                        [cos(5*pi/4), sin(5*pi/4)],
                        [cos(-3*pi/4), sin(-3*pi/4)]])

    police = pygame.font.Font(None, 60)

    # Raquettes
    raqgx, raqgy = 20, hauteur // 2
    raqdx, raqdy = largeur - 40, hauteur // 2
    wg = wd = 20
    hg = hd = 100
    mouvHautg = mouvBasg = mouvHautd = mouvBasd = False

    MAX_HAUTEUR = hauteurEC

    dico_dessin={
            "rectangle" : {
                "raquette gauche" : [(raqgx, raqgy, wg, hg), BLANC],
                "raquette droite" : [(raqdx, raqdy, wd, hd),BLANC]
            },
            "cercle": {
                "balle" : [(posx, posy), RAYON_BALLE, BLANC]
            }
    }

    id_powerup=0
    inverse_controle=False
    joueur_inverse = None
    double_raquette_gauche = False
    double_raquette_droite = False
    super_vitesse=False

    while jeu_en_cours:
        pygame.display.update()
        monEcran.fill(GRIS_FONCE)

        scores = f"{scoreg} - {scored}"
        score_texte = police.render(scores, True, BLANC)
        monEcran.blit(score_texte, score_texte.get_rect(center=(largeur // 2, 40)))

        affiche_joueurg = police.render(joueurg, True, BLANC)
        affiche_joueurd = police.render(joueurd, True, BLANC)

        monEcran.blit(affiche_joueurg, (20, 20))
        monEcran.blit(affiche_joueurd, affiche_joueurd.get_rect(topright=(largeur - 20, 20)))

        # Collision haut/bas
        if posy <= 0 or posy >= hauteur:
            canal_rebond_bord.play(choice(rebonds))
            direction[1] *= -1
            if hauteur + decalement <= MAX_HAUTEUR:
                hauteur += decalement
                monEcran= grandit_fenetre(pointeur, largeur, hauteur, decalage_haut=posy <= 0)

        # Mouvements des raquettes
        avancement = 0.4
        # Gauche
        if double_raquette_gauche:
            if mouvHautg and raqgy <= hauteur - hg - 10:
                raqgy += avancement  # inversé
            if mouvBasg and raqgy >= 10:
                raqgy -= avancement
        else:
            if mouvHautg and raqgy >= 10:
                raqgy -= avancement
            if mouvBasg and raqgy <= hauteur - hg - 10:
                raqgy += avancement

        # Droite
        if double_raquette_droite:
            if mouvHautd and raqdy <= hauteur - hd - 10:
                raqdy += avancement
            if mouvBasd and raqdy >= 10:
                raqdy -= avancement
        else:
            if mouvHautd and raqdy >= 10:
                raqdy -= avancement
            if mouvBasd and raqdy <= hauteur - hd:
                raqdy += avancement

        # Collision raquettes (y compris doubles)
        collision = False
        collision_raq_active = False
        if not collision_raq_active:
            if raqgx <= posx - RAYON_BALLE <= raqgx + wg and raqgy <= posy <= raqgy + hg and direction[0] < 0:
                collision = True
                balle_au_gauche = True
            elif double_raquette_gauche and raqgx <= posx - RAYON_BALLE <= raqgx + wg and raqgy2 <= posy <= raqgy2 + hg and direction[0] < 0:
                collision = True
                balle_au_gauche = True
            elif raqdx <= posx + RAYON_BALLE <= raqdx + wd and raqdy <= posy <= raqdy + hd and direction[0] > 0:
                collision = True
                balle_au_gauche = False
            elif double_raquette_droite and raqdx <= posx + RAYON_BALLE <= raqdx + wd and raqdy2 <= posy <= raqdy2 + hd and direction[0] > 0:
                collision = True
                balle_au_gauche = False

            if collision:
                canal_rebond_raq.play(choice(rebonds))
                sens = -signe(direction[0])
                if sens == 1:
                    angle = -(raqgy + hg/2 - posy) * (pi/3) / hg
                else:
                    angle = -(raqdy + hd/2 - posy) * (pi/3) / hd
                direction[0] = sens * cos(angle)
                direction[1] = sin(angle)
                largeur += decalement
                raqdx += decalement
                monEcran = grandit_fenetre(pointeur, largeur, hauteur, decalage_gauche=sens == 1)
                if randint(1, 5) == 1:
                    dico_dessin["cercle"][f"powerup{id_powerup}"] = powerup(hauteur, largeur)
                    id_powerup += 1
                if super_vitesse:
                    vitesse=old_vitesse
                    super_vitesse=False
                vitesse += 0.025
                collision_raq_active = True


        # Collision powerup
        collision = collision_powerup(dico_dessin,posx,posy)
        if collision :
            if dico_dessin["cercle"][collision[0]][2] == ROUGE:
                vitesse*=1.3
                if super_vitesse:
                    old_vitesse*=1.3
            elif dico_dessin["cercle"][collision[0]][2] == VERT:
                inverse_controle=True
                joueur_inverse = "droite" if balle_au_gauche else "gauche"
            elif dico_dessin["cercle"][collision[0]][2] == BLEU:
                    if balle_au_gauche:
                        double_raquette_gauche = True
                    else:
                        double_raquette_droite = True
            elif dico_dessin["cercle"][collision[0]][2] == JAUNE:
                old_vitesse=vitesse
                vitesse*=2
                super_vitesse=True
            del dico_dessin["cercle"][collision[0]]

        # Score
        if posx + RAYON_BALLE < 0:
            scored += 1
            return {"scoreg": scoreg, "scored": scored, "hauteur": hauteur, "largeur": largeur, "jeu": True}
        elif posx - RAYON_BALLE > largeur:
            scoreg += 1
            return {"scoreg": scoreg, "scored": scored, "hauteur": hauteur, "largeur": largeur, "jeu": True}

    
        posx += vitesse * direction[0]
        posy += vitesse * direction[1]

        if not (raqgx <= posx - RAYON_BALLE <= raqgx + wg) and not (raqdx <= posx + RAYON_BALLE <= raqdx + wd):
            collision_raq_active = False

        if double_raquette_gauche:
            raqgy2 = hauteur - raqgy - hg  # miroir vertical
            dico_dessin["rectangle"]["raquette gauche 2"] = [(raqgx, raqgy2, wg, hg), BLANC]
        if double_raquette_droite:
            raqdy2 = hauteur - raqdy - hd
            dico_dessin["rectangle"]["raquette droite 2"] = [(raqdx, raqdy2, wd, hd), BLANC]
        
        dico_dessin["rectangle"]["raquette gauche"] = [(raqgx, raqgy, wg, hg), BLANC]
        dico_dessin["rectangle"]["raquette droite"] = [(raqdx, raqdy, wd, hd), BLANC]
        dico_dessin["cercle"]["balle"] = [(posx, posy), RAYON_BALLE, BLANC]

 

        # Reduit la fenêtre
        if pygame.time.get_ticks() % 200 == 0:  # le fais toute les 200ms
            largeur -= reduction
            hauteur -= reduction
            raqdx -= reduction
            monEcran = reduit_fenetre(pointeur, largeur, hauteur)
        if pygame.time.get_ticks() % 5000 == 0:
            inverse_controle = False
            joueur_inverse = None

        # Evenements pygame
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                jeu_en_cours = False

            elif evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_a:
                    if inverse_controle and joueur_inverse == "gauche":
                        mouvBasg = True
                    else:
                        mouvHautg = True
                if evenement.key == pygame.K_q:
                    if inverse_controle and joueur_inverse == "gauche":
                        mouvHautg = True
                    else:
                        mouvBasg = True
                if evenement.key == pygame.K_p:
                    if inverse_controle and joueur_inverse == "droite":
                        mouvBasd = True
                    else:
                        mouvHautd = True
                if evenement.key == pygame.K_m:
                    if inverse_controle and joueur_inverse == "droite":
                        mouvHautd = True
                    else:
                        mouvBasd = True

            elif evenement.type == pygame.KEYUP:
                if evenement.key == pygame.K_a or evenement.key == pygame.K_q:
                    mouvHautg = False
                    mouvBasg = False
                if evenement.key == pygame.K_p or evenement.key == pygame.K_m:
                    mouvHautd = False
                    mouvBasd = False


        afficher(dico_dessin,monEcran)

    pygame.quit()
    return {"scoreg": 0, "scored": 0, "hauteur": hauteur, "largeur": largeur, "jeu": False}

# Boucle principale
joueurs=menu()
joueurg=joueurs[0]
joueurd=joueurs[1]
while retour["jeu"]:
    if not joueMusique:
        musique.play(loops=-1)
        musique.set_volume(0.3)
        joueMusique=True
    retour = jeu(retour["scoreg"], retour["scored"], retour["largeur"], retour["hauteur"])
