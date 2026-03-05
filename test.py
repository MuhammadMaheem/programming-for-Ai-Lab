# # class link:
# #     def __init__(self, head):
# #         self.head = head
# #         self.next =None
# #         self.prev = None

# #     @staticmethod
# #     def position(start, target):
# #         current = start
# #         index = 0
# #         while current is not None:
# #             if current.head == target:
# #                 return index 
# #             current = current.next
# #             index += 1

# #         return -1

# # node1 = link(10)
# # node2 = link(20)
# # node3 = link(30)


# # node1.next = node2
# # node2.next = node3

# # node2.prev = node1
# # node3.prev = node2

# # print(node1.prev)   
# # print(node1.head)
# # print(node1.next.head)


# # print(node2.prev.head)
# # print(node2.head)
# # print(node2.next.head)


# # pos  = link.position(node1 , 30)
# # print(pos)














# def is_balanced(s):
#     stack = []
#     mappings = {
#         ')': '(',
#         ']': '[', 
#         '}': '{'
#         }
#     for char in s:
#         if char in mappings.values():
#             stack.append(char)
#             print(stack)
#         elif char in mappings:
#             if not stack or stack.pop() != mappings[char]:
#                 return False
#     return not stack



# s = '(y{as}[aa)'

# x = is_balanced(s)
# print(x)













# class Node:
#     def __init__(self, data):
#         self.data = data    # The value (e.g., 10, "apple")
#         self.next = None    # Points to next node
#         self.prev = None    # Points to previous node
#     def print_forward(head):
#         current = head
#         while current:
#             print(current.data, end=" ⇄ ")
#             current = current.next
#         print("None")

#     # Usage:
#     def swap_values(head, val1, val2):
#         # Find both nodes
#         node1 = node2 = None
#         current = head

#         while current:
#             if current.data == val1:
#                 node1 = current
#             if current.data == val2:
#                 node2 = current
#             current = current.next

#         # If both found, swap their data
#         if node1 and node2:
#             node1.data, node2.data = node2.data, node1.data

# # Create nodes
# a = Node(10)
# b = Node(20)
# c = Node(30)

# # Link them forward
# a.next = b
# b.next = c

# # Link them backward
# b.prev = a
# c.prev = b

# # Now:
# # a ⇄ b ⇄ c
# # 10 ⇄ 20 ⇄ 30



# # Example:
# y = Node.print_forward(a)  # Now: 30 ⇄ 20 ⇄ 10 ⇄ None
# print(y)

# x = Node.swap_values(b, 20, 30)
# y = Node.print_forward(a)  # Now: 30 ⇄ 20 ⇄ 10 ⇄ None
# print(x)
# print(y)





















def solve_n_queens(n):
    # Create an NxN board filled with dots
    board = [['.' for _ in range(n)] for _ in range(n)]

    def is_safe(row, col):
        # Check if there is a queen in the same column
        for i in range(row):
            if board[i][col] == 'Q':
                return False
        
        # Check upper-left diagonal
        i, j = row, col
        while i >= 0 and j >= 0:
            if board[i][j] == 'Q':
                return False
            i -= 1
            j -= 1
            
        # Check upper-right diagonal
        i, j = row, col
        while i >= 0 and j < n:
            if board[i][j] == 'Q':
                return False
            i -= 1
            j += 1
            
        return True

    def solve(row):
        # If all queens are placed, we found a solution
        if row == n:
            return True
        
        # Try placing queen in each column of current row
        for col in range(n):
            if is_safe(row, col):
                board[row][col] = 'Q'
                
                # Recursively try to place the rest
                if solve(row + 1):
                    return True
                
                # If placing queen here doesn't lead to a solution, remove it (backtrack)
                board[row][col] = '.'
                
        return False

    # Start solving from the first row
    if solve(0):
        print(f"Solution for {n}-Queens:")
        for row in board:
            print(" ".join(row))
    else:
        print(f"No solution exists for {n}-Queens.")

# Dynamic Input
if __name__ == "__main__":
    try:
        user_input = input("Enter the number of queens (N): ")
        n = int(user_input)
        solve_n_queens(n)
    except ValueError:
        print("Please enter a valid integer.")
