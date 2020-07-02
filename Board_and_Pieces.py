import pygame
from positions import positions, starting_positions

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

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        super(Background, self).__init__()  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Piece(pygame.sprite.Sprite):
    def __init__(self, name, piece, colour, starting_location, starting_position):
        super(Piece, self).__init__()  #call Sprite initializer
        self.image = pygame.image.load(f'images/{piece}_{colour}.png')
        self.rect = self.image.get_rect()
        self.rect.center = starting_location
        self.name = name
        self.colour = colour
        self.starting_position = starting_position
        self.current_position = starting_position
        self.dragging = False

class Pawn(Piece):
    def __init__(self, name, colour, starting_location, starting_position):
        self.piece = 'pawn'
        super(Pawn, self).__init__(name, self.piece, colour, starting_location, starting_position)

    def possible_moves(self, current_state):
        possible_moves_clean = []
        current_position_raw = [letter_conversion[self.current_position[0]],int(self.current_position[1])]
        
        if 'white' in self.name:
            forward = [0,1]
        else:
            forward = [0,-1]

        right = [1,0]
        left =[-1,0]
        directions = [right,left]

        if self.current_position == self.starting_position:
            double_forward = True
        else:
            double_forward = False

        # try moving forward 1
        possible_move_raw = [sum(x) for x in zip(forward, current_position_raw)]

        letter = list(letter_conversion.keys())[list(letter_conversion.values()).index(possible_move_raw[0])]
        possible_move_clean = letter + str(possible_move_raw[1])

        can_move = True
        for piece in current_state.keys():
            piece_colour = piece.split('_')[1]
            if current_state[piece] == possible_move_clean:
                double_forward = False
                can_move = False
        if can_move:
            possible_moves_clean.append(possible_move_clean)

        # try moving forward 2
        if double_forward:
            possible_move_raw = [sum(x) for x in zip(forward, current_position_raw)]
            possible_move_raw = [sum(x) for x in zip(forward, possible_move_raw)]
            
            letter = list(letter_conversion.keys())[list(letter_conversion.values()).index(possible_move_raw[0])]
            possible_move_clean = letter + str(possible_move_raw[1])

            can_move = True
            for piece in current_state.keys():
                piece_colour = piece.split('_')[1]
                if current_state[piece] == possible_move_clean:
                    double_forward = False
                    can_move = False
            if can_move:
                possible_moves_clean.append(possible_move_clean)

        for direction in directions:

            possible_move_raw = [sum(x) for x in zip(forward, current_position_raw)]
            possible_move_raw = [sum(x) for x in zip(direction, possible_move_raw)]
            if possible_move_raw[0] not in range(1,9) or possible_move_raw[1] not in range(1,9):
                continue
            letter = list(letter_conversion.keys())[list(letter_conversion.values()).index(possible_move_raw[0])]
            possible_move_clean = letter + str(possible_move_raw[1])

            can_move = False
            for piece in current_state.keys():
                piece_colour = piece.split('_')[1]
                if current_state[piece] == possible_move_clean and piece_colour != self.colour:
                    can_move = True
                    break
            
            if can_move:
                possible_moves_clean.append(possible_move_clean)

        return possible_moves_clean




class Rook(Piece):
    def __init__(self, name, colour, starting_location, starting_position):
        self.piece = 'rook'
        super(Rook, self).__init__(name, self.piece, colour, starting_location, starting_position)

    def possible_moves(self, current_state):
        possible_moves_clean = []
        current_position_raw = [letter_conversion[self.current_position[0]],int(self.current_position[1])]

        up = [0,1]
        down = [0,-1]
        right = [1,0]
        left = [-1,0]
        directions = [up,down,left,right]

        for direction in directions:
            previous_position_raw = current_position_raw
            can_move = True
            while can_move:
                possible_move_raw = [sum(x) for x in zip(direction, previous_position_raw)]
                previous_position_raw = possible_move_raw
                if possible_move_raw[0] not in range(1,9) or possible_move_raw[1] not in range(1,9):
                    break
                letter = list(letter_conversion.keys())[list(letter_conversion.values()).index(possible_move_raw[0])]
                possible_move_clean = letter + str(possible_move_raw[1])

                for piece in current_state.keys():
                    piece_colour = piece.split('_')[1]
                    if current_state[piece] == possible_move_clean:
                        if piece_colour != self.colour:
                            possible_moves_clean.append(possible_move_clean)
                        can_move = False
                if can_move:
                    possible_moves_clean.append(possible_move_clean)

        return possible_moves_clean
                        




