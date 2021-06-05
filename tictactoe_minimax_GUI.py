import tkinter as tk
import tkinter.messagebox as messagebox
import numpy as np

h = 300
w = 300
human = 'X'
ai = 'O'
draw = 'D'

board = [[None for i in range(3)]for i in range(3)] #defining the board

root = tk.Tk()
root.title('Tic-Tac-Toe AI')

canvas = tk.Canvas(root, height= h, width =w, bg='white')
canvas.pack()

# Found a pattern and implemented it as it is much faster in python than loopinf through or hard coding

def DrawHumanTurn(row, col, canvas):
    x1, x2 = col, row
    x1 = x1*100
    x2 = x2*100
    x3 = col+1
    x4 = row+1
    x3 = x3*100
    x4 = x4*100

    x1_1, x2_2, x3_3, x4_4 = x3, x2, x1, x4
    line = canvas.create_line(x1, x2, x3, x4, fill='black', width=4)
    line = canvas.create_line(x1_1, x2_2, x3_3, x4_4, fill='black', width=4)

def DrawAITurn(row, col, canvas):
    c1, c2 = col, row
    c1 = c1*100
    c2 = c2*100
    c1 += 50
    c2 += 50
    circle = canvas.create_oval(c1-48, c2-48, c1+48, c2+48, fill='black')
    circle = canvas.create_oval(c1-44, c2-44, c1+44, c2+44, fill='white')
    
# draw the board on canvas

def DrawGrid(canvas):
    line = canvas.create_line(100, 0, 100, 300, fill='black')
    line = canvas.create_line(200, 0, 200, 300, fill='black')
    line = canvas.create_line(0, 100, 300, 100, fill='black')
    line = canvas.create_line(0, 200, 300, 200, fill='black')

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

def CheckWinner(board, player):  # to check if someone has won or not
    if board[0][0] == board[1][1] and board[0][0] == board[2][2] and board[0][0] == player: #Check maindiagonal
        return True 
    if board[0][2] == board[1][1] and board[0][2] == board[2][0] and board[0][2] == player: #Check counterdiagonal
        return True

    for i in range(len(board[0])):
        if board[i][0] == board[i][1] and board[i][0] == board[i][2] and board[i][0] == player: #Check row wise
            return True
        if board[0][i] == board[1][i] and board[0][i] == board[2][i] and board[0][i] == player: #Check column wise
            return True
def GameOver(player): #To show a gameover message and kill the tkinter window
    if player == ai:
        messagebox.showinfo("HAHA LOSER!","AI won")
        root.destroy()
    elif player == human:
        messagebox.showinfo('Congratulations :/','Human Won')
        root.destroy()
    elif player == draw:
        messagebox.showinfo('BOOORING!!','Draw')
        root.destroy()

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
    
    for position in GetEmptyCells(board):  #looping throuh all possible valid moves of the board at a certain position
        row, col = position[0], position[1]
        board[row][col] = ai if minimizing else human #changing board after deciding a valid move
        score = minimax(board, depth - 1, not minimizing) #resursivly calling minimax on the end node
        board[row][col] = None #changing back to previous state
        score[0], score[1] = row, col 

        if minimizing:
            if score[2] < optimal[2]: #checking the minimum score for ai
                optimal = score
        else:
            if score[2] > optimal[2]:  #checking maximum score for human
                optimal = score
    return optimal 

#utility functions

def AITurn(board):
    depth = len(GetEmptyCells(board)) 
    if depth == 9: 
        row = np.random.randint(0, 1, 2)
        col = np.random.randint(0, 1, 2)
    else:
        turn = minimax(board, depth, True)
        row = turn[0]
        col = turn[1]
    if ValidMove(board, row, col):
        board[row][col] = ai
        DrawAITurn(row, col, canvas)
        if CheckWinner(board, ai):
            GameOver(ai)
        if len(GetEmptyCells(board)) == 0:
            GameOver(draw)
    else: print("Wrong Move")

def PlayerTurn(board, cellIndex):
    row = cellIndex // 3
    col = cellIndex % 3
    if ValidMove(board, row, col):
        board[row][col] = human
        DrawHumanTurn(row, col, canvas)
        if CheckWinner(board, ai):
            GameOver(ai)
        if len(GetEmptyCells(board)) == 0:
            GameOver(draw)
    else: print("Wrong Move")
    AITurn(board)

# To convert corordinate values to an integer that corresponds to a cell in the board
def GetIntegerValue(corr):
    x, y = corr[0], corr[1]
    if x > 0 and x < 100 and y > 0 and y < 100:
        PlayerTurn(board, 0)
    elif x > 100 and x < 200 and y > 0 and y < 100:
        PlayerTurn(board, 1)
    elif x > 200 and x < 300 and y > 0 and y < 100:
        PlayerTurn(board, 2)
    elif x > 0 and x < 100 and y > 100 and y < 200:
        PlayerTurn(board, 3)
    elif x > 100 and x < 200 and y > 100 and y < 200:
        PlayerTurn(board, 4)
    elif x > 200 and x < 300 and y > 100 and y < 200:
        PlayerTurn(board, 5)
    elif x > 0 and x < 100 and y > 200 and y < 300:
        PlayerTurn(board, 6)
    elif x > 100 and x < 200 and y > 200 and y < 300:
        PlayerTurn(board, 7)
    elif x > 200 and x < 300 and y > 200 and y < 300:
        PlayerTurn(board, 8)

# To get the mouse click coordinate
def getxy(event):
        x, y = event.x, event.y
        return GetIntegerValue([x, y])

#main function
def main():
    x1, x2, x3, x4 = 0, 0, 300, 300
    canvas.create_rectangle(x1, x2, x3, x4, fill='white', tag='rectangle')
    DrawGrid(canvas)
    canvas.tag_bind('rectangle','<Button-1>', getxy)
    root.mainloop()
if __name__ == "__main__":
    main()