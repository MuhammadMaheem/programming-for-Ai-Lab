# grid = [
#     [1, 2, 3],
#     [4, 5, 6],
#     [7, 8, 9]
# ]


# main_diag = [grid[i][i] for i in range(len(grid))]
# print("Main diagonal:", main_diag)  # Output: [1, 5, 9]

# n = len(grid)
# anti_diag = [grid[i][n - 1 - i] for i in range(n)]






def get_diagonals_from_position(grid, r, c):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Main diagonal (top-left to bottom-right): i - j == r - c
    main_diag = []
    for i in range(rows):
        j = i - (r - c)
        if 0 <= j < cols:
            main_diag.append(grid[i][j])

    anti_diag = []
    for i in range(rows):
        j = (r + c) - i
        if 0 <= j < cols:
            anti_diag.append(grid[i][j])

    return main_diag, anti_diag


grid = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9,10,11,12]
]

r, c = 1,1  # Value is 7
main, anti = get_diagonals_from_position(grid, r, c)

print("Main diagonal (↘↖):", main)   # [3, 6, 9] → Wait, let's verify!
print("Anti-diagonal (↗↙):", anti)  # [5, 8] or [8, 5]? Let's fix logic.