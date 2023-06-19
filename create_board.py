# Define the square representation using numeric codes
class game:
    def __init__(self, winner, check_status):
        self.winner = None
        self.check_status = None
    
    def announce_winner(self):
        print("winner is %s" % self.winner)
            
def main():
    game = game(starting_board)

def game_setup():
    global SQUARES, FILE_MAP, EMPTY, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING
    SQUARES = {
    'a1': 1,  'b1': 2,  'c1': 3,  'd1': 4,  'e1': 5,  'f1': 6,  'g1': 7,  'h1': 8,
    'a2': 9,  'b2': 10, 'c2': 11, 'd2': 12, 'e2': 13, 'f2': 14, 'g2': 15, 'h2': 16,
    'a3': 17, 'b3': 18, 'c3': 19, 'd3': 20, 'e3': 21, 'f3': 22, 'g3': 23, 'h3': 24,
    'a4': 25, 'b4': 26, 'c4': 27, 'd4': 28, 'e4': 29, 'f4': 30, 'g4': 31, 'h4': 32,
    'a5': 33, 'b5': 34, 'c5': 35, 'd5': 36, 'e5': 37, 'f5': 38, 'g5': 39, 'h5': 40,
    'a6': 41, 'b6': 42, 'c6': 43, 'd6': 44, 'e6': 45, 'f6': 46, 'g6': 47, 'h6': 48,
    'a7': 49, 'b7': 50, 'c7': 51, 'd7': 52, 'e7': 53, 'f7': 54, 'g7': 55, 'h7': 56,
    'a8': 57, 'b8': 58, 'c8': 59, 'd8': 60, 'e8': 61, 'f8': 62, 'g8': 63, 'h8': 64
    }
    
    FILE_MAP = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
    # Accessing the numeric code for a square
    #square = 'e4'
    #numeric_code = SQUARES[square]
    #print(numeric_code)  # Output: 28

    # Reverse lookup - Getting the algebraic notation for a numeric code
    #numeric_code = 34
    #algebraic_notation = next(key for key, value in SQUARES.items() if value == numeric_code)
    #print(algebraic_notation)  # Output: 'c5'
    
    # Define the piece representation using numeric codes
    EMPTY = 0
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6
    
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
        [ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK],
        [PAWN, PAWN, PAWN, PAWN, PAWN, PAWN, PAWN, PAWN],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [PAWN, PAWN, PAWN, PAWN, PAWN, PAWN, PAWN, PAWN],
        [ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK],
    ]
    return starting_board, current_player, castling_rights, en_passant_square, half_move_counter, full_move_counter

def print_board(board):
    for rank in range(8):
        for file in range(8):
            piece = board[rank][file]
            print(piece, end=" ")
        print()

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

# Define variables to track the game state
# white always starts the game

# Define rule checks for movements
def check_move(color, move, piece):
    if "x" in move:
        source_square = move.replace("x", "")[:2]
        target_square = move.replace("x", "")[2:]
    elif "+" in move:
        source_square = move.replace("+", "")[:2]
        target_square = move.replace("+", "")[2:]
    elif "#" in move:
        source_square = move.replace("#", "")[:2]
        target_square = move.replace("#", "")[2:]
    elif "=" in move:
        source_square = move.replace("=", "")[:2]
        target_square = move.replace("=", "")[2:]
    else:
        source_square = move[:2]
        target_square = move[2:]
        
    # Convert algebraic notation to numeric codes
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
        elif color == "white":
            if target_rank == 4 and source_rank == 2:
                result = True
            elif target_rank == source_rank + 1:
                result = True
            else:
                result = False
        elif color == "black":
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

def check_board(board, move, piece):
    return True

# Make a move on the chessboard 
def make_move(move):
    global current_player, castling_rights, en_passant_square, half_move_counter, full_move_counter
    if "#" in move:
        print("Checkmate!")
    elif "+" in move:
        print("Check!")

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
    check_move(current_player, move, piece)
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

move = "d8h4#"
make_move(move)
print_board(board)
print("After Move:", move, "\n"
      "Current player:", current_player, "\n"
      "Castling rights:", castling_rights, "\n"
      "En passant square:", en_passant_square, "\n"
      "Half-move counter:", half_move_counter, "\n"
      "Full-move counter:", full_move_counterwwww)
