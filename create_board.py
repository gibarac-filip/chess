import numpy as np
# Define the square representation using numeric codes
""""
class game:
    def __init__(self, winner, check_status):
        self.winner = None
        self.check_status = None
    
    def announce_winner(self):
        print("winner is %s" % self.winner)
"""
        
class Piece:
    def __init__(self, color, value, name, initial):
        self.color = color
        self.value = value
        self.name = name
        self.inital = initial
        self.has_moved = False

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 1, 'Pawn', 'P')

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 3, 'Knight', 'N')

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, 3, 'Bishop', 'B')

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 5, "Rook", "R")

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 8, 'Queen', 'Q')

class King(Piece):
    def __init__(self, color):
        super().__init__(color, 9, 'King', 'K')

def game_setup():
    global SQUARES, FILE_MAP
    
    SQUARES = {
    'a1': 0,  'b1': 1,  'c1': 2,  'd1': 3,  'e1': 4,  'f1': 5,  'g1': 6,  'h1': 7,
    'a2': 8,  'b2': 9,  'c2': 10, 'd2': 11, 'e2': 12, 'f2': 13, 'g2': 14, 'h2': 15,
    'a3': 16, 'b3': 17, 'c3': 18, 'd3': 19, 'e3': 20, 'f3': 21, 'g3': 22, 'h3': 23,
    'a4': 24, 'b4': 25, 'c4': 26, 'd4': 27, 'e4': 28, 'f4': 29, 'g4': 30, 'h4': 31,
    'a5': 32, 'b5': 33, 'c5': 34, 'd5': 35, 'e5': 36, 'f5': 37, 'g5': 38, 'h5': 39,
    'a6': 40, 'b6': 41, 'c6': 42, 'd6': 43, 'e6': 44, 'f6': 45, 'g6': 46, 'h6': 47,
    'a7': 48, 'b7': 49, 'c7': 50, 'd7': 51, 'e7': 52, 'f7': 53, 'g7': 54, 'h7': 55,
    'a8': 56, 'b8': 57, 'c8': 58, 'd8': 59, 'e8': 60, 'f8': 61, 'g8': 62, 'h8': 63
    }
    
    FILE_MAP = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    # Accessing the numeric code for a square
    #square = 'e4'
    #numeric_code = SQUARES[square]
    #print(numeric_code)  # Output: 28

    # Reverse lookup - Getting the algebraic notation for a numeric code
    #numeric_code = 34
    #algebraic_notation = next(key for key, value in SQUARES.items() if value == numeric_code)
    #print(algebraic_notation)  # Output: 'c5'
        
    current_player = "white"
    castling_rights = {
        "white_kingside": True,
        "white_queenside": True,
        "black_kingside": True,
        "black_queenside": True,
    }
    en_passant_square = None
    half_move_counter = 0
    full_move_counter = 0
    starting_board = [
        [Rook('white'), Knight('white'), Bishop('white'), Queen('white'), King('white'), Bishop('white'), Knight('white'), Rook('white')],
        [Pawn('white') for _ in range(8)],
        [Piece(None, None, None, 0) for _ in range(8)],
        [Piece(None, None, None, 0) for _ in range(8)],
        [Piece(None, None, None, 0) for _ in range(8)],
        [Piece(None, None, None, 0) for _ in range(8)],
        [Pawn('black') for _ in range(8)],
        [Rook('black'), Knight('black'), Bishop('black'), Queen('black'), King('black'), Bishop('black'), Knight('black'), Rook('black')]
    ]

    return starting_board, current_player, castling_rights, en_passant_square, half_move_counter, full_move_counter

