import pygame
from positions import positions, starting_positions
from Board_and_Pieces import *

# convert letter position to numbers for simplicity
letter_conversion = {'A':1
                    ,'B':2
                    ,'C':3
                    ,'D':4
                    ,'E':5
                    ,'F':6
                    ,'G':7
                    ,'H':8
                    }



def in_check(all_sprites,current_state, colour):

    all_moves = []
    for piece in all_sprites:
        if piece.colour != colour:
            if piece.name in current_state:
                possible_moves = piece.possible_moves(current_state)
                all_moves += possible_moves

    for piece in all_sprites:
        if piece.piece == 'king' and piece.colour == colour:
            if current_state[piece.name] in all_moves:
                return True
            return False

def checkmate(all_sprites,current_state, colour):
    '''checks if colour is in checkmate'''
    checkmate = True
    for piece in all_sprites:
        if piece.colour == colour:
            possible_moves = piece.possible_moves(current_state)
            for move in possible_moves:
                new_state = {key:val for key, val in current_state.items() if val != move}
                new_state[piece.name] = move
                check = in_check(all_sprites,new_state, colour)
                if not check:
                    return False
    return True

def stalemate_or_checkmate(all_sprites,current_state, colour):
    if checkmate(all_sprites,current_state, colour):
        if in_check(all_sprites,current_state, colour):
            return 'checkmate'
        else:
            return 'stalemate'
    return False
