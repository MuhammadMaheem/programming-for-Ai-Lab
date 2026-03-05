jug1 = 0  # 4-liter jug
jug2 = 0  # 5-liter jug
cap_1 = 4
cap_2 = 5
goal = 2

step = 0
print(f"Step {step}: Jug1 = {jug1}, Jug2 = {jug2}")

while jug1 != goal and jug2 != goal:
    step += 1
    
    if jug2 == 0:
        jug2 = cap_2
        print(f"Step {step}: Fill Jug2 → Jug1={jug1}, Jug2={jug2}")
    
    elif jug1 == cap_1:
        jug1 = 0
        print(f"Step {step}: Empty Jug1 → Jug1={jug1}, Jug2={jug2}")
    
    else:
        space_in_jug1 = cap_1 - jug1  
        
        if jug2 >= space_in_jug1:
            jug1 = cap_1
            jug2 = jug2 - space_in_jug1
        else:
            jug1 = jug1 + jug2
            jug2 = 0
        
        print(f"Step {step}: Pour Jug2→Jug1 → Jug1={jug1}, Jug2={jug2}")

print("\n✅ Goal reached!")