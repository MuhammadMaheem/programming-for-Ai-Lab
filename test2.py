# import numpy as np

# # # # ============================================
# # # # STEP 1: CREATE THE WORLD
# # # # ============================================
# # # grid_size = 5

# # # # Agent starts at top-left
# # # agent_pos = np.array([0, 0])  # [row, col]

# # # # Goal is at bottom-right  
# # # goal_pos = np.array([4, 4])

# # # print("=== THE WORLD ===")
# # # print(f"Agent position: {agent_pos}")
# # # print(f"Goal position: {goal_pos}")
# # # print()

# # # # ============================================
# # # # STEP 2: DEFINE POSSIBLE ACTIONS
# # # # ============================================
# # # # We'll use 0=up, 1=down, 2=left, 3=right
# # # actions = {
# # #     0: np.array([-1, 0]),  # up (decrease row)
# # #     1: np.array([1, 0]),   # down (increase row)
# # #     2: np.array([0, -1]),  # left (decrease col)
# # #     3: np.array([0, 1])    # right (increase col)
# # # }

# # # print("=== ACTIONS ===")
# # # for action_num, move in actions.items():
# # #     print(f"Action {action_num}: move by {move}")
# # # print()

# # # # ============================================
# # # # STEP 3: TRY MOVING THE AGENT
# # # # ============================================
# # # print("=== LET'S MOVE! ===")

# # # # Let's try moving right
# # # chosen_action = 3  # right
# # # new_pos = agent_pos + actions[chosen_action]

# # # print(f"Agent was at: {agent_pos}")
# # # print(f"We chose action {chosen_action} (right)")
# # # print()

# # # # ============================================
# # # # YOUR TURN TO CODE!
# # # # ============================================
# # # # TODO 1: Try changing chosen_action to 1 (down)
# # # #         What happens to new_pos?
# # # def reach_goal(current_pos , goal_pos):
# # #     if current_pos[0] and current_pos[1] == goal_pos[0] and goal_pos[1]:
# # #         print("yes")
# # #     else:
# # #         print("no")
# # # # TODO 2: What if agent tries to move UP when already at [0,0]?
# # # #         It would go to [-1, 0] which is OUTSIDE the grid!
# # # #         Can you write a simple check to prevent this?
# # # #         Hint: use np.clip() or if statements
# # # if new_pos[0] < 0 or new_pos[1] < 0:
# # #     new_pos = agent_pos
# # #     print("Agent Cant go outside the boundary")
# # #     print(f"Agent moves to: {new_pos}")

# # # else:
# # #     print(f"Agent moves to: {new_pos}")
# # #     print("true")

# # # # TODO 3: Write a function that checks if agent reached the goal
# # # #         def reached_goal(agent_pos, goal_pos):
# # # #             # Your code here
# # # #             pass


# # # reach_goal(agent_pos,goal_pos)
# # # print("=" * 40)
# # # print("🎯 YOUR CHALLENGES:")
# # # print("1. Change the action and see what happens")
# # # print("2. Add boundary checking (keep agent in grid)")  
# # # print("3. Write reached_goal() function")
# # # print("=" * 40)


















# # import numpy as np

# # # ============================================
# # # STEP 1: CREATE THE WORLD
# # # ============================================
# # grid_size = 5

# # # Agent starts at top-left
# # agent_pos = np.array([0, 0])  # [row, col]

# # # Goal is at bottom-right  
# # goal_pos = np.array([4, 4])

# # print("=== THE WORLD ===")
# # print(f"Agent position: {agent_pos}")
# # print(f"Goal position: {goal_pos}")
# # print()

# # # ============================================
# # # STEP 2: DEFINE POSSIBLE ACTIONS
# # # ============================================
# # actions = {
# #     0: np.array([-1, 0]),  # up
# #     1: np.array([1, 0]),   # down
# #     2: np.array([0, -1]),  # left
# #     3: np.array([0, 1])    # right
# # }

# # # ============================================
# # # STEP 3: HELPER FUNCTIONS
# # # ============================================

# # def is_valid_pos(pos, grid_size):
# #     """Check if position is inside the grid"""
# #     return 0 <= pos[0] < grid_size and 0 <= pos[1] < grid_size

# # def reached_goal(agent_pos, goal_pos):
# #     """Check if agent reached the goal"""
# #     # Fixed version using np.array_equal
# #     return np.array_equal(agent_pos, goal_pos)

# # def move_agent(current_pos, action, grid_size):
# #     """Move agent and return new position (with boundary check)"""
# #     new_pos = current_pos + actions[action]
    
