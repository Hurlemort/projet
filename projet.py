from random import randint,choice
import pygame
scoreg, scored = 0,0


def jeu(scoreg, scored):
    pygame.init()
    largeur ,hauteur=800,600
    monEcran=pygame.display.set_mode((largeur ,hauteur ))

    jeu_en_cours=True
    vitesse=0.1

    #balle
    posx=largeur//2
    posy=hauteur//2
    direction=choice([[1,1],[-1,1],[1,-1],[-1,-1]])
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
            raqgy-=0.5
        if mouvBasg==True:
            raqgy+=0.5
            
        if mouvHautd==True:
            raqdy-=0.5
        if mouvBasd==True:
            raqdy+=0.5
        # rebond raquettes    
        if (raqgx<posx-rayon<raqgx+wg and raqgy<posy+rayon<raqgy+hg) ^ (raqdx<posx+rayon<raqdx+wd and raqdy<posy+rayon<raqdy+hd): #collision balle-raquettes
            direction[0]*=-1
            vitesse+=0.05
        
        if posx+rayon<0:
            scoreg+=1
            jeu(scoreg, scored)
            
        elif posx-rayon>largeur:
            scored+=1
            jeu(scoreg, scored)

            
        
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
                mouvHautg, mouvBasg, mouvHautd, mouvBasd=False, False, False, False
                    
    pygame.quit()
    
jeu(scoreg,scored)