# Define rule checks for movements
#PAWN
def generate_pawn_moves(board, current_square):

    legal_moves = []
    flattened_board = []
    for sub_array in board:
        flattened_board.extend(sub_array)

    # Calculate the target square for a single square advance
    try: current_square = SQUARES[current_square]
    except: current_square = current_square
    
    # Determine the direction of pawn movement based on its color
    direction = 1 if flattened_board[current_square].color == "white" else -1
    
    if flattened_board[current_square].name != 'Pawn':
        return []
    else:
        single_square = current_square + 8 * direction

        # Check if the single square advance is a legal move
        if flattened_board[single_square].value == None:
            legal_moves.append(single_square)

        # Calculate the target square for a double square advance from the initial rank
        double_square = current_square + 16 * direction

        # Check if the double square advance is a legal move
        if ((flattened_board[current_square].color == "white" and current_square < 32) or (not flattened_board[current_square].color == "white" and current_square >= 32 and current_square <= 55)):
            if flattened_board[single_square].value == None:
                legal_moves.append(double_square)

        # Calculate the target squares for diagonal captures
        capture_squares = [current_square + 7 * direction, current_square + 9 * direction]
        #capture_squares = 15,17

        # Check if diagonal captures are legal moves
        for square in capture_squares:
            #square = 17
            if abs(FILE_MAP[next(key for key, value in SQUARES.items() if value == abs(min(square,63)))[0]] - FILE_MAP[next(key for key, value in SQUARES.items() if value == current_square)[0]]) == 1:
                if square >= 0 and square < 64:
                    if (flattened_board[current_square].color != flattened_board[square].color) and (flattened_board[square].value != None):
                        legal_moves.append(square)
        
        legal_moves_pawn = []
        for i in range(len(legal_moves)):
            legal_moves_pawn.append(next(key for key, value in SQUARES.items() if value == legal_moves[i]))

        return legal_moves_pawn

#KNIGHT
def generate_knight_moves(board, current_square):

    legal_moves = []
    flattened_board = []
    for sub_array in board:
        flattened_board.extend(sub_array)
    
    # flattened_board[SQUARES['e4']] = Knight('white'); flattened_board[SQUARES['f6']] = Knight('white') 
    # flattened_board[SQUARES['c3']] = Knight('black'); flattened_board[SQUARES['b5']] = Knight('black')
    # test_board = np.array(flattened_board).reshape(8,8)
     
    # Calculate the target square for a single square advance
    try: current_square = SQUARES[current_square]
    except: current_square = current_square
    
    if flattened_board[current_square].name != "Knight":
        return []
    else:
        offsets = [-17, -15, -10, -6, 6, 10, 15, 17]
        # current_square = 'c3'
        # target_square = 'b5'
        # target_square = SQUARES[target_square] 
        # next(key for key, value in SQUARES.items() if value == target_square) 
        for offset in offsets:
            # offset = 15
            target_square = current_square + offset
            target_square = abs(min(max(target_square,0), 63))
            current_file = FILE_MAP[next(key for key, value in SQUARES.items() if value == current_square)[0]]
            target_file = FILE_MAP[next(key for key, value in SQUARES.items() if value == target_square)[0]]

            if abs(target_file - current_file) == 1 or abs(target_file - current_file) == 2:
                if target_square >= 0 and target_square < 64:
                    if flattened_board[current_square].color != flattened_board[target_square].color:
                        legal_moves.append(target_square)

    legal_moves_knight = []
    for i in range(len(legal_moves)):
        legal_moves_knight.append(next(key for key, value in SQUARES.items() if value == legal_moves[i]))

    return legal_moves_knight

generate_knight_moves(test_board, 'b1')

#BISHOP
def generate_bishop_moves(board, current_square):

    legal_moves = []
    flattened_board = []
    for sub_array in board:
        flattened_board.extend(sub_array)
    
    # flattened_board[SQUARES['d4']] = Bishop('white'); flattened_board[SQUARES['e4']] = Bishop('white') 
    # flattened_board[SQUARES['d5']] = Bishop('black'); flattened_board[SQUARES['e5']] = Bishop('black')
    # test_board = np.array(flattened_board).reshape(8,8)
     
    # Calculate the target square for a single square advance
    # current_square = 'd4'
    try: current_square = SQUARES[current_square]
    except: current_square = current_square
    
    if flattened_board[current_square].name != "Bishop":
        return []
    else:
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for direction in directions:

            d_file, d_rank = direction
            # d_file, d_rank = 1,1
            
            current_file = FILE_MAP[next(key for key, value in SQUARES.items() if value == current_square)[0]]+1
            current_rank = int(next(key for key, value in SQUARES.items() if value == current_square)[1])    
            
            target_square = current_square
            #target_square = 36
            iterative_index = 0
            while iterative_index == 0:
                target_square += d_file * 8 + d_rank
                try: target_file = FILE_MAP[next(key for key, value in SQUARES.items() if value == target_square)[0]]+1
                except: target_file = -1
                try: target_rank = int(next(key for key, value in SQUARES.items() if value == target_square)[1])
                except: target_rank = -1
                #cannot be transported to the other side of the map
                if (target_square < 0 or target_square >= 64) or (abs((current_file - target_file) / (current_rank - target_rank)) != 1):
                    i=1
                    break
                else:
                    piece_on_target = flattened_board[target_square]
                    if piece_on_target.value == 0 :
                        legal_moves.append(target_square)
                    elif piece_on_target.value != 0 and (piece_on_target.color != flattened_board[current_square].color):
                        legal_moves.append(target_square)
                        i=1
                        break
                    elif piece_on_target.value != 0 and (piece_on_target.color == flattened_board[current_square].color):
                        i=1
                        break
                    else: 
                        i=1
                        break

        legal_moves_bishop = [next(key for key, value in SQUARES.items() if value == square) for square in sorted(legal_moves)]

        return legal_moves_bishop