# #     # Keep agent inside grid using np.clip
# #     new_pos = np.clip(new_pos, 0, grid_size - 1)
    
# #     return new_pos

# # # ============================================
# # # STEP 4: THE REWARD SYSTEM ⭐⭐⭐
# # # ============================================

# # def get_reward(agent_pos, goal_pos):
# #     """
# #     This is THE KEY to reinforcement learning!
# #     We tell the agent what's good and what's bad.
# #     """
# #     if reached_goal(agent_pos, goal_pos):
# #         return 100  # BIG reward for reaching goal! 🎉
# #     else:
# #         return -1   # Small penalty for each step (encourages shorter paths)

# # # ============================================
# # # STEP 5: LET'S SIMULATE A FEW MOVES!
# # # ============================================

# # print("\n" + "="*50)
# # print("🎮 SIMULATING AGENT MOVES")
# # print("="*50)

# # # Reset agent
# # agent_pos = np.array([0, 0])
# # total_reward = 0

# # # Simulate a path: right, right, down, down, right, right, down, down
# # moves = [3, 3, 1, 1, 3, 3, 1, 1]  # This should reach the goal!

# # for step, action in enumerate(moves, 1):
# #     # Move the agent
# #     agent_pos = move_agent(agent_pos, action, grid_size)
    
# #     # Get reward for this position
# #     reward = get_reward(agent_pos, goal_pos)
# #     total_reward += reward
    
# #     # Print what happened
# #     action_names = {0: "UP", 1: "DOWN", 2: "LEFT", 3: "RIGHT"}
# #     print(f"Step {step}: Move {action_names[action]} → Position {agent_pos} → Reward: {reward:+4d}")
    
# #     # Check if reached goal
# #     if reached_goal(agent_pos, goal_pos):
# #         print(f"\n🎉 GOAL REACHED! Total Reward: {total_reward}")
# #         break

# # # ============================================
# # # 🎯 YOUR NEW CHALLENGES!
# # # ============================================
# # print("\n" + "="*50)
# # print("🎯 NOW IT'S YOUR TURN:")
# # print("="*50)
# # print("1. Try changing the 'moves' list above")
# # print("   - Can you find a SHORTER path to the goal?")
# # print("   - What if you go the WRONG way first?")
# # print()
# # print("2. THINK: Why do we give -1 for each step?")
# # print("   - What if we gave 0 instead?")
# # print("   - What if we gave -10 instead?")
# # print()
# # print("3. EXPERIMENT: Change the reward values in get_reward()")
# # print("   - What happens if goal reward = 10 instead of 100?")
# # print("   - What happens if step penalty = -10 instead of -1?")
# # print()
# # print("4. NEXT CONCEPT: Right now WE chose the moves.")
# # print("   But in RL, the AGENT chooses randomly at first!")
# # print("   How could we make it choose random actions?")
# # print("="*50)







# # Shape: (5, 5, 4) 
# # q_table[row][col][action] = value
# q_table = np.zeros((5, 5, 4))
# print(q_table)


# print(q_table[3,4,2])






import numpy as np

# ============================================
# SETUP: WORLD AND ACTIONS
# ============================================
grid_size = 5
agent_pos = np.array([0, 0])
goal_pos = np.array([4, 4])

actions = {
    0: np.array([-1, 0]),  # up
    1: np.array([1, 0]),   # down
    2: np.array([0, -1]),  # left
    3: np.array([0, 1])    # right
}

def move_agent(pos, action, grid_size):
    new_pos = pos + actions[action]
    return np.clip(new_pos, 0, grid_size - 1)

def get_reward(pos, goal):
    return 100 if np.array_equal(pos, goal) else -1

# ============================================
# METHOD 1: NUMPY ARRAY Q-TABLE
# ============================================
print("="*60)
print("METHOD 1: NUMPY ARRAY Q-TABLE")
print("="*60)

# Create Q-table: shape (rows, cols, actions)
q_table_numpy = np.zeros((grid_size, grid_size, 4))

print(f"Q-table shape: {q_table_numpy.shape}")
print(f"Total values stored: {q_table_numpy.size}")
print()

# Let's say we learn that at position [0,0], action 3 (right) is good
q_table_numpy[0, 0, 3] = 50.0

print("After learning: at [0,0], action RIGHT (3) is worth 50")
print(f"Value at [0,0] for action 3: {q_table_numpy[0, 0, 3]}")
print()

# Get the BEST action at a position
position = [0, 0]
best_action_numpy = np.argmax(q_table_numpy[position[0], position[1], :])
best_value_numpy = np.max(q_table_numpy[position[0], position[1], :])

