import numpy as np
import pygame
import random
import sys
import math 
from puissance_4 import *
from parametre import*
from keras.models import Sequential
from keras.layers import Dense
from bot import*


def create_model():
    '''La première ligne de la fonction crée un objet Sequential, 
    qui est utilisé pour empiler les couches du réseau de neurones les unes sur les autres.
La ligne suivante ajoute une couche Dense au réseau de neurones avec 128 neurones, 
une dimension d'entrée de 42 et une fonction d'activation "relu". 
La fonction relu (rectified linear unit) est utilisée pour introduire de la non-linéarité dans les sorties de chaque neurone.
La ligne suivante ajoute une autre couche Dense avec 256 neurones et une fonction d'activation "relu".
La ligne suivante ajoute une autre couche Dense avec 128 neurones et une fonction d'activation "relu".
La dernière ligne ajoute une couche Dense finale avec 7 neurones (correspondant aux 7 classes possibles de classification) et 
une fonction d'activation "softmax". La fonction softmax est utilisée pour normaliser les sorties des neurones 
afin qu'elles puissent être interprétées comme des probabilités.
Enfin, le modèle est compilé avec une fonction de perte categorical_crossentropy,
 un optimiseur adam et une métrique d'évaluation accuracy.
La fonction create_model() renvoie ensuite le modèle créé'''
    model = Sequential()
    model.add(Dense(128, input_dim=42, activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(7, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


'''Si le nombre aléatoire est supérieur à la valeur d'exploration epsilon, la fonction utilise le modèle de réseau de neurones pour choisir la meilleure colonne. 
         Tout d'abord, la fonction "np.reshape" est utilisée pour transformer le plateau de jeu en un tableau 1D de longueur 128, 
         ce qui correspond à la taille d'entrée attendue par le modèle de réseau de neurones.
           Les sorties du modèle sont calculées en appelant la méthode "predict" du modèle. 
           Les sorties sont ensuite filtrées en utilisant les positions valides renvoyées par la fonction "get_valid_locations".
        '''
''' Une variable "mask" est créée en initialisant tous les éléments à 1.
          Puis la valeur "0" est assignée aux positions invalides de la variable "mask".
          Finalement, les sorties sont multipliées par la variable "mask" pour annuler les sorties invalides. 
         La colonne avec la plus grande sortie est choisie en utilisant la fonction "np.argmax".
         '''
def get_model_move(board, model, epsilon):
             
    if np.random.rand() < epsilon:
        # exploration : choisit une colonne au hasard
        col = np.random.randint(0, 7)
        while not is_valid_location(board, col):
            col = np.random.randint(0, 7)
    else:
 
        inputs = np.reshape(board, (1, 42))   # np.reshape permet de transformer le plateau de jeu en un tableau 1D de longueur 42, 
    # correspondant à la taille d'entrée attendue par le modèle de réseau de neurones
        outputs = model.predict(inputs)
        valid_moves = get_valid_locations(board)
        mask = np.ones(outputs.shape) # On crée une matrice de la même taille que les sorties du modèle, remplie de 1
        mask[0][np.logical_not(valid_moves)] = 0
        outputs *= mask
        col = np.argmax(outputs)
    return col


def get_best_move(board, nn, turn):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, turn)
        score = nn.predict(temp_board.reshape(1, -1))[0]
        if max(score) > best_score:
            best_score = max(score)
            best_col = col
    return best_col



def get_valid_locations(board):
    valid_locations = []
    for col in range(TAB_COLONNE):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations
def train_model(model, X_train, y_train):
    """
    Entraîne le modèle de réseau de neurones en utilisant les données d'entraînement.

    :param model: le modèle de réseau de neurones à entraîner
    :param X_train: les données d'entraînement
    :param y_train: les étiquettes associées aux données d'entraînement
    """
    y_train = y_train.reshape(-1, 1)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=2)



def save_data(model, etat):
    # Enregistrement du modèle dans un fichier HDF5
    model.save("model.h5")

    # Enregistrement des états et des coups joués dans des fichiers Numpy
    np.save("states.npy", np.array(etat))



def player_vs_IA():
    # Initialisation du tableau de jeu
    board = np.zeros((TAB_LIGNE, TAB_COLONNE))

    # Détermination du premier joueur
    turn = random.randint(1, 2)

    # Chargement du réseau de neurones
    model = create_model()

    # Liste pour stocker les états de jeu
    game_states = []

    # Boucle principale du jeu
    while True:
        # Gestion des événements Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_data(model, game_states)
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
                            game_states.append(board)
                            train_model(model, np.array([state.flatten() for state in game_states]), np.array([state.flatten() for state in game_states]))
                            return

                        # Vérifiez si le joueur a trois pièces d'affilée
                        if check_three_in_a_row(board, 1):
                            # Bloquer le prochain coup du joueur
                             
                            block_col = find_blocking_column(board, 1)
                            if block_col is not None:
                                row = get_next_open_row(board, block_col)
                                drop_piece(board, row, block_col, 2)
                                turn = 2
                                break

                        turn = 2

                # Tour du bot
                else:
                    col = get_best_move(board, model, 2)

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if check_victory(board, 2):
                            draw_board(board)
                            pygame.display.update()
                            pygame.time.wait(3000)
                            print("L'IA a gagné !")
                            game_states.append(board)
                            train_model(model,np.array([state.flatten() for state in game_states]),np.array([state.flatten() for state in game_states]))
                            return

                        turn = 1

                draw_board(board)

                if check_board_full(board):
                    pygame.time.wait(3000)
                    print("Match nul , Attention l'IA vous ratrape !")
                    game_states.append(board)
                    train_model(model,np.array([state.flatten() for state in game_states]),np.array([state.flatten() for state in game_states]))
                    return 

 