"""
Q-LEARNING FROM SCRATCH
A super simple implementation for beginners!

Goal: Teach an agent to navigate a 5x5 grid to reach the goal
"""

import numpy as np
import random

# ============================================
# STEP 1: SETUP THE WORLD
# ============================================

# Size of our grid (5x5 means 25 positions)
GRID_SIZE = 5

# Starting position (top-left corner)
START_POS = [0, 0]

# Goal position (bottom-right corner)
GOAL_POS = [4, 4]

# ============================================
# STEP 2: DEFINE ACTIONS
# ============================================

# The agent can do 4 things:
# 0 = Move UP (decrease row)
# 1 = Move DOWN (increase row)
# 2 = Move LEFT (decrease column)
# 3 = Move RIGHT (increase column)

def move_agent(position, action):
    """
    Move the agent based on action.
    Returns new position after moving.
    """
    # Make a copy so we don't change the original
    new_pos = position.copy()
    
    if action == 0:  # UP
        new_pos[0] = max(0, position[0] - 1)  # Don't go above row 0
    elif action == 1:  # DOWN
        new_pos[0] = min(GRID_SIZE - 1, position[0] + 1)  # Don't go below last row
    elif action == 2:  # LEFT
        new_pos[1] = max(0, position[1] - 1)  # Don't go left of column 0
    elif action == 3:  # RIGHT
        new_pos[1] = min(GRID_SIZE - 1, position[1] + 1)  # Don't go right of last column
    
    return new_pos

# ============================================
# STEP 3: DEFINE REWARDS
# ============================================

def get_reward(position):
    """
    Tell the agent if it did something good or bad.
    
    Returns:
        +100 if reached goal (GREAT JOB!)
        -1 for each step (encourages finding shortest path)
    """
    if position[0] == GOAL_POS[0] and position[1] == GOAL_POS[1]:
        return 100  # Big reward for reaching goal!
    else:
        return -1   # Small penalty for each step

# ============================================
# STEP 4: Q-TABLE FUNCTIONS
# ============================================

# This is where the agent stores what it learned!
# Key format: "row,col,action" → Value: how good that action is
q_table = {}

def get_q_value(position, action):
    """
    Look up Q-value for a state-action pair.
    If we haven't seen it before, return 0 (neutral guess).
    """
    key = f"{position[0]},{position[1]},{action}"
    return q_table.get(key, 0.0)  # Default to 0 if not in table

def set_q_value(position, action, value):
    """
    Store a Q-value in the table.
    """
    key = f"{position[0]},{position[1]},{action}"
    q_table[key] = value

def get_best_action(position):
    """
    Find which action has the highest Q-value at this position.
    This is the action the agent thinks is best!
    """
    best_action = 0
    best_value = get_q_value(position, 0)
    
    # Check all 4 actions
    for action in range(4):
        value = get_q_value(position, action)
        if value > best_value:
            best_value = value
            best_action = action
    
    return best_action

# ============================================
# STEP 5: EXPLORATION VS EXPLOITATION
# ============================================

def choose_action(position, epsilon):
    """
    Decide which action to take.
    
    epsilon = exploration rate
    - High epsilon (like 0.9): Try random actions (explore)
    - Low epsilon (like 0.1): Use best known action (exploit)
    
    This is called "epsilon-greedy" strategy
    """
    if random.random() < epsilon:
        # EXPLORE: Try a random action
        return random.randint(0, 3)
    else:
        # EXPLOIT: Use the best action we know
        return get_best_action(position)

# ============================================
# STEP 6: THE Q-LEARNING UPDATE! (THE MAGIC!)
# ============================================

def update_q_value(old_position, action, new_position, reward, alpha, gamma):
    """
    This is the heart of Q-Learning!
    Update the Q-value based on what happened.
    
    Parameters:
    - old_position: Where we were
    - action: What we did
    - new_position: Where we ended up
    - reward: What reward we got
    - alpha: Learning rate (0.1 = learn slowly and steadily)
    - gamma: Discount factor (0.9 = care about future rewards)
    """
    
    # STEP 1: Get the old Q-value (what we thought before)
    old_q = get_q_value(old_position, action)
    
    # STEP 2: Find the best Q-value at the NEW position
    # This represents "what's the best we could do from here?"
    max_future_q = max([get_q_value(new_position, a) for a in range(4)])
    
    # STEP 3: Calculate the new Q-value using THE FORMULA!
    # 
    # Explanation:
    # - reward: What we got right now
    # - gamma * max_future_q: What we might get in the future
    # - (reward + gamma * max_future_q): Total expected value
    # - (... - old_q): How wrong our old guess was
    # - alpha * (...): Small step towards the correct value
    # - old_q + alpha * (...): Update our guess slightly
    
    new_q = old_q + alpha * (reward + gamma * max_future_q - old_q)
    
    # STEP 4: Store the updated Q-value
    set_q_value(old_position, action, new_q)
    
    return old_q, new_q  # Return both for logging

# ============================================
# STEP 7: TRAINING LOOP (WHERE LEARNING HAPPENS!)
# ============================================

