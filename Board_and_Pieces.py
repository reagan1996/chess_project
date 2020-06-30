import pygame
from positions import positions, starting_positions

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
        self.starting_position = starting_position
        self.current_position = starting_position
        self.dragging = False

class Pawn(Piece):
    def __init__(self, name, colour, starting_location, starting_position):
        self.piece = 'pawn'
        super(Pawn, self).__init__(name, self.piece, colour, starting_location, starting_position)

    def possible_moves():
            pass

class Rook(Piece):
    def __init__(self, name, colour, starting_location, starting_position):
        self.piece = 'rook'
        super(Rook, self).__init__(name, self.piece, colour, starting_location, starting_position)

        def possible_moves():
            pass

class Knight(Piece):
    def __init__(self, name, colour, starting_location, starting_position):
        self.piece = 'knight'
        super(Knight, self).__init__(name, self.piece, colour, starting_location, starting_position)

        def possible_moves():
            pass

class Bishop(Piece):
    def __init__(self, name, colour, starting_location, starting_position):
        self.piece = 'bishop'
        super(Bishop, self).__init__(name, self.piece, colour, starting_location, starting_position)

        def possible_moves():
            pass

class Queen(Piece):
    def __init__(self, name, colour, starting_location, starting_position):
        self.piece = 'queen'
        super(Queen, self).__init__(name, self.piece, colour, starting_location, starting_position)

    def possible_moves():
            pass

class King(Piece):
    def __init__(self, name, colour, starting_location, starting_position):
        self.piece = 'king'
        super(King, self).__init__(name, self.piece, colour, starting_location, starting_position)
    
    def possible_moves():
            pass