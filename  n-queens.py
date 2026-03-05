import numpy as np
board = np.zeros((4, 4))

def q_range(row):
    queen_range = ([row-1,row,row+1],[0,1,2])
    print(queen_range)
for row in range(4):
    for col in range(4):
        board[row][col] = 1
        if 1 in board[row]:
            print("tre") 
            break
        
    # print(board)








q_range(1)