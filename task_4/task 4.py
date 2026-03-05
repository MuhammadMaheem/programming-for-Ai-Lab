# N-Queens Problem Solver

def is_safe(board, row, col, n):
    for i in range(row):
        if board[i] == col:
            return False

    for i in range(row):
        if board[i] - i == col - row:
            return False

    for i in range(row):
        if board[i] + i == col + row:
            return False

    return True

def solve_n_queens(board, row, n, solutions):
    if row == n:
        solutions.append(board[:])
        return

    for col in range(n):
        if is_safe(board, row, col, n):
            board[row] = col
            solve_n_queens(board, row + 1, n, solutions)
            board[row] = -1  # backtrack

def print_board(board, n):
    for i in range(n):
        row_str = ""
        for j in range(n):
            if board[i] == j:
                row_str += "Q "
            else:
                row_str += ". "
        print(row_str)
    print()

# Main part
n = 8  
board = [-1] * n 
solutions = []

solve_n_queens(board, 0, n, solutions)

print(f"Total solutions for {n}-Queens: {len(solutions)}")
if solutions:
    print("One possible solution:")
    print_board(solutions[0], n)