class Knight(Piece):
    def __init__(self, name, colour, starting_location, starting_position):
        self.piece = 'knight'
        super(Knight, self).__init__(name, self.piece, colour, starting_location, starting_position)

    def possible_moves(self, current_state):
        possible_moves_clean = []
        current_position_raw = [letter_conversion[self.current_position[0]],int(self.current_position[1])]

        up_right = [1,2]
        up_left = [-1,2]
        down_right = [1,-2]
        down_left = [-1,-2]
        right_up = [2,1]
        right_down = [2,-1]
        left_up = [-2,1]
        left_down = [-2,-1]
        directions = [up_right,up_left,down_right,down_left,right_up,right_down,left_up,left_down]

        for direction in directions:

            possible_move_raw = [sum(x) for x in zip(direction, current_position_raw)]
            if possible_move_raw[0] not in range(1,9) or possible_move_raw[1] not in range(1,9):
                continue
            letter = list(letter_conversion.keys())[list(letter_conversion.values()).index(possible_move_raw[0])]
            possible_move_clean = letter + str(possible_move_raw[1])

            can_move = True
            for piece in current_state.keys():
                piece_colour = piece.split('_')[1]
                if current_state[piece] == possible_move_clean and piece_colour == self.colour:
                    can_move = False
                    break

            if can_move:
                possible_moves_clean.append(possible_move_clean)

        return possible_moves_clean





class Bishop(Piece):
    def __init__(self, name, colour, starting_location, starting_position):
        self.piece = 'bishop'
        super(Bishop, self).__init__(name, self.piece, colour, starting_location, starting_position)

    def possible_moves(self, current_state):
        possible_moves_clean = []
        current_position_raw = [letter_conversion[self.current_position[0]],int(self.current_position[1])]

        up_right = [1,1]
        up_left = [-1,1]
        down_right = [1,-1]
        down_left = [-1,-1]
        directions = [up_right,up_left,down_right,down_left]

        for direction in directions:
            previous_position_raw = current_position_raw
            can_move = True
            while can_move:
                possible_move_raw = [sum(x) for x in zip(direction, previous_position_raw)]
                previous_position_raw = possible_move_raw
                if possible_move_raw[0] not in range(1,9) or possible_move_raw[1] not in range(1,9):
                    break
                letter = list(letter_conversion.keys())[list(letter_conversion.values()).index(possible_move_raw[0])]
                possible_move_clean = letter + str(possible_move_raw[1])

                for piece in current_state.keys():
                    piece_colour = piece.split('_')[1]
                    if current_state[piece] == possible_move_clean:
                        if piece_colour != self.colour:
                            possible_moves_clean.append(possible_move_clean)
                        can_move = False
                if can_move:
                    possible_moves_clean.append(possible_move_clean)

        return possible_moves_clean

class Queen(Piece):
    def __init__(self, name, colour, starting_location, starting_position):
        self.piece = 'queen'
        super(Queen, self).__init__(name, self.piece, colour, starting_location, starting_position)

    def possible_moves(self, current_state):
        possible_moves_clean = []
        current_position_raw = [letter_conversion[self.current_position[0]],int(self.current_position[1])]

        up = [0,1]
        down = [0,-1]
        right = [1,0]
        left = [-1,0]
        up_right = [1,1]
        up_left = [-1,1]
        down_right = [1,-1]
        down_left = [-1,-1]
        directions = [up,down,left,right,up_right,up_left,down_right,down_left]

        for direction in directions:
            previous_position_raw = current_position_raw
            can_move = True
            while can_move:
                possible_move_raw = [sum(x) for x in zip(direction, previous_position_raw)]
                previous_position_raw = possible_move_raw
                if possible_move_raw[0] not in range(1,9) or possible_move_raw[1] not in range(1,9):
                    break
                letter = list(letter_conversion.keys())[list(letter_conversion.values()).index(possible_move_raw[0])]
                possible_move_clean = letter + str(possible_move_raw[1])

                for piece in current_state.keys():
                    piece_colour = piece.split('_')[1]
                    if current_state[piece] == possible_move_clean:
                        if piece_colour != self.colour:
                            possible_moves_clean.append(possible_move_clean)
                        can_move = False
                if can_move:
                    possible_moves_clean.append(possible_move_clean)

        return possible_moves_clean

class King(Piece):
    def __init__(self, name, colour, starting_location, starting_position):
        self.piece = 'king'
        super(King, self).__init__(name, self.piece, colour, starting_location, starting_position)
    
    def possible_moves(self, current_state):
        possible_moves_clean = []
        current_position_raw = [letter_conversion[self.current_position[0]],int(self.current_position[1])]

        up = [0,1]
        down = [0,-1]
        right = [1,0]
        left = [-1,0]
        up_right = [1,1]
        up_left = [-1,1]
        down_right = [1,-1]
        down_left = [-1,-1]
        directions = [up,down,left,right,up_right,up_left,down_right,down_left]

        for direction in directions:

            possible_move_raw = [sum(x) for x in zip(direction, current_position_raw)]
            if possible_move_raw[0] not in range(1,9) or possible_move_raw[1] not in range(1,9):
                continue
            letter = list(letter_conversion.keys())[list(letter_conversion.values()).index(possible_move_raw[0])]
            possible_move_clean = letter + str(possible_move_raw[1])

            can_move = True
            for piece in current_state.keys():
                piece_colour = piece.split('_')[1]
                if current_state[piece] == possible_move_clean and piece_colour == self.colour:
                    can_move = False
                    break
            if can_move:
                possible_moves_clean.append(possible_move_clean)

        return possible_moves_clean