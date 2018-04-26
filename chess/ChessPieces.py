'''
Define behaviour of all chess pieces
1. actions - The actions they can perform
2. speed - The speed they can move
3. pos - Their current position on the board
4. player - The player they are associated with
'''
class Piece():
    def __init__(self, name, pos, player):
        self.name = name
        self.pos = pos
        self.player = player

    def __str__(self):    
        return self.name
    
    __repr__ = __str__
class King(Piece):
    def __init__(self, pos, player, name="King"):
        super().__init__(name, pos, player)
        self.actions = [(1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1, 1), (0,1), (1,1)]
        self.speed = [1]

class Queen(Piece):
    def __init__(self, pos, player, name="Queen"):
        super().__init__(name, pos, player)
        self.actions = [(1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1, 1), (0,1), (1,1)]
        self.speed = [1,2,3,4,5,6,7,8]

class Rook(Piece):
    def __init__(self, pos, player, name="Rook"):
        super().__init__(name, pos, player)
        self.actions = [(1,0), (0,-1), (-1,0), (0,1)]
        self.speed = [1,2,3,4,5,6,7,8]

class Bishop(Piece):
    def __init__(self, pos, player, name="Bishop"):
        super().__init__(name, pos, player)
        self.actions = [(1,1), (1,-1), (-1,-1), (-1,1)]
        self.speed = [1,2,3,4,5,6,7,8]

class Knight(Piece):
    def __init__(self, pos, player, name="Knight"):
        super().__init__(name, pos, player)
        self.actions = [(2,1), (2,-1), (-2,1), (-2,-1), (-2,-1), (-2,1), (-1,2), (1,2)]
        self.speed = [1]

class Pawn(Piece):
    def __init__(self, pos, player, name="Pawn"):
        super().__init__(name, pos, player)
        self.actions = [(-1,1), (1,1), (0,1)]
        self.speed = [1]

