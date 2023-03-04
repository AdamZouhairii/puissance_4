import numpy as np
import pygame
import random
import sys
import math
from IA import*
from parametre import *
from bot import*
# Initialisation de Pygame
pygame.init()


#humain vs humain
def player_vs_player():
    # Initialisation du tableau de jeu
    board = np.zeros((TAB_LIGNE, TAB_COLONNE))

    # TAILLE_CARRE du premier joueur
    turn = random.randint(1, 2)

    # Boucle principale du jeu
    while True:
        # Gestion des événements Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(WINDOW, (0, 0, 0), (0, 0, LARGEUR, TAILLE_CARRE))
                posx = event.pos[0]
                if turn == 1:
                    pygame.draw.circle(WINDOW, PLAYER_1_COLOR, (posx, int(TAILLE_CARRE/2)), RAYON)
                else:
                    pygame.draw.circle(WINDOW, PLAYER_2_COLOR, (posx, int(TAILLE_CARRE/2)), RAYON)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(WINDOW, (0, 0, 0), (0, 0, LARGEUR, TAILLE_CARRE))
                posx = event.pos[0]
                col = int(math.floor(posx/TAILLE_CARRE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)

                    if turn == 1:
                        drop_piece(board, row, col, 1)

                        if check_victory(board, 1):
                            draw_board(board)
                            pygame.display.update()
                            pygame.time.wait(3000)
                            print("Joueur 1 a gagné !")
                            return

                        turn = 2

                    else:
                        drop_piece(board, row, col, 2)

                        if check_victory(board, 2):
                            draw_board(board)
                            pygame.display.update()
                            pygame.time.wait(3000)
                            print("Joueur 2 a gagné !")
                            return

                        turn = 1

                draw_board(board)

                if check_board_full(board):
                    pygame.time.wait(3000)
                    print("Match nul !")
                    return


 
 

            
 




def show_menu():
    while True:
        # Gestion des événements Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Affichage du menu
        WINDOW.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        title_text = font.render("Puissance 4", True, (255, 0, 255))
        WINDOW.blit(title_text, (LARGEUR/2 - title_text.get_width()/2, 50))

        new_game_text = font.render("player vs bot", True, (255, 255, 255))
        new_game_rect = new_game_text.get_rect(center=(LARGEUR/2, 150))
        WINDOW.blit(new_game_text, new_game_rect)

        newgame= font.render("combatre l'ia", True, (255, 255, 255))
        new_ = newgame.get_rect(center=(LARGEUR/2, 200))
        WINDOW.blit(new_game_text, new_)

        game = font.render("player vs player", True, (255, 255, 255))
        game_ = game.get_rect(center=(LARGEUR/2, 250))
        WINDOW.blit(game,game_ )

        settings_text = font.render("Paramètres", True, (255, 255, 255))
        settings_rect = settings_text.get_rect(center=(LARGEUR/2, 300))
        WINDOW.blit(settings_text, settings_rect)

        quit_text = font.render("Quitter", True, (255, 0, 0))
        quit_rect = quit_text.get_rect(center=(LARGEUR/2, 350))
        WINDOW.blit(quit_text, quit_rect)

        # Vérification des clics de souris
        mx, my = pygame.mouse.get_pos()

        if new_game_rect.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0] == 1:
                player_vs_bot()

        if new_.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0] == 1:
                player_vs_IA()

        if game_.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0] == 1:
                player_vs_player()

        if settings_rect.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0] == 1:
                show_settings(LARGEUR, HAUTEUR, TAB_LIGNE, TAB_COLONNE, TAILLE_CARRE, RAYON, PLAYER_1_COLOR, PLAYER_2_COLOR, BOT_COLOR)

        if quit_rect.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0] == 1:
                pygame.quit()
                sys.exit()

        pygame.display.update()

 
 
