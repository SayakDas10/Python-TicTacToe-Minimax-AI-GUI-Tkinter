import numpy as np

human = 'X'
ai = 'O'


# Possible valid moves and the depth is calculated from number of empty cells in the board
def GetEmptyCells(board):
    empty =[]
    for i in range(len(board[0])):
        for j in range(len(board[1])):
            if board[i][j] == None:
                empty.append([i, j])
    return empty

# To check if a move is a valid move, ie. if a move corresponds to an empty cell or not
def ValidMove(board, row, col):
    return True if [row, col] in GetEmptyCells(board) else False

def CheckWinner(board, player): # to check if someone has won or not
    if board[0][0] == board[1][1] and board[0][0] == board[2][2] and board[0][0] == player: #Check maindiagonal
        return True 
    if board[0][2] == board[1][1] and board[0][2] == board[2][0] and board[0][2] == player: #Check counterdiagonal
        return True

    for i in range(len(board[0])):
        if board[i][0] == board[i][1] and board[i][0] == board[i][2] and board[i][0] == player: #Check row wise
            return True
        if board[0][i] == board[1][i] and board[0][i] == board[2][i] and board[0][i] == player: #Check column wise
            return True
    
# static evaluation function, sets a score to the leaf node
def GetScore(board):
    if CheckWinner(board, ai):
        score = -1
    elif CheckWinner(board, human):
        score = +1
    else: score = 0
    return score

# THE ULTIMATE ALGOOOO
def minimax(board, depth, minimizing):
    if minimizing:
        optimal = [-1, -1, np.inf] # defining default temporary score for ai
    else: optimal = [-1, -1, -np.inf] # defining default temporary score for human
    if depth == 0 or CheckWinner(board, human) or CheckWinner(board, ai): #getting score of a leaf node or the node where a game ends
        score = GetScore(board)
        return [-1, -1, score]
    
    for position in GetEmptyCells(board): #looping throuh all possible valid moves of the board at a certain position
        row, col = position[0], position[1]
        board[row][col] = ai if minimizing else human #changing board after deciding a valid move
        score = minimax(board, depth - 1, not minimizing) #resursivly calling minimax on the end node
        board[row][col] = None #changing back to previous state
        score[0], score[1] = row, col 

        if minimizing:
            if score[2] < optimal[2]: #checking the minimum score for ai
                optimal = score
        else:
            if score[2] > optimal[2]: #checking maximum score for human
                optimal = score
    return optimal 
#utility functions
def DisplayBoard(board):
    print('\n')
    for i in range(len(board[0])):
        print(board[i],'\n')


def PlayerTurn(board):
    index = int(input('Player Turn: ')) - 1
    row = index // 3
    col = index % 3
    if ValidMove(board, row, col):
        board[row][col] = human
    else: print("Wrong Move")
    return board

def AITurn(board):
    depth = len(GetEmptyCells(board)) #depth of the tree is the length of empty cell set
    if depth == 9: #if the ai goes first, it chooses a random cell from the board
        row = np.random.randint(0, 1, 2)
        col = np.random.randint(0, 1, 2)
    else:
        turn = minimax(board, depth, True) #getting the best turn for ai
        row = turn[0]
        col = turn[1]
    if ValidMove(board, row, col):
        print("Ai Turn: ")
        board[row][col] = ai
    else: print("Wrong Move")
    return board

#main function
def main():
    board = [[None for i in range(3)]for i in range(3)]
    while True:
        PlayerTurn(board)
        DisplayBoard(board)
        if CheckWinner(board, human):
            print(human," Won")
            break
        if len(GetEmptyCells(board)) == 0:
            print("Tie Game.")
            break
        AITurn(board)
        DisplayBoard(board)
        if CheckWinner(board, ai):
            print(ai," Won")
            break

if __name__ == "__main__":
    main()