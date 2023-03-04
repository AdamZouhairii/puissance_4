import numpy as np
import pygame
import random
import sys
import math 
from puissance_4 import *
from parametre import*


def check_board_full(board):
    """
    Vérifie si le tableau de jeu est plein.

    :param board: Le tableau de jeu.
    :return: True si le tableau est plein, False sinon.
    """
    for col in range(TAB_COLONNE):
        if board[TAB_LIGNE-1][col] == 0:
            return False
    return True



def find_blocking_column(board, player):
    # Vérification des rangées
    for row in range(TAB_LIGNE):
        for col in range(TAB_COLONNE - 2):
            if board[row][col] == player and board[row][col+1] == player and board[row][col+2] == player:
                if row > 0 and board[row-1][col+1] == 0 and board[row-1][col+2] == 0 and is_valid_location(board, col+1):
                    return col+1
                elif row > 0 and board[row-1][col] == 0 and board[row-1][col+2] == 0 and is_valid_location(board, col):
                    return col
                elif row > 0 and board[row-1][col] == 0 and board[row-1][col+1] == 0 and is_valid_location(board, col+2):
                    return col+2
                elif row == 0 and board[row+1][col+1] == 0 and board[row+1][col+2] == 0 and is_valid_location(board, col+1):
                    return col+1
                elif row == 0 and board[row+1][col] == 0 and board[row+1][col+2] == 0 and is_valid_location(board, col):
                    return col
                elif row == 0 and board[row+1][col] == 0 and board[row+1][col+1] == 0 and is_valid_location(board, col+2):
                    return col+2

    return None

def check_three_in_a_row(board, player):
    # Vérification des rangées
    for row in range(TAB_LIGNE):
        for col in range(TAB_COLONNE - 2):
            if board[row][col] == player and board[row][col+1] == player and board[row][col+2] == player:
                return True

    # Vérification des colonnes
    for row in range(TAB_LIGNE - 2):
        for col in range(TAB_COLONNE):
            if board[row][col] == player and board[row+1][col] == player and board[row+2][col] == player:
                return True

    # Vérification de la diagonale descendante (de gauche à droite)
    for row in range(TAB_LIGNE - 2):
        for col in range(TAB_COLONNE - 2):
            if board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player:
                return True

    # Vérification de la diagonale montante (de gauche à droite)
    for row in range(2, TAB_LIGNE):
        for col in range(TAB_COLONNE - 2):
            if board[row][col] == player and board[row-1][col+1] == player and board[row-2][col+2] == player:
                return True

    return False

def drop_piece(board, row, col, piece):
    """
    Place une pièce sur le tableau de jeu à la position spécifiée.

    :param board: Le tableau de jeu.
    :param row: La rangée où placer la pièce.
    :param col: La colonne où placer la pièce.
    :param piece: La pièce à placer (1 pour le joueur 1, 2 pour le joueur 2).
    """
    board[row][col] = piece

def get_next_open_row(board, col):
    """
    Retourne la prochaine rangée vide dans la colonne spécifiée.

    :param board: Le tableau de jeu.
    :param col: La colonne dans laquelle trouver la prochaine rangée vide.
    :return: L'index de la prochaine rangée vide ou None si la colonne est pleine.
    """
    for r in range(TAB_LIGNE):
        if board[r][col] == 0:
            return r
    return None

def is_valid_location(board, col):
    """
    Vérifie si la colonne spécifiée est valide pour jouer un coup.

    :param board: Le tableau de jeu.
    :param col: La colonne à vérifier.
    :return: True si la colonne est valide, False sinon.
    """
    return board[TAB_LIGNE-1][col] == 0

