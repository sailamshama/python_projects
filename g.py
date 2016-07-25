def is_empty(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != " ":
                return False
    return True    
    
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    '''assuming the sequence is filled.. we only check for end points
    returns whether a sequence is open or semi-open
'''
    adj_y_start = y_end - (length)*d_y 
    adj_x_start = x_end - (length)*d_x

    adj_y_end = y_end + d_y 
    adj_x_end = x_end + d_x
    
    end_points = [adj_y_start, adj_x_start, adj_y_end, adj_x_end]
    
    y_start_out_of_bound = adj_y_start >= 8 or adj_y_start < 0
    x_start_out_of_bound = adj_x_start >= 8 or adj_x_start < 0
    y_end_out_of_bound = adj_y_end >= 8 or adj_y_end <0
    x_end_out_of_bound = adj_x_end >= 8 or adj_x_end < 0
    
    #FOR SEQUENCES NEAR BORDER

    #if both end points are out of bound:
    if ((y_start_out_of_bound) or (x_start_out_of_bound)) and\
       ((y_end_out_of_bound or x_end_out_of_bound)):
        return "CLOSED"
    
    #if only one end is out of bound: 
    #if start end is closed
    elif ((y_start_out_of_bound) or (x_start_out_of_bound)):
        #check if the other is closed by other color
        if board[adj_y_end][adj_x_end] != " ":
            return "CLOSED"
        return "SEMIOPEN"
    #if end end is closed
    elif ((y_end_out_of_bound) or (x_end_out_of_bound)):
        #check if the other is closed by other color
        if board[adj_y_start][adj_x_start] != " ":
            return "CLOSED"
        return "SEMIOPEN"
    
    
    #FOR SEQUENCES BOUND BY OTHER COLORS

    #if sequence is open
    if board[adj_y_start][adj_x_start] == " " and\
       board[adj_y_end][adj_x_end] == " ":
        return "OPEN"
    #if sequence is closed
    elif board[adj_y_start][adj_x_start] != " " and\
       board[adj_y_end][adj_x_end] != " ":
        return "CLOSED"
    #if sequence is semiopen
    else: return "SEMIOPEN"
    
def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count = 0
    semi_open_seq_count = 0
    
    #sequence_tracker tracks sequence of desired color
    sequence_tracker = 0

    #start iterating at start location
    y = y_start
    x = x_start

    #setting stop conditions
    y_out_of_bound = (y<0 or y>=len(board))
    x_out_of_bound = (x<0 or x>=len(board))

    #as long as you're within the board
    while not(y_out_of_bound or x_out_of_bound):
        #as long as you haven't hit another color
        while board[y][x] == col:
            #increment your sequence length
            sequence_tracker += 1
            y += d_y
            x += d_x
            y_out_of_bound = (y<0 or y>=len(board))
            x_out_of_bound = (x<0 or x>=len(board))
            if y_out_of_bound or x_out_of_bound:
                break
        #if you've hit another color, analyze the length of the sequence \
        #    obtained
        #if it's greater than or less than required length, ignore
        if sequence_tracker != length:
            open_seq_count += 0
            semi_open_seq_count += 0
        else:
            #if it is of the desired length, check how it's bounded
            #note, it's end position is one less than the last values of y \
            #and x
            if is_bounded(board, y-d_y, x-d_x, length, d_y, d_x) == "OPEN":
                open_seq_count += 1
            if is_bounded(board, y-d_y, x-d_x, length, d_y, d_x) == "SEMIOPEN":
                semi_open_seq_count += 1
        y += d_y
        x += d_x
        #reset sequence tracker/ length counter
        sequence_tracker = 0
        #reset tracker that checks if its out of bound
        y_out_of_bound = (y<0 or y>=len(board))
        x_out_of_bound = (x<0 or x>=len(board))
        if y_out_of_bound or x_out_of_bound:
            break
    
    return open_seq_count, semi_open_seq_count
    
def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    #for all horizontal rows
    for y in range(len(board)):
        counts = detect_row(board, col, y,0, length, 0,1)
        open_seq_count += counts[0]
        semi_open_seq_count += counts[1]

    #for all vertical rows:
    for x in range(len(board[0])):
        counts = detect_row(board, col, 0,x, length, 1,0)
        open_seq_count += counts[0]
        semi_open_seq_count += counts[1]

    #all backward_slash diagonals
    x_start = 0
    for y_start in range(len(board)):
        counts = detect_row(board, col, y_start, x_start, length, 1,1)
        open_seq_count += counts[0]
        semi_open_seq_count += counts[1]
    y_start = 0
    for x_start in range(1, len(board)):
        counts = detect_row(board, col, y_start, x_start, length, 1,1)
        open_seq_count += counts[0]
        semi_open_seq_count += counts[1]

    #for forward_slash diagonals
    y_start = 0
    for x_start in range(len(board)):
        counts = detect_row(board, col, y_start, x_start, length, 1,-1)
        open_seq_count += counts[0]
        semi_open_seq_count += counts[1] 
    for y_start in range(1, len(board)):
        #x_start is 7 as ended by last for loop
        counts = detect_row(board, col, y_start, x_start,length, 1, -1)
        open_seq_count += counts[0]
        semi_open_seq_count += counts[1]

    return open_seq_count, semi_open_seq_count
    
def search_max(board):
    scores_position = {}
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] == " ":
                temp = board[y][x]
                board[y][x] ="b"
                gain = score(board)
                scores_position[gain] = (y,x)
                board[y][x] = temp
    return scores_position[max(scores_position.keys())]
    
