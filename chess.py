# each square: w=57 h = 57

# left bottom w=21 h=21


# right top w=25 h=25

from positions import positions, starting_positions
from Pieces import *
from Board import Background, Board

import pygame


# --- constants --- (UPPER_CASE names)

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 498

#BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
# RED   = (255,   0,   0)

FPS = 30



# --- functions --- (lower_case names)

def current_state(all_sprites):
    state = {}
    for piece in all_sprites:
        state[piece.name] = piece.current_position
    return state

def promote_pawn(piece,all_sprites):
    
    if piece.colour == 'white':
        promotion_number = 8
    else:
        promotion_number = 1

    name, colour, starting_location, starting_position = [piece.name, piece.colour, piece.rect.center, piece.current_position]
    if int(piece.current_position[1]) == promotion_number:
        piece.kill()
        vars()[piece.name] = Queen(piece.name, piece.colour, piece.rect.center, piece.current_position)
        all_sprites.add(vars()[piece.name])

# --- main ---

# - init -

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Chess")

# - objects -

BackGround = Background('images/board.png', [0,0])



# initialize board

Board = Board(starting_positions)

# player_1 = pygame.sprite.Group()
# player_2 = pygame.sprite.Group()
# all_sprites = pygame.sprite.Group()

# starting_colour = 'white'
# current_turn = starting_colour


# for starting_piece in starting_positions.keys():
#     piece,colour = starting_piece.split('_')[:2]
#     starting_location = positions[starting_positions[starting_piece]][2]
#     starting_position = starting_positions[starting_piece]
#     vars()[starting_piece] = vars()[piece.capitalize()](starting_piece,colour,starting_location,starting_position)

#     if starting_colour in starting_piece:
#         player_1.add(vars()[starting_piece])
#     else:
#         player_2.add(vars()[starting_piece])
#     all_sprites.add(vars()[starting_piece])


# - mainloop -

clock = pygame.time.Clock()

running = True

while running:

    # - events -

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                Board.select_event(event)


        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                Board.place_event(event)

        elif event.type == pygame.MOUSEMOTION:
            Board.move_event(event)




    # - updates (without draws) -

    # empty

    # - draws (without updates) -

    screen.fill(WHITE)
    screen.blit(BackGround.image, BackGround.rect)

    for entity in Board.all_sprites:
        screen.blit(entity.image, entity.rect)


    pygame.display.flip()

    # - constant game speed / FPS -

    clock.tick(FPS)

# - end -

pygame.quit()