def draw_board(board):
    for row in range(TAB_LIGNE):
        for col in range(TAB_COLONNE):
            pygame.draw.rect(WINDOW, (0, 0, 255), (col*TAILLE_CARRE, row*TAILLE_CARRE+TAILLE_CARRE, TAILLE_CARRE, TAILLE_CARRE))
            pygame.draw.circle(WINDOW, (0, 0, 0), (int(col*TAILLE_CARRE+TAILLE_CARRE/2), int(row*TAILLE_CARRE+TAILLE_CARRE+TAILLE_CARRE/2)), RAYON)

    for row in range(TAB_LIGNE):
        for col in range(TAB_COLONNE):
            if board[row][col] == 1:
                pygame.draw.circle(WINDOW, PLAYER_1_COLOR, (int(col*TAILLE_CARRE+TAILLE_CARRE/2), HAUTEUR-int(row*TAILLE_CARRE+TAILLE_CARRE/2)), RAYON)
            elif board[row][col] == 2:
                pygame.draw.circle(WINDOW, BOT_COLOR, (int(col*TAILLE_CARRE+TAILLE_CARRE/2), HAUTEUR-int(row*TAILLE_CARRE+TAILLE_CARRE/2)), RAYON)
    pygame.display.update()
#Cette fonction prend en entrée le tableau de jeu "board" qui est une matrice numpy de dimensions TAB_LIGNE x TAB_COLONNE, et le joueur "player" dont on vérifie s'il a gagné.

#La fonction commence par vérifier s'il y a une victoire horizontale en parcourant chaque ligne du tableau et en vérifiant si les quatre éléments consécutifs appartiennent au joueur. Ensuite, elle vérifie les victoires verticales en parcourant chaque colonne du tableau et en vérifiant si les quatre éléments consécutifs appartiennent au joueur.

#La fonction vérifie ensuite les victoires diagonales en parcourant le tableau en diagonale. Elle vérifie les victoires diagonales en bas à droite en parcourant chaque élément du tableau dont la position correspond à l'élément en haut à gauche de la diagonale. Elle vérifie les victoires diagonales en bas à gauche en parcourant chaque élément du tableau dont la position correspond à l'élément en haut à droite de la diagonale.

#Si la fonction n'a pas trouvé de victoire, elle renvoie False.
 

def check_victory(board, player):
    # Vérifier les victoires horizontales
    for row in range(TAB_LIGNE):
        for col in range(TAB_COLONNE - 3):
            if board[row][col] == player and board[row][col+1] == player and board[row][col+2] == player and board[row][col+3] == player:
                return True

    # Vérifier les victoires verticales
    for row in range(TAB_LIGNE - 3):
        for col in range(TAB_COLONNE):
            if board[row][col] == player and board[row+1][col] == player and board[row+2][col] == player and board[row+3][col] == player:
                return True

    # Vérifier les victoires diagonales en bas à droite
    for row in range(TAB_LIGNE - 3):
        for col in range(TAB_COLONNE - 3):
            if board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player:
                return True

    # Vérifier les victoires diagonales en bas à gauche
    for row in range(TAB_LIGNE - 3):
        for col in range(3, TAB_COLONNE):
            if board[row][col] == player and board[row+1][col-1] == player and board[row+2][col-2] == player and board[row+3][col-3] == player:
                return True

    return False

def player_vs_bot():
    # Initialisation du tableau de jeu
    board = np.zeros((TAB_LIGNE, TAB_COLONNE))

    # Détermination du premier joueur
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
                    pygame.draw.circle(WINDOW, BOT_COLOR, (posx, int(TAILLE_CARRE/2)), RAYON)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(WINDOW, (0, 0, 0), (0, 0, LARGEUR, TAILLE_CARRE))
                # Tour du joueur humain
                if turn == 1:
                    posx = event.pos[0]
                    col = int(math.floor(posx/TAILLE_CARRE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if check_victory(board, 1):
                            draw_board(board)
                            pygame.display.update()
                            pygame.time.wait(3000)
                            print("Vous avez gagné !")
                            return

                        # Check if the player has three pieces in a row
                        if check_three_in_a_row(board, 1):
                            # Block the player's next move half the time
                            if random.randint(0, 1) == 0:
                                block_col = find_blocking_column(board, 1)
                                if block_col is not None:
                                    row = get_next_open_row(board, block_col)
                                    drop_piece(board, row, block_col, 2)
                                    turn = 2
                                    break

                        turn = 2

                # Tour du bot
                else:
                    col = random.randint(0, TAB_COLONNE-1)

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if check_victory(board, 2):
                            draw_board(board)
                            pygame.display.update()
                            pygame.time.wait(3000)
                            print("Le bot a gagné !")
                            return

                        turn = 1

                draw_board(board)

                if check_board_full(board):
                    pygame.time.wait(3000)
                    print("Match nul !")
                    return