generate_bishop_moves(test_board, 'd4')

#ROOK
def generate_rook_moves(board, current_square):

    legal_moves = []
    flattened_board = []
    for sub_array in board:
        flattened_board.extend(sub_array)
    
    # flattened_board[SQUARES['d4']] = Rook('white'); flattened_board[SQUARES['e4']] = Rook('white') 
    # flattened_board[SQUARES['d5']] = Rook('black'); flattened_board[SQUARES['e5']] = Rook('black')
    # test_board = np.array(flattened_board).reshape(8,8)
    # board = test_board
     
    # Calculate the target square for a single square advance
    # current_square = 'd4'
    try: current_square = SQUARES[current_square]
    except: current_square = current_square
    
    if flattened_board[current_square].name != "Rook":
        return []
    else:
        directions = [(1, 0), (-1,0), (0,1), (0,-1)]
        for direction in directions:

            d_file, d_rank = direction
            # d_file, d_rank = 1,1
            
            current_file = FILE_MAP[next(key for key, value in SQUARES.items() if value == current_square)[0]]+1
            current_rank = int(next(key for key, value in SQUARES.items() if value == current_square)[1])    
            
            target_square = current_square
            #target_square = 36
            iterative_index = 0
            while iterative_index == 0:
                target_square += d_file * 8 + d_rank
                try: target_file = FILE_MAP[next(key for key, value in SQUARES.items() if value == target_square)[0]]+1
                except: target_file = -1
                try: target_rank = int(next(key for key, value in SQUARES.items() if value == target_square)[1])
                except: target_rank = -1
                #cannot be transported to the other side of the map
                if (target_square < 0 or target_square >= 64) or (target_file != current_file and target_rank != current_rank):
                    iterative_index=1
                    break
                else:
                    piece_on_target = flattened_board[target_square]
                    if piece_on_target.value == 0 :
                        legal_moves.append(target_square)
                    elif piece_on_target.value != 0 and (piece_on_target.color != flattened_board[current_square].color):
                        legal_moves.append(target_square)
                        iterative_index=1
                        break
                    elif piece_on_target.value != 0 and (piece_on_target.color == flattened_board[current_square].color):
                        iterative_index=1
                        break
                    else:
                        iterative_index=1
                        break

        legal_moves_rook = [next(key for key, value in SQUARES.items() if value == square) for square in sorted(legal_moves)]

        return legal_moves_rook

generate_rook_moves(test_board, 'd4')

