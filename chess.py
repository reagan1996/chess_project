# each square: w=57 h = 57

# left bottom w=21 h=21


# right top w=25 h=25

from positions import positions, starting_positions
from Board_and_Pieces import *
from Events import *

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

player_1 = pygame.sprite.Group()
player_2 = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

starting_colour = 'white'
current_turn = starting_colour


for starting_piece in starting_positions.keys():
    piece,colour = starting_piece.split('_')[:2]
    starting_location = positions[starting_positions[starting_piece]][2]
    starting_position = starting_positions[starting_piece]
    vars()[starting_piece] = vars()[piece.capitalize()](starting_piece,colour,starting_location,starting_position)

    if starting_colour in starting_piece:
        player_1.add(vars()[starting_piece])
    else:
        player_2.add(vars()[starting_piece])
    all_sprites.add(vars()[starting_piece])


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
                state = current_state(all_sprites)
                game_ended = stalemate_or_checkmate(all_sprites,state, current_turn)
                if game_ended:
                    print(game_ended)
                else:
                    for piece in all_sprites:
                        if piece.colour != current_turn:
                            continue

                        if piece.rect.collidepoint(event.pos):
                            piece.dragging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = piece.rect.x - mouse_x
                            offset_y = piece.rect.y - mouse_y


        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for piece in all_sprites:
                    if piece.dragging == True:

                        Mouse_x, Mouse_y = pygame.mouse.get_pos()
                        off_board = True
                        for position in positions.keys():
                            if Mouse_x in range(positions[position][0][0],positions[position][0][1]) and Mouse_y in range(positions[position][1][0],positions[position][1][1]):
                                on_board = False
                                state = current_state(all_sprites)
                                possible_moves = piece.possible_moves(state)
                                # if can move ...
                                if position in possible_moves:
                                    # .. check if you are in check after move
                                    new_state = {key:val for key, val in state.items() if val != position}
                                    new_state[piece.name] = position
                                    check = in_check(all_sprites,new_state, current_turn)
                                    # if put in check don't move
                                    if check:
                                        print('check')
                                        piece.rect.center = positions[piece.current_position][2]
                                    else:
                                        # ... delete any piece in the new position
                                        for other_piece in all_sprites:
                                            if other_piece.current_position == position:
                                                other_piece.kill()
                                        # move this piece into the center of the new position
                                        piece.rect.center = positions[position][2]
                                        piece.current_position = position
                                        # change turns if the player moves
                                        if current_turn == 'white':
                                            current_turn = 'black'
                                        else:
                                            current_turn = 'white'
                                        if piece.piece == 'pawn':
                                                if piece.colour == 'white':
                                                    promotion_number = 8
                                                else:
                                                    promotion_number = 1

                                                name, colour, starting_location, starting_position = [piece.name, piece.colour, piece.rect.center, piece.current_position]
                                                if int(piece.current_position[1]) == promotion_number:
                                                    piece.kill()
                                                    vars()[piece.name] = Queen(piece.name, piece.colour, piece.rect.center, piece.current_position)
                                                    all_sprites.add(vars()[piece.name])
                                else:
                                    piece.rect.center = positions[piece.current_position][2]
                        if off_board:
                            piece.rect.center = positions[piece.current_position][2]

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

