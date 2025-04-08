from random import randint,choice, uniform
from math import cos, sin, pi
import pygame
scoreg, scored = 0,0

def signe(n):
    return n/abs(n)

def jeu(scoreg, scored):
    pygame.init()
    largeur ,hauteur=800,600
    monEcran=pygame.display.set_mode((largeur ,hauteur ))
    aAug=True
    jeu_en_cours=True
    vitesse=0.1

    #balle
    posx=largeur//2
    posy=hauteur//2
    direction=choice([[cos(pi/4),sin(pi/4)],
                      [cos(-1*pi/4),sin(-1*pi/4)],
                      [cos(5*pi/4),sin(5*pi/4)],
                      [cos(-3*pi/4),sin(-3*pi/4)]
                      ])
    rayon=15

    # scores
    font = pygame.font.SysFont('arial', 30)
    scores=f"{scoreg} - {scored}"

    #raquette gauche
    raqgx=20
    raqgy=hauteur//2
    wg =20
    hg=100
    mouvHautg=False
    mouvBasg=False

    #raquette droite
    raqdx=largeur-40
    raqdy=hauteur//2
    wd=20
    hd=100
    mouvHautd=False
    mouvBasd=False
    while jeu_en_cours==True:
        pygame.display.update()
        monEcran.fill((100,40,70))
        scores=f"{scoreg} - {scored}"
        trucmuche=font.render(scores, True, (255,255,255))
        monEcran.blit(trucmuche, trucmuche.get_rect(center=(largeur//2, 20)))
        #changement de direction quand la balle touche un mur
        if posy<=0 or posy>=hauteur:
            direction[1]*=-1
        
        #mouvement des raquettes
        if mouvHautg==True:
            if raqgy>=10:
                raqgy-=0.5
        if mouvBasg==True:
            if raqgy<=hauteur-hg-10:
                raqgy+=0.5
            
        if mouvHautd==True:
            if raqdy>=10:
                raqdy-=0.5
        if mouvBasd==True:
            if raqdy<=hauteur-hd:
                raqdy+=0.5
        # rebond raquettes
        b=signe(direction[1])
        a=round(uniform(0,pi/2),2)
        if (raqgx<=posx-rayon<=raqgx+wg and raqgy<=posy<=raqgy+hg) ^ (raqdx<=posx+rayon<=raqdx+wd and raqdy<=posy<=raqdy+hd): #collision balle-raquettes
            direction[0]=-b*sin(a)
            if aAug==False:
                vitesse+=0.05
            aAug=True
        
        if posx+rayon<0:
            scoreg+=1
            
        elif posx-rayon>largeur:
            scored+=1

            
        
        #dessin des raquettes
        pygame.draw.rect(monEcran,(100, 100, 100),(raqgx,raqgy,wg,hg))
        pygame.draw.rect(monEcran,(100, 100, 100),(raqdx,raqdy,wd,hd))

        ##Déplacement de La balle
        posx=posx+vitesse*direction[0]#Variation des abscisses
        posy=posy+vitesse*direction[1]#Variation des ordonnées
        
        #Création de la balle
        pygame.draw.circle(monEcran,(255, 255, 255),(posx,posy),rayon)

        #PARTIE GESTION DES EVENEMENTS
        for evenement in pygame.event.get():# Boucle sur les evenements
            if evenement.type==pygame.QUIT: #Si l'evenement est quitter            
                jeu_en_cours=False #arret de la boucle
            if evenement.type==pygame.KEYDOWN:
                if evenement.key==pygame.K_a:
                    mouvHautg=True
                
                if evenement.key==pygame.K_q:
                    mouvBasg=True
                    
                if evenement.key==pygame.K_p:
                    mouvHautd=True
                
                if evenement.key==pygame.K_m:
                    mouvBasd=True
                    
            elif evenement.type==pygame.KEYUP:
                if evenement.key==pygame.K_a:
                    mouvHautg=False
                    
                if evenement.key==pygame.K_q:
                    mouvBasg=False
                    
                if evenement.key==pygame.K_p:
                    mouvHautd=False
                    
                if evenement.key==pygame.K_m:
                    mouvBasd=False

                    
    pygame.quit()
    
jeu(scoreg,scored)