def train_agent(num_episodes=100, max_steps=50):
    """
    Train the agent for many episodes.
    
    An episode = one attempt to reach the goal from start
    """
    
    # Hyperparameters (these control how learning works)
    ALPHA = 0.1      # Learning rate: How fast to learn
    GAMMA = 0.9      # Discount: How much to value future rewards
    EPSILON_START = 1.0    # Start with lots of exploration
    EPSILON_DECAY = 0.01   # Decrease exploration over time
    EPSILON_MIN = 0.1      # Always keep some exploration
    
    print("=" * 60)
    print("STARTING Q-LEARNING TRAINING!")
    print("=" * 60)
    print(f"Episodes: {num_episodes}")
    print(f"Alpha (learning rate): {ALPHA}")
    print(f"Gamma (discount): {GAMMA}")
    print()
    
    # Train for many episodes
    for episode in range(num_episodes):
        
        # Start at the beginning
        agent_pos = START_POS.copy()
        
        # Calculate epsilon (exploration rate) for this episode
        # It starts high (1.0) and decreases over time
        epsilon = max(EPSILON_MIN, EPSILON_START - episode * EPSILON_DECAY)
        
        # Track episode stats
        total_reward = 0
        steps = 0
        
        # Run one episode
        for step in range(max_steps):
            
            # 1. Choose an action (explore or exploit)
            action = choose_action(agent_pos, epsilon)
            
            # 2. Take the action
            old_pos = agent_pos.copy()
            agent_pos = move_agent(agent_pos, action)
            
            # 3. Get reward
            reward = get_reward(agent_pos)
            total_reward += reward
            steps += 1
            
            # 4. UPDATE Q-VALUE! This is where learning happens!
            old_q, new_q = update_q_value(old_pos, action, agent_pos, reward, ALPHA, GAMMA)
            
            # 5. Check if reached goal
            if agent_pos[0] == GOAL_POS[0] and agent_pos[1] == GOAL_POS[1]:
                # Success! Start new episode
                break
        
        # Print progress every 10 episodes
        if (episode + 1) % 10 == 0:
            print(f"Episode {episode + 1:3d} | Steps: {steps:2d} | Reward: {total_reward:4.0f} | Epsilon: {epsilon:.2f} | Q-values learned: {len(q_table)}")
    
    print()
    print("=" * 60)
    print("TRAINING COMPLETE!")
    print("=" * 60)
    print(f"Total Q-values learned: {len(q_table)}")
    print()

# ============================================
# STEP 8: TEST THE TRAINED AGENT
# ============================================

def test_agent():
    """
    Test the trained agent (no more exploration, just use what it learned)
    """
    print("=" * 60)
    print("TESTING THE TRAINED AGENT")
    print("=" * 60)
    print("Agent will now use only what it learned (no random moves)")
    print()
    
    agent_pos = START_POS.copy()
    steps = 0
    max_steps = 20
    
    # Action names for printing
    action_names = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    
    print(f"Starting at {agent_pos}")
    
    while steps < max_steps:
        # Get best action (no exploration!)
        action = get_best_action(agent_pos)
        
        # Take action
        old_pos = agent_pos.copy()
        agent_pos = move_agent(agent_pos, action)
        steps += 1
        
        # Print what happened
        print(f"Step {steps}: From {old_pos} → {action_names[action]:5s} → {agent_pos}")
        
        # Check if reached goal
        if agent_pos[0] == GOAL_POS[0] and agent_pos[1] == GOAL_POS[1]:
            print()
            print(f"🎉 GOAL REACHED in {steps} steps!")
            print()
            return
    
    print()
    print("❌ Did not reach goal in time")
    print()

# ============================================
# STEP 9: VISUALIZE Q-TABLE (BONUS!)
# ============================================

def show_learned_policy():
    """
    Show what the agent learned: best action at each position
    """
    print("=" * 60)
    print("LEARNED POLICY (Best action at each position)")
    print("=" * 60)
    
    action_symbols = ['↑', '↓', '←', '→']
    
    print("\nGrid (arrows show best action):")
    print()
    
    for row in range(GRID_SIZE):
        line = ""
        for col in range(GRID_SIZE):
            pos = [row, col]
            
            if pos == GOAL_POS:
                line += " 🎯 "
            else:
                best_action = get_best_action(pos)
                line += f" {action_symbols[best_action]}  "
        
        print(line)
    
    print()

# ============================================
# STEP 10: RUN EVERYTHING!
# ============================================

if __name__ == "__main__":
    
    print()
    print("🤖 Q-LEARNING TUTORIAL")
    print("Teaching an agent to navigate a grid!")
    print()
    
    # Train the agent
    train_agent(num_episodes=100, max_steps=50)
    
    # Test what it learned
    test_agent()
    
    # Show the learned policy
    show_learned_policy()
    
    print("=" * 60)
    print("🎓 DONE! You just trained a reinforcement learning agent!")
    print("=" * 60)
    print()
    print("💡 TRY THIS:")
    print("1. Run this script multiple times - does it learn?")
    print("2. Change ALPHA to 0.5 - does it learn faster?")
    print("3. Change GAMMA to 0.5 - what happens?")
    print("4. Make the grid 10x10 instead of 5x5")
    print()