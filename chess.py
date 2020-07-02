# each square: w=57 h = 57

# left bottom w=21 h=21


# right top w=25 h=25

from positions import positions, starting_positions
from Board_and_Pieces import *

import pygame


# --- constants --- (UPPER_CASE names)

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 498

#BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
# RED   = (255,   0,   0)

FPS = 30



# --- functions --- (lower_case names)

# --- main ---

# - init -

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Chess")

# - objects -

BackGround = Background('images/board.png', [0,0])


player_1 = pygame.sprite.Group()
player_2 = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


# initialize board
for starting_piece in starting_positions.keys():
    piece,colour = starting_piece.split('_')[:2]
    starting_location = positions[starting_positions[starting_piece]][2]
    starting_position = starting_positions[starting_piece]
    vars()[starting_piece] = vars()[piece.capitalize()](starting_piece,colour,starting_location,starting_position)

    if 'white' in starting_piece:
        player_1.add(vars()[starting_piece])
    else:
        player_2.add(vars()[starting_piece])
    all_sprites.add(vars()[starting_piece])


def current_state(all_sprites):
    state = {}
    for piece in all_sprites:
        state[piece.name] = piece.current_position
    return state

starting_colour = 'white'
current_turn = starting_colour

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
                for piece in all_sprites:

                    if current_turn not in piece.name:
                        continue

                    if piece.rect.collidepoint(event.pos):
                        piece.dragging = True
                        mouse_x, mouse_y = event.pos
                        offset_x = piece.rect.x - mouse_x
                        offset_y = piece.rect.y - mouse_y
                        state = current_state(all_sprites)
                        print(piece.possible_moves(state))

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for piece in all_sprites:
                    if piece.dragging == True:

                        Mouse_x, Mouse_y = pygame.mouse.get_pos()
                        for position in positions.keys():
                            if Mouse_x in range(positions[position][0][0],positions[position][0][1]) and Mouse_y in range(positions[position][1][0],positions[position][1][1]):
                                can_move = True
                                for other_piece in all_sprites:
                                    if other_piece.current_position == position:
                                        if (piece in player_1 and other_piece in player_1) or (piece in player_2 and other_piece in player_2):
                                            piece.rect.center = positions[piece.current_position][2]
                                            can_move = False
                                        else:
                                            other_piece.kill()
                                if can_move:
                                    piece.rect.center = positions[position][2]
                                    piece.current_position = position
                                    # change turns on if the player moves
                                    if current_turn == 'white':
                                        current_turn = 'black'
                                    else:
                                        current_turn = 'white'
                        piece.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            for piece in all_sprites:
                if piece.dragging:
                    mouse_x, mouse_y = event.pos
                    piece.rect.x = mouse_x + offset_x
                    piece.rect.y = mouse_y + offset_y




    # - updates (without draws) -

    # empty

    # - draws (without updates) -

    screen.fill(WHITE)
    screen.blit(BackGround.image, BackGround.rect)

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)


    pygame.display.flip()

    # - constant game speed / FPS -

    clock.tick(FPS)

# - end -

pygame.quit()

