def hollow_square(n):
    result = []
    for i in range(n):
        row = ""
        for j in range(n):
            if i == 0 or i == n - 1 or j == 0 or j == n - 1:
                row += "* "
            else:
                row += "  "
        result.append(row)
    return "\n".join(result)





def hollow_square_with_line(n):
    if n < 1:
        return ""
    result = []
    for i in range(n):
        row = ""
        for j in range(n):
            if i == 0 or i == n - 1 or j == 0 or j == n - 1 or i == j:
                row += "* "
            else:
                row += "  "
        result.append(row)
    return "\n".join(result)





def hollow_square_with_two_diagonal_lines(n):
    if n < 1:
        return ""
    result = []
    for i in range(n):
        row = ""
        for j in range(n):
            if i == 0 or i == n - 1 or j == 0 or j == n - 1 or i == j or i + j == n - 1:
                row += "* "
            else:
                row += "  "
        result.append(row)
    return "\n".join(result)
               


def hollow_square_with_diagonal_lines(n):
    if n < 3:
        for _ in range(n):
            print("* " * n)
        return
    if n % 2 == 0:
        n -= 1  
    mid = n // 2

    for i in range(n):
        for j in range(n):
   
            if i == 0 or i == n - 1 or j == 0 or j == n - 1:
                print("*", end=" ")
     
            elif i == mid and j <= mid:
                print("*", end=" ")
          
            elif i >= mid and j == i:               
                print("*", end=" ")
            elif i <= mid and j == 2 * mid - i:     
                print("*", end=" ")
            else:
                print(" ", end=" ")
        print()


def hollow_square_center_block(n):
    if n < 2:
        result = []
        for _ in range(n):
            result.append("* " * n)
        return "\n".join(result)

    mid = n // 2
    result = []
    for i in range(n):
        row = ""
        for j in range(n):
            if i == 0 or i == n - 1 or j == 0 or j == n - 1:
                row += "* "
            elif (i == 1 or i == n - 2) and j == n - 2:
                row += "* "
            elif (
                (n % 2 == 1 and i == mid) or
                (n % 2 == 0 and (i == mid - 1 or i == mid))
            ) and j <= n - 3:
                row += "* "
            else:
                row += "  "
        result.append(row)
    return "\n".join(result)



listing = {
    "hollow_square": hollow_square,
    "hollow_square_with_line": hollow_square_with_line,
    "hollow_square_with_diagonal_lines": hollow_square_with_diagonal_lines,
    "hollow_square_with_two_diagonal_lines": hollow_square_with_two_diagonal_lines,
}

def grinding():
    patterns = {}
    for key, func in listing.items():
        patterns[key] = func(9)
    
    keys = list(patterns.keys())
    for i in range(0, len(keys), 2):
        pat1 = patterns[keys[i]]
        pat2 = patterns[keys[i+1]] if i+1 < len(keys) else " "
        lines1 = pat1.split('\n')
        lines2 = pat2.split('\n') if pat2 else [' '] * len(lines1)
        for j in range(len(lines1)):
            print(lines1[j] + "  " + lines2[j])
        print("\n")

grinding()
