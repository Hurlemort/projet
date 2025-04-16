import os
import sys
import pygame
import win32gui
from random import randint, choice, uniform
from math import cos, sin, pi

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
canal_rebond = pygame.mixer.Channel(1)
musique = pygame.mixer.Sound(os.path.join("assets", "sons", "musique.mp3"))
rebonds = [
    pygame.mixer.Sound(os.path.join("assets", "sons", "rebond1.mp3")),
    pygame.mixer.Sound(os.path.join("assets", "sons", "rebond2.mp3")),
    pygame.mixer.Sound(os.path.join("assets", "sons", "rebond3.mp3")),
    pygame.mixer.Sound(os.path.join("assets", "sons", "rebond4.mp3")),
]



def sonRebondAleatoire():
    canal_rebond.play(choice(rebonds))

def signe(n):
    return n / abs(n)

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


def jeu(scoreg, scored, largeur, hauteur):
    # Paramètres initiaux
    os.environ['SDL_VIDEO_WINDOW_POS'] = f"{(largeurEC - largeur) // 2},{(hauteurEC - hauteur) // 2}"
    monEcran = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption("Super Pong")
    

    pointeur = win32gui.FindWindow(None, "Super Pong")

    aReb = False
    jeu_en_cours = True
    vitesse = 0.1

    # Balle
    posx, posy = largeur // 2, hauteur // 2
    direction = choice([[cos(pi/4), sin(pi/4)],
                        [cos(-pi/4), sin(-pi/4)],
                        [cos(5*pi/4), sin(5*pi/4)],
                        [cos(-3*pi/4), sin(-3*pi/4)]])
    rayon = 15

    police = pygame.font.SysFont('arial', 30)

    # Raquettes
    raqgx, raqgy = 20, hauteur // 2
    raqdx, raqdy = largeur - 40, hauteur // 2
    wg = wd = 20
    hg = hd = 100
    mouvHautg = mouvBasg = mouvHautd = mouvBasd = False

    MAX_HAUTEUR = hauteurEC

    while jeu_en_cours:
        pygame.display.update()
        monEcran.fill((100, 40, 70))
        scores = f"{scoreg} - {scored}"
        score_texte = police.render(scores, True, (255, 255, 255))
        monEcran.blit(score_texte, score_texte.get_rect(center=(largeur // 2, 20)))

        # Collision haut/bas
        if posy <= 0 or posy >= hauteur:
            direction[1] *= -1
            sonRebondAleatoire()
            if hauteur + decalement <= MAX_HAUTEUR:
                hauteur += decalement
                monEcran= grandit_fenetre(pointeur, largeur, hauteur, decalage_haut=posy <= 0)

        # Mouvements des raquettes
        if mouvHautg and raqgy >= 10:
            raqgy -= 0.5
        if mouvBasg and raqgy <= hauteur - hg - 10:
            raqgy += 0.5
        if mouvHautd and raqdy >= 10:
            raqdy -= 0.5
        if mouvBasd and raqdy <= hauteur - hd:
            raqdy += 0.5

        # Rebond sur les raquettes
        rebond_gauche = rebond_droite = False
        if raqgx <= posx - rayon <= raqgx + wg and raqgy <= posy <= raqgy + hg:
            rebond_gauche = True
            direction_facteur = 1
        elif raqdx <= posx + rayon <= raqdx + wd and raqdy <= posy <= raqdy + hd:
            rebond_droite = True
            direction_facteur = -1

        if rebond_gauche or rebond_droite:
            if not aReb:
                angle = uniform(pi/6, pi/3)
                direction[0] = direction_facteur * abs(cos(angle))
                direction[1] = signe(direction[1]) * abs(sin(angle))
                vitesse += 0.025
                largeur += decalement
                raqdx += decalement
                monEcran = grandit_fenetre(pointeur, largeur, hauteur, decalage_gauche=rebond_gauche)
                aReb = True
                sonRebondAleatoire()

        # Reset rebond
        if not (raqgx - 2 * rayon <= posx <= raqgx + wg + 2 * rayon or
                raqdx - 2 * rayon <= posx <= raqdx + wd + 2 * rayon):
            aReb = False

        # Score
        if posx + rayon < 0:
            scoreg += 1
            return {"scoreg": scoreg, "scored": scored, "hauteur": hauteur, "largeur": largeur, "jeu": True}
        elif posx - rayon > largeur:
            scored += 1
            return {"scoreg": scoreg, "scored": scored, "hauteur": hauteur, "largeur": largeur, "jeu": True}

        # Dessins
        pygame.draw.rect(monEcran, (100, 100, 100), (raqgx, raqgy, wg, hg))
        pygame.draw.rect(monEcran, (100, 100, 100), (raqdx, raqdy, wd, hd))
        posx += vitesse * direction[0]
        posy += vitesse * direction[1]
        pygame.draw.circle(monEcran, (255, 255, 255), (posx, posy), rayon)

        # Reduit la fenêtre
        if pygame.time.get_ticks() % 200 == 0:  # le fais toute les 200ms
            largeur -= reduction
            hauteur -= reduction
            raqdx -= reduction
            monEcran = reduit_fenetre(pointeur, largeur, hauteur)

        # Evenements pygame
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                jeu_en_cours = False
            elif evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_a:
                    mouvHautg = True
                if evenement.key == pygame.K_q:
                    mouvBasg = True
                if evenement.key == pygame.K_p:
                    mouvHautd = True
                if evenement.key == pygame.K_m:
                    mouvBasd = True

            elif evenement.type == pygame.KEYUP:
                if evenement.key == pygame.K_a:
                    mouvHautg = False
                if evenement.key == pygame.K_q:
                    mouvBasg = False
                if evenement.key == pygame.K_p:
                    mouvHautd = False
                if evenement.key == pygame.K_m:
                    mouvBasd = False

    pygame.quit()
    return {"scoreg": 0, "scored": 0, "hauteur": hauteur, "largeur": largeur, "jeu": False}

# Boucle principale
while retour["jeu"]:
    if not joueMusique:
        musique.play()
        joueMusique=True
    retour = jeu(retour["scoreg"], retour["scored"], retour["largeur"], retour["hauteur"])
