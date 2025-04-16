import os
import pygame
from random import choice, uniform
from math import cos, sin, pi

pygame.init()

# Résolution écran
largeurEC, hauteurEC = pygame.display.Info().current_w, pygame.display.Info().current_h
largeur, hauteur = 800, 600

retour = {"scoreg": 0, "scored": 0, "hauteur": hauteur, "largeur": largeur, "jeu": True}

def signe(n):
    return n/abs(n)

def centrer_fenetre(largeur, hauteur, decalage_haut=False,):
    x = (largeurEC - largeur) // 2
    y = (hauteurEC - hauteur) // 2
    os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"

def jeu(scoreg, scored, largeur, hauteur):
    centrer_fenetre(largeur, hauteur)
    monEcran = pygame.display.set_mode((largeur, hauteur))

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

    font = pygame.font.SysFont('arial', 30)

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
        score_text = font.render(scores, True, (255, 255, 255))
        monEcran.blit(score_text, score_text.get_rect(center=(largeur // 2, 20)))

        # Collision haut
        if posy <= 0:
            direction[1] *= -1
            if hauteur + 20 <= MAX_HAUTEUR:
                hauteur += 20
                centrer_fenetre(largeur, hauteur, decalage_haut=True)
                monEcran = pygame.display.set_mode((largeur, hauteur))

        # Collision bas
        elif posy >= hauteur:
            direction[1] *= -1
            if hauteur + 20 <= MAX_HAUTEUR:
                hauteur += 20
                centrer_fenetre(largeur, hauteur)
                monEcran = pygame.display.set_mode((largeur, hauteur))

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
        if raqgx <= posx - rayon <= raqgx + wg and raqgy <= posy <= raqgy + hg:
            if not aReb:
                angle = uniform(pi/6, pi/3)
                direction[0] = abs(cos(angle))
                direction[1] = signe(direction[1]) * abs(sin(angle))
                vitesse += 0.05
                aReb = True

        elif raqdx <= posx + rayon <= raqdx + wd and raqdy <= posy <= raqdy + hd:
            if not aReb:
                angle = uniform(pi/6, pi/3)
                direction[0] = -abs(cos(angle))
                direction[1] = signe(direction[1]) * abs(sin(angle))
                vitesse += 0.05
                aReb = True

        # Reset rebond si hors raquettes
        if not (raqgx - 2 * rayon <= posx <= raqgx + wg + 2 * rayon or
                raqdx - 2 * rayon <= posx <= raqdx + wd + 2 * rayon):
            aReb = False

        # Gestion des points (hauteur non transmise augmentée)
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

        # Événements clavier
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

while retour["jeu"]:
    retour = jeu(retour["scoreg"], retour["scored"], retour["largeur"], retour["hauteur"])