#QUEEN
def generate_queen_moves(board, current_square):

    legal_moves = []
    flattened_board = []
    for sub_array in board:
        flattened_board.extend(sub_array)
    
    # flattened_board[SQUARES['d4']] = Queen('white'); flattened_board[SQUARES['e4']] = Queen('white') 
    # flattened_board[SQUARES['d5']] = Queen('black'); flattened_board[SQUARES['e5']] = Queen('black')
    # test_board = np.array(flattened_board).reshape(8,8)
    # board = test_board
     
    # Calculate the target square for a single square advance
    # current_square = 'd4'
    try: current_square = SQUARES[current_square]
    except: current_square = current_square
    
    if flattened_board[current_square].name != "Queen":
        return []
    else:
        directions = [(1, 0), (-1,0), (0,1), (0,-1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for direction in directions:

            d_file, d_rank = direction
            # d_file, d_rank = 1,1
            
            current_file = FILE_MAP[next(key for key, value in SQUARES.items() if value == current_square)[0]]+1
            current_rank = int(next(key for key, value in SQUARES.items() if value == current_square)[1])    
            
            target_square = current_square
            #target_square = 36
            iterative_index = 0
            while iterative_index == 0:
                target_square += d_file * 8 + d_rank
                try: target_file = FILE_MAP[next(key for key, value in SQUARES.items() if value == target_square)[0]]+1
                except: target_file = -1
                try: target_rank = int(next(key for key, value in SQUARES.items() if value == target_square)[1])
                except: target_rank = -1
                #cannot be transported to the other side of the map
                if (target_square < 0 or target_square >= 64) or (target_file != current_file and target_rank != current_rank and abs((current_file - target_file) / (current_rank - target_rank)) != 1):
                    iterative_index=1
                    break
                else:
                    piece_on_target = flattened_board[target_square]
                    if piece_on_target.value == 0 :
                        legal_moves.append(target_square)
                    elif piece_on_target.value != 0 and (piece_on_target.color != flattened_board[current_square].color):
                        legal_moves.append(target_square)
                        iterative_index=1
                        break
                    elif piece_on_target.value != 0 and (piece_on_target.color == flattened_board[current_square].color):
                        iterative_index=1
                        break
                    else:
                        iterative_index=1
                        break

        legal_moves_queen = [next(key for key, value in SQUARES.items() if value == square) for square in sorted(legal_moves)]

        return legal_moves_queen

generate_queen_moves(test_board, 'd4')

#KING
#Supporting King Functions: is_king_square_attacked, is_castling_allowed, get_castling_moves
def is_king_square_attacked(board, target_square, attacker_color):
    #is_king_square_attacked(board, 1, flattened_board[current_square].color)
    #is_king_square_attacked(board, 8, flattened_board[current_square].color)
    #is_king_square_attacked(board, 9, flattened_board[current_square].color)

    flattened_board = []
    for sub_array in board:
        flattened_board.extend(sub_array)
    #attacker_color = flattened_board[current_square].color
    attacker_color = "black" if attacker_color == "white" else "white"
    #target_square = 1

    while True:
        for i in range(64):
            legal_pawn_moves = generate_pawn_moves(board, i)
            legal_bishop_moves = generate_bishop_moves(board, i)
            legal_knight_moves = generate_knight_moves(board, i)
            legal_rook_moves = generate_rook_moves(board, i)
            legal_queen_moves = generate_queen_moves(board, i)
            target_file = FILE_MAP[next(key for key, value in SQUARES.items() if value == target_square)[0]]+1
            target_rank = int(next(key for key, value in SQUARES.items() if value == target_square)[1])  
            if next(key for key, value in SQUARES.items() if value == target_square) in legal_pawn_moves and flattened_board[i].color == attacker_color:
                print("pawn from", next(key for key, value in SQUARES.items() if value == i), "attacking king")
                return True
            if next(key for key, value in SQUARES.items() if value == target_square) in legal_bishop_moves and flattened_board[i].color == attacker_color:
                print("bishop from", next(key for key, value in SQUARES.items() if value == i), "attacking king")
                return True
            if next(key for key, value in SQUARES.items() if value == target_square) in legal_knight_moves and flattened_board[i].color == attacker_color:
                print("knight from", next(key for key, value in SQUARES.items() if value == i), "attacking king")
                return True
            if next(key for key, value in SQUARES.items() if value == target_square) in legal_rook_moves and flattened_board[i].color == attacker_color:
                print("rook from", next(key for key, value in SQUARES.items() if value == i), "attacking king")
                return True
            if next(key for key, value in SQUARES.items() if value == target_square) in legal_queen_moves and flattened_board[i].color == attacker_color:
                print("queen from", next(key for key, value in SQUARES.items() if value == i), "attacking king")
                return True
            if flattened_board[i].name == "King" and flattened_board[i].color == attacker_color:
                king_file = FILE_MAP[next(key for key, value in SQUARES.items() if value == i)[0]]+1
                king_rank = int(next(key for key, value in SQUARES.items() if value == i)[1])
                if abs(king_file-target_file) <= 1 and abs(king_rank-target_rank) <= 1:
                    print("king from", next(key for key, value in SQUARES.items() if value == i), "attacking king")
                    return True
        return False
                    

def is_castling_allowed(board, current_square):
    flattened_board = []
    for sub_array in board:
        flattened_board.extend(sub_array)
    try:
        current_square = SQUARES[current_square]
    except KeyError:
        current_square = current_square

    if flattened_board[current_square].name != "King":
        return False

    # Check if the king has not moved
    if flattened_board[current_square].has_moved:
        return False

    # Determine the castling direction and the squares involved
    if flattened_board[current_square].color == "white":
        king_row, rook1_col, rook2_col = 7, 0, 7
    else:
        king_row, rook1_col, rook2_col = 0, 0, 7

    # Check if the chosen rook has not moved
    rook1_square = king_row * 8 + rook1_col
    rook2_square = king_row * 8 + rook2_col

    if flattened_board[rook1_square].name != "Rook" or flattened_board[rook2_square].name != "Rook":
        return False

    if flattened_board[rook1_square].has_moved or flattened_board[rook2_square].has_moved:
        return False

    # Check if squares between the king and rook are empty
    empty_squares = [current_square + i for i in range(1, 3)]
    if any(flattened_board[square].value != 0 for square in empty_squares):
        return False

    # Check if squares the king moves through are not under attack
    squares_under_attack = [current_square + i for i in range(1, 4)]
    if any(is_king_square_attacked(board, square, flattened_board[current_square].color) for square in squares_under_attack):
        return False

    return True

def get_castling_moves(board, current_square):
    flattened_board = []
    for sub_array in board:
        flattened_board.extend(sub_array)
    try:
        current_square = SQUARES[current_square]
    except KeyError:
        current_square = current_square

    if flattened_board[current_square].name != "King":
        return []

    castling_moves = []
    king_row = current_square // 8

    # Determine the castling direction and squares involved
    if flattened_board[current_square].color == "white":
        king_col, rook_col = 4, 0
    else:
        king_col, rook_col = 4, 7
        
    if rook_col == 0:
        castling_moves.append(current_square - 2)  # Queenside castling
    else:
        castling_moves.append(current_square + 2)  # Kingside castling

    return castling_moves

def generate_king_moves(board, current_square):

    legal_moves = []
    flattened_board = []
    for sub_array in board:
        flattened_board.extend(sub_array)
    
    # flattened_board[SQUARES['b8']] = Rook('black'); flattened_board[SQUARES['c3']] = King('black') 
    # flattened_board[SQUARES['a1']] = King('white')
    # board = np.array(flattened_board).reshape(8,8)
     
    # Calculate the target square for a single square advance
    # current_square = 'a1'
    try: current_square = SQUARES[current_square]
    except: current_square = current_square
    
    current_file = FILE_MAP[next(key for key, value in SQUARES.items() if value == current_square)[0]]+1
    current_rank = int(next(key for key, value in SQUARES.items() if value == current_square)[1])    
    
    if flattened_board[current_square].name != "King":
        return []
    else:
        directions = [(1, 0), (-1,0), (0,1), (0,-1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for direction in directions:

            d_file, d_rank = direction
            # d_file, d_rank = 1,1   
            
            target_square = current_square
            # target_square = 1
            # next(key for key, value in SQUARES.items() if value == target_square)
            while True:
                target_square += d_file * 8 + d_rank
                try: target_file = FILE_MAP[next(key for key, value in SQUARES.items() if value == target_square)[0]]+1
                except: target_file = -1
                try: target_rank = int(next(key for key, value in SQUARES.items() if value == target_square)[1])
                except: target_rank = -1
                #cannot be transported to the other side of the map
                if (target_square < 0 or target_square >= 64):
                    print("break point 1")
                    break
                elif is_castling_allowed(board, current_square):
                    # You'll need to implement the is_castling_allowed function to check if castling is allowed
                    castling_moves = get_castling_moves(board, current_square)
                    legal_moves.extend(castling_moves)
                    print("adding castling moves?")
                else:
                    piece_on_target = flattened_board[target_square]
                    if piece_on_target.value == 0:
                        # is_king_square_attacked(board, 1, flattened_board[current_square].color) False
                        # is_king_square_attacked(board, 8, flattened_board[current_square].color) False, needs to be True
                        # is_king_square_attacked(board, 9, flattened_board[current_square].color) False, needs to be True
                        if not is_king_square_attacked(board, target_square, flattened_board[current_square].color) and abs(target_file - current_file) <= 1 and abs(target_rank - current_rank) <=1:
                            legal_moves.append(target_square)
                            print("adding not attacked empty square")
                    elif piece_on_target.value != 0 and (piece_on_target.color != flattened_board[current_square].color):
                        if not is_king_square_attacked(board, target_square, flattened_board[current_square].color) and abs(target_file - current_file) <= 1 and abs(target_rank - current_rank) <=1:
                            legal_moves.append(target_square)
                            print("add close empty square")
                            break
                    elif piece_on_target.value != 0 and (piece_on_target.color == flattened_board[current_square].color):
                        print("break point 3")
                        break
                    else:
                        print("break point 4")
                        break
        
        # sorted(legal_moves)
        legal_moves_king = [next(key for key, value in SQUARES.items() if value == square) for square in sorted(legal_moves)]

        return legal_moves_king

legal_moves_king(test_board, 'd4')

test_board = [
        [Rook('white'), Knight('white'), Bishop('white'), Queen('white'), King('white'), Bishop('white'), Knight('white'), Rook('white')],
        [Piece(None, 0, None, '_') for _ in range(8)],
        [Piece(None, 0, None, '_') for _ in range(8)],
        [Piece(None, 0, None, '_') for _ in range(8)],
        [Piece(None, 0, None, '_') for _ in range(8)],
        [Piece(None, 0, None, '_') for _ in range(8)],
        [Piece(None, 0, None, '_') for _ in range(8)],
        [Rook('black'), Knight('black'), Bishop('black'), Queen('black'), King('black'), Bishop('black'), Knight('black'), Rook('black')]
    ]
test_board = [
        [Piece(None, 0, None, '_') for _ in range(8)],
        [Piece(None, 0, None, '_') for _ in range(8)],
        [Piece(None, 0, None, '_') for _ in range(8)],
        [Piece(None, 0, None, '_') for _ in range(8)],
        [Piece(None, 0, None, '_') for _ in range(8)],
        [Piece(None, 0, None, '_') for _ in range(8)],
        [Piece(None, 0, None, '_') for _ in range(8)],
        [Piece(None, 0, None, '_') for _ in range(8)]
    ]
print_board(board)
# print_board(starting_board)
# print_board(test_board)

"""""
# Define rule checks for movements
def piece_movement_rules(move, piece, is_white):

    #taking pieces notation
    if "x" in move:
        source_square = move.replace("x", "")[:2]
        target_square = move.replace("x", "")[2:]
    #check notation
    elif "+" in move:
        source_square = move.replace("+", "")[:2]
        target_square = move.replace("+", "")[2:]
    #checkmate notation
    elif "#" in move:
        source_square = move.replace("#", "")[:2]
        target_square = move.replace("#", "")[2:]
    #promotion notation
    elif "=" in move:
        source_square = move.replace("=", "")[:2]
        target_square = move.replace("=", "")[2:]
    #regular moves
    else:
        source_square = move[:2]
        target_square = move[2:]
        
    # Convert algebraaic notation to numeric codes
    source_file = FILE_MAP[source_square[0]]
    source_rank = int(source_square[1])
        
    #first move has to be from a square that has a unit
    target_file = FILE_MAP[target_square[0]]
    target_rank = int(target_square[1])

    # Convert algebraic notation to numeric codes
    source_file = FILE_MAP[source_square[0]]
    source_rank = int(source_square[1])
    
    #first move has to be from a square that has a unit
    target_file = FILE_MAP[target_square[0]]
    target_rank = int(target_square[1])
    
    if source_file == target_file and target_rank == source_rank:
        result = False
    
    if piece == 1:
        if "x" in move:
            if target_file != source_file and target_rank == source_rank + 1:
                result = True
            else:
                result = False
        elif target_file != source_file:
            result = False
        elif is_white == "white":
            if target_rank == 4 and source_rank == 2:
                result = True
            elif target_rank == source_rank + 1:
                result = True
            else:
                result = False
        elif is_white == "black":
            if target_rank == 5 and source_rank == 7:
                result = True
            elif target_rank == source_rank - 1:
                result = True
            else:
                result = False
        else:
            result = True
    elif piece == 2: 
        if abs(target_rank - source_rank) == 1:
            if abs(target_file - source_file) == 2:
                result = True
            else:
                result = False
        if abs(target_rank - source_rank) == 2:
            if abs(target_file - source_file) == 1:
                result = True
            else:
                result = False
        else:
            result = False            
    elif piece == 3: 
        if abs(target_rank - source_rank) == abs(target_file - source_file):
            result = True
        else:
            result = False
    elif piece == 4: 
        if target_rank == source_rank or target_file == source_file:
            result = True
        else:
            result = False
    elif piece == 5: 
        if target_rank == source_rank:
                result = True
        elif target_file == source_file:
            result = True
        else:
            if abs(target_rank - source_rank) == abs(target_file - source_file):
                result = True
            else:
                result = False
    elif piece == 6:
        if abs(target_file - source_file) > 1 or abs(target_rank - source_rank) > 1:
            result = True
        else:
            result = False
    else: result = False
    return result


def print_board(board):
    for rank in range(8):
        for file in range(8):
            piece = board[rank][file]
            print(piece, end="")
        print()
"""""
        
def print_board(board):
    for rank in range(8):
        for file in range(8):
            piece = board[8-rank-1][file]
            print(piece.inital, end="  ")
        print()

print_board(board)

def reset_counters(h, f):
    h = 0
    f = 0

# Initialize first game state
board = game_setup()[0]
current_player = game_setup()[1]
castling_rights = game_setup()[2]
en_passant_square = game_setup()[3]
half_move_counter = game_setup()[4]
full_move_counter = game_setup()[5]

# Create a chessboard
print("Initial Chessboard:")
print_board(board)
print("Current player:", current_player, "\n"
      "Castling rights:", castling_rights, "\n"
      "En passant square:", en_passant_square, "\n"
      "Half-move counter:", half_move_counter, "\n"
      "Full-move counter:", full_move_counter)

# Make a move on the chessboard 
def make_move(move):
    global current_player, castling_rights, en_passant_square, half_move_counter, full_move_counter

    # Extract source and target squares from the move
    source_square = move[:2]
    target_square = move[2:]
    
    # Convert algebraic notation to numeric codes
    source_file = FILE_MAP[source_square[0]]
    source_rank = int(source_square[1])
    
    #first move has to be from a square that has a unit
    target_file = FILE_MAP[target_square[0]]
    target_rank = int(target_square[1])

    # Get the piece at the source square
    piece = board[8-source_rank][source_file]
    check_move_structure(current_player, move, piece)
    check_board(board, move, piece)

    # Move the piece to the target square
    board[8-target_rank][target_file] = piece
    board[8-source_rank][source_file] = EMPTY

    # Update game state variables

    # Switch current player
    current_player = "black" if current_player == "white" else "white"

    # Update castling rights, en passant square, half-move counter, and full-move counter
    half_move_counter += 1
    if half_move_counter % 2 == 0: 
        full_move_counter += 1 
    else: 
        full_move_counter = full_move_counter

    # ... (additional code for updating the game state)

# Test making a move
move = "f2f3"
make_move(move)
print_board(board)
print("After Move:", move, "\n"
      "Current player:", current_player, "\n"
      "Castling rights:", castling_rights, "\n"
      "En passant square:", en_passant_square, "\n"
      "Half-move counter:", half_move_counter, "\n"
      "Full-move counter:", full_move_counter)

move = "e7e5"
make_move(move)
print_board(board)
print("After Move:", move, "\n"
      "Current player:", current_player, "\n"
      "Castling rights:", castling_rights, "\n"
      "En passant square:", en_passant_square, "\n"
      "Half-move counter:", half_move_counter, "\n"
      "Full-move counter:", full_move_counter)

move = "g2g4"
make_move(move)
print_board(board)
print("After Move:", move, "\n"
      "Current player:", current_player, "\n"
      "Castling rights:", castling_rights, "\n"
      "En passant square:", en_passant_square, "\n"
      "Half-move counter:", half_move_counter, "\n"
      "Full-move counter:", full_move_counter)

move = "d8h4"
make_move(move)
print_board(board)
print("After Move:", move, "\n"
      "Current player:", current_player, "\n"
      "Castling rights:", castling_rights, "\n"
      "En passant square:", en_passant_square, "\n"
      "Half-move counter:", half_move_counter, "\n"
      "Full-move counter:", full_move_counter)