print(f"Best action at {position}: {best_action_numpy} (value: {best_value_numpy})")
print()

# ============================================
# METHOD 2: DICTIONARY Q-TABLE
# ============================================
print("="*60)
print("METHOD 2: DICTIONARY Q-TABLE")
print("="*60)

# Create empty dictionary
q_table_dict = {}

print(f"Initial dictionary size: {len(q_table_dict)} entries")
print()

# Store a value: use string key "row,col,action"
key = "0,0,3"
q_table_dict[key] = 50.0

print("After learning: at [0,0], action RIGHT (3) is worth 50")
print(f"Value at key '{key}': {q_table_dict[key]}")
print(f"Dictionary now has {len(q_table_dict)} entries")
print()

# Get the BEST action at a position using dictionary
def get_best_action_dict(q_table, pos):
    """Find best action at position using dictionary"""
    best_action = 0
    best_value = -float('inf')
    
    for action in range(4):
        key = f"{pos[0]},{pos[1]},{action}"
        value = q_table.get(key, 0.0)  # Default to 0 if not in dict
        
        if value > best_value:
            best_value = value
            best_action = action
    
    return best_action, best_value

position = [0, 0]
best_action_dict, best_value_dict = get_best_action_dict(q_table_dict, position)
print(f"Best action at {position}: {best_action_dict} (value: {best_value_dict})")
print()

# ============================================
# COMPARISON
# ============================================
print("="*60)
print("📊 COMPARISON")
print("="*60)
print(f"NumPy - Memory used: {q_table_numpy.size} values (even if zeros)")
print(f"Dict  - Memory used: {len(q_table_dict)} values (only non-zero)")
print()
print("NumPy - Access: q_table[0, 0, 3]  ← Simple indexing")
print("Dict  - Access: q_table['0,0,3']  ← Need string key")
print()

# ============================================
# 🎯 YOUR PRACTICE EXERCISES!
# ============================================
print("="*60)
print("🎯 YOUR TURN TO PRACTICE!")
print("="*60)
print()

print("EXERCISE 1 (EASY): NumPy Array")
print("-" * 40)
print("TODO: Add these learned values to q_table_numpy:")
print("  - At [1,1], action DOWN (1) = 30")
print("  - At [2,2], action RIGHT (3) = 70")
print()
print("# Your code here:")
print("# q_table_numpy[?, ?, ?] = ?")
print()

print("EXERCISE 2 (EASY): Dictionary")
print("-" * 40)
print("TODO: Add the same values to q_table_dict:")
print("  - At [1,1], action DOWN (1) = 30")
print("  - At [2,2], action RIGHT (3) = 70")
print()
print("# Your code here:")
print("# q_table_dict['?,?,?'] = ?")
print()

print("EXERCISE 3 (MEDIUM): Retrieval")
print("-" * 40)
print("TODO: Get the value for action UP (0) at position [1,1]")
print("  - From NumPy: value_np = q_table_numpy[?, ?, ?]")
print("  - From Dict: value_dict = q_table_dict.get('?,?,?', 0.0)")
print()

print("EXERCISE 4 (CHALLENGE): Which is better?")
print("-" * 40)
print("Run this code and answer:")
print()
print("# Time test (uncomment to run):")
print("# import time")
print("#")
print("# # Test NumPy speed")
print("# start = time.time()")
print("# for _ in range(100000):")
print("#     val = q_table_numpy[2, 3, 1]")
print("# numpy_time = time.time() - start")
print("#")
print("# # Test Dict speed")  
print("# start = time.time()")
print("# for _ in range(100000):")
print("#     val = q_table_dict.get('2,3,1', 0.0)")
print("# dict_time = time.time() - start")
print("#")
print("# print(f'NumPy time: {numpy_time:.4f}s')")
print("# print(f'Dict time: {dict_time:.4f}s')")
print()

print("="*60)
print("💡 REFLECTION QUESTIONS:")
print("="*60)
print("1. Which method feels more natural to you?")
print("2. For a 5x5 grid, which uses less memory?")
print("3. What if we had a 1000x1000 grid but only visited 100 cells?")
print("4. Which would you choose for our RL agent and why?")
print("="*60)




import time

# Test NumPy speed
start = time.time()
for _ in range(100000):
    val = q_table_numpy[2, 3, 1]
numpy_time = time.time() - start

# Test Dict speed  
start = time.time()
for _ in range(100000):
    val = q_table_dict.get('2,3,1', 0.0)
dict_time = time.time() - start

print(f'NumPy time: {numpy_time:.4f}s')
print(f'Dict time: {dict_time:.4f}s')