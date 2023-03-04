import pygame
import sys

# Paramètres du jeu
LARGEUR = 580
HAUTEUR = 565
TAB_LIGNE = 6
TAB_COLONNE = 7
TAILLE_CARRE = 80
RAYON = int(TAILLE_CARRE/2 - 5)
PLAYER_1_COLOR = (255, 0, 0)
PLAYER_2_COLOR = (255, 255, 0)
BOT_COLOR = PLAYER_2_COLOR
FPS = 60

# Initialisation de la fenêtre de jeu
WINDOW = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame_icon = pygame.image.load('icon.png')
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption("Puissance 4")


def show_settings(LARGEUR, HAUTEUR, TAB_LIGNE, TAB_COLONNE, TAILLE_CARRE, RAYON, PLAYER_1_COLOR, PLAYER_2_COLOR, BOT_COLOR):
     
    while True:
        # Gestion des événements Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Affichage de l'écran des paramètres
        WINDOW.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        title_text = font.render("Paramètres", True, (255, 255, 255))
        WINDOW.blit(title_text, (LARGEUR/2 - title_text.get_width()/2, 100))

        width_text = font.render("Largeur : " + str(LARGEUR), True, (255, 255, 255))
        width_rect = width_text.get_rect(center=(LARGEUR/2, 200))
        WINDOW.blit(width_text, width_rect)

        height_text = font.render("Hauteur : " + str(HAUTEUR), True, (255, 255, 255))
        height_rect = height_text.get_rect(center=(LARGEUR/2, 250))
        WINDOW.blit(height_text, height_rect)

        rows_text = font.render("Lignes : " + str(TAB_LIGNE), True, (255, 255, 255))
        rows_rect = rows_text.get_rect(center=(LARGEUR/2, 300))
        WINDOW.blit(rows_text, rows_rect)

        cols_text = font.render("Colonnes : " + str(TAB_COLONNE), True, (255, 255, 255))
        cols_rect = cols_text.get_rect(center=(LARGEUR/2, 350))
        WINDOW.blit(cols_text, cols_rect)

        size_text = font.render("Taille des cases : " + str(TAILLE_CARRE), True, (255, 255, 255))
        size_rect = size_text.get_rect(center=(LARGEUR/2, 400))
        WINDOW.blit(size_text, size_rect)

        radius_text = font.render("Rayon des pièces : " + str(RAYON), True, (255, 255, 255))
        radius_rect = radius_text.get_rect(center=(LARGEUR/2, 450))
        WINDOW.blit(radius_text, radius_rect)

        p1_color_text = font.render("Couleur joueur 1 : " + str(PLAYER_1_COLOR), True, (255, 255, 255))
        p1_color_rect = p1_color_text.get_rect(center=(LARGEUR/2, 500))
        WINDOW.blit(p1_color_text, p1_color_rect)

        p2_color_text = font.render("Couleur joueur 2 : " + str(PLAYER_2_COLOR), True, (255, 255, 255))
        p2_color_rect = p2_color_text.get_rect(center=(LARGEUR/2, 550))
        WINDOW.blit(p2_color_text, p2_color_rect)

        quit_text = font.render("Retour", True, (255, 255, 0))
        quit_rect = quit_text.get_rect(center=(LARGEUR/5, 100))
        WINDOW.blit(quit_text, quit_rect)

        mx, my = pygame.mouse.get_pos()

        if quit_rect.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0] == 1:
                pygame.quit()
                sys.exit()

        pygame.display.update()