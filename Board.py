from positions import positions, starting_positions
from Pieces import *

import pygame

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        super(Background, self).__init__()  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Board:
    def __init__(self, starting_positions):
        self.player_1 = pygame.sprite.Group()
        self.player_2 = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        self.starting_colour = 'white'
        self.current_turn = self.starting_colour

        self.initiate_board(starting_positions)

    def initiate_board(self,starting_positions):
        for starting_piece in starting_positions.keys():
            piece,colour = starting_piece.split('_')[:2]
            starting_position = starting_positions[starting_piece]
            starting_location = positions[starting_position][2]
            
            vars()[starting_piece] = globals()[piece.capitalize()](starting_piece,colour,starting_location,starting_position)

            if self.starting_colour in starting_piece:
                self.player_1.add(vars()[starting_piece])
            else:
                self.player_2.add(vars()[starting_piece])
            self.all_sprites.add(vars()[starting_piece])

    def current_state(self):
        state = {}
        for piece in self.all_sprites:
            state[piece.name] = piece.current_position
        return state

    def select_event(self,event):
        state = self.current_state()
        game_ended = self.stalemate_or_checkmate(state,self.current_turn)
        if game_ended:
            print(game_ended)
        else:
            for piece in self.all_sprites:
                if piece.colour != self.current_turn:
                    continue

                if piece.rect.collidepoint(event.pos):
                    piece.dragging = True
                    mouse_x, mouse_y = event.pos
                    self.offset_x = piece.rect.x - mouse_x
                    self.offset_y = piece.rect.y - mouse_y

    def place_event(self,event):
        for piece in self.all_sprites:
            if piece.dragging == True:

                Mouse_x, Mouse_y = pygame.mouse.get_pos()
                off_board = True
                for position in positions.keys():
                    if Mouse_x in range(positions[position][0][0],positions[position][0][1]) and Mouse_y in range(positions[position][1][0],positions[position][1][1]):
                        off_board = False
                        state = self.current_state()
                        possible_moves = piece.possible_moves(state)
                        # if can move ...
                        if position in possible_moves:
                            # .. check if you are in check after move
                            new_state = {key:val for key, val in state.items() if val != position}
                            new_state[piece.name] = position
                            check = self.in_check(new_state, self.current_turn)
                            # if put in check don't move
                            if check:
                                print("check")
                                piece.rect.center = positions[piece.current_position][2]
                            else:
                                # ... delete any piece in the new position
                                for other_piece in self.all_sprites:
                                    if other_piece.current_position == position:
                                        other_piece.kill()
                                # move this piece into the center of the new position
                                piece.rect.center = positions[position][2]
                                piece.current_position = position
                                # change turns if the player moves
                                if self.current_turn == 'white':
                                    self.current_turn = 'black'
                                else:
                                    self.current_turn = 'white'
                                # promote pawn if possible
                                piece = self.promote_pawn(piece)
                        else:
                            piece.rect.center = positions[piece.current_position][2]
                if off_board:
                    piece.rect.center = positions[piece.current_position][2]

                piece.dragging = False

    def move_event(self,event):
        for piece in self.all_sprites:
            if piece.dragging:
                mouse_x, mouse_y = event.pos
                piece.rect.x = mouse_x + self.offset_x
                piece.rect.y = mouse_y + self.offset_y

    def promote_pawn(self,piece):
        if piece.colour == 'white':
            promotion_number = 8
        else:
            promotion_number = 1

        name, colour, starting_location, starting_position = [piece.name, piece.colour, piece.rect.center, piece.current_position]
        if int(piece.current_position[1]) == promotion_number:
            piece.kill()
            vars()[name] = globals()['Queen'](name, colour, starting_location, starting_position)
            self.all_sprites.add(vars()[name])
            return vars()[name]
        else:
            return piece

    def in_check(self,current_state, colour):
        all_moves = []
        for piece in self.all_sprites:
            if piece.colour != colour:
                if piece.name in current_state:
                    possible_moves = piece.possible_moves(current_state)
                    all_moves += possible_moves

        for piece in self.all_sprites:
            if piece.piece == 'king' and piece.colour == colour:
                if current_state[piece.name] in all_moves:
                    return True
                return False

    def checkmate(self,current_state, colour):
        '''checks if colour is in checkmate'''
        checkmate = True
        for piece in self.all_sprites:
            if piece.colour == colour:
                possible_moves = piece.possible_moves(current_state)
                for move in possible_moves:
                    new_state = {key:val for key, val in current_state.items() if val != move}
                    new_state[piece.name] = move
                    check = self.in_check(new_state, colour)
                    if not check:
                        return False
        return True

    def stalemate_or_checkmate(self,current_state, colour):
        if self.checkmate(current_state, colour):
            if self.in_check(current_state, colour):
                return 'checkmate'
            else:
                return 'stalemate'
        return False