def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def horizontal_win(board, col):
    for y in board:
        row_string = ''.join(y)
        if col*5 in row_string:
            return True
    return False

def vertical_win(board,col):
    row_string = ""
    for x in range(len(board)):
        for y in range(len(board)):
            row_string += board[y][x]
        if col*5 in row_string:
            return True
        row_string = ""
    return False

def backward_diagonal_win(board,col):
    winning_sequence = col*5
    d_y = 1
    d_x = 1
    row_string = ""
    x=0

    #check all diagonal rows starting from left end of board
    for y in range(4):
        for i in range(len(board)-y):
            row_string += board[y][x]
            y+=d_y
            x+=d_x
        x =0
        if winning_sequence in row_string:
            return True
    #check all diagonal rows starting from top of board
    row_string = ""
    y =0
    for x in range(1,4):
        for i in range(len(board)-x):
            row_string += board[y][x]
            y += d_y
            x += d_x
        y = 0
        if winning_sequence in row_string:
            return True
    return False

def forward_diagonal_win(board,col):
    '''
    checks diagonals
    (0,7)-(7,0)
    (1,7)-(7,1)
    (2,7)-(7,2)
    (3,7)-(7,3)

    (0,6)-(0,5)
    (0,5)-(5,0)
    (0,4)-(4,0)
    '''
    winning_sequence = col*5
    d_y = 1
    d_x = -1
    row_string = ""
    x = 7

    #check all diagonals starting from right end of the board
    for y in range(4):
        for i in range(len(board)-y):
            row_string += board[y][x]
            y += d_y
            x += d_x
        x = 7
        if winning_sequence in row_string:
            return True
        row_string = ""
    #check all diagonals starting for top of board
    y = 0
    row_string = ""
    for x in range(6, 3, -1):
        for i in range(x+1):
            row_string += board[y][x]
            y += d_y
            x += d_x
        y = 0
        if winning_sequence in row_string:
            return True
    return False

def win(board, col):
    if vertical_win(board,col) or horizontal_win(board, col) or \
       backward_diagonal_win(board,col) or forward_diagonal_win(board,col):
        return True
    return False

def is_win(board):
    black_won = win(board, "b")
    white_won = win(board, "w")
    
    if black_won and white_won:
        return "Draw"
    elif black_won:
        return "Black won"
    elif white_won:
        return "White won"
    else:
        return "Continue playing" 


def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)
    

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board
                


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))
        
    
    

        
    
def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
     
        
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
        
            
            
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    
    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    
    y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #     
    
    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);
    
    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #        
    #        
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0


  
            
if __name__ == '__main__':
    easy_testset_for_main_functions()
    some_tests()
