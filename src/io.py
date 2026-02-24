def get_user_bowler():
    """
    Get user bowler choice.
    """
    print(f"Lets bowl! Please pick a bowler:")
    print(" 1. Norm D.")
    print(" 2. Jason B.")
    print(" 3. New B.")
    player_choice = int(input("Answer: "))    
    
    return player_choice

def print_shot_simulation(start_x, start_y, target_x, target_y, launch_angle_rad, vel_x, vel_y):
    """
    Takes a bowler shot simulation results and prints them nicely to terminal.
    """ 
    print("Simulating Shot")
    print(f" start: ({start_x:.2f}, {start_y:.2f})\n target: ({target_x:.2f}, {target_y:.2f})")
    print(f" launch angle: {launch_angle_rad:.2f}")
    print(f" veloc: ({vel_x:.2f}, {vel_y:.2f})")

def print_lane_path(path):
    """
    Takes a ball movement path and prints it nicely to terminal.
    """    
    print("      LEFT                               RIGHT")
    print("      39                  20                 1")
    print("      |.......................................|")
    
    # Step backwards from 60ft to 0ft in 2-foot increments
    for target_y in range(60, -1, -2):
        # Find the coordinate in the path closest to this exact distance
        closest_point = min(path, key=lambda p: abs(p[0] - target_y))
        board_x = closest_point[1]        
        
        row_chars = ['.'] * 39 # default lane background
        
        # Draw Arrows around 14ft-16ft
        if target_y == 14 or target_y == 16:
            for arrow in [5, 10, 15, 20, 25, 30, 35]:
                arrow_idx = int(39 - arrow) # mirror for visual Left/Right
                row_chars[arrow_idx] = '^'
                
        # Draw the Ball ('O')
        if board_x < 0.5:            
            row_str = "".join(row_chars) + "O" # right Gutter
        elif board_x > 39.5: 
            row_str = "O" + "".join(row_chars) # left Gutter
        else:
            char_idx = int(39 - round(board_x)) # convert board 1-39 to string index 38-0
            row_chars[char_idx] = 'O'
            row_str = " " + "".join(row_chars) + " "

        # Add zone labels
        label = ""
        if target_y == 60: label = " <-- PINS / IMPACT"
        elif target_y == 40: label = " <-- PATTERN END"
        elif target_y == 16: label = " <-- ARROWS"
        elif target_y == 0:  label = " <-- FOUL LINE"        
        
        print(f"{target_y:02d}ft |{row_str}|{label}") # print the row

def print_pin_deck_result(deck, hit_log):
    """
    Takes the simulation results and prints them nicely to temrinal.
    """
    if hit_log:
        for log in hit_log:
            print(log)
    
        # Check the total count
        pins_down = len(hit_log)    
        if pins_down == 10:
            print(" STRIKE!")
        else:
            # Find which pins are still standing
            standing_pins = [str(pin.id) for pin in deck.pins if pin.is_standing]
            print(f" Count: {pins_down} | Left Standing: {', '.join(standing_pins)}")
    else:
        print(" Count: 0 | Left Standing: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10")

def print_scorecard(scorecard):
    """Draws a live TV-style 10-frame bowling scorecard to the terminal."""
    print("\n" + "=" * 65)
    
    # Header Row (Frame Numbers)
    header = "|" + "|".join([f"  {i}  " for i in range(1, 10)]) + "|   10   |"
    print(header)
    print("-" * 65)
    
    # Rolls Row (X, /, -)
    rolls_str = "|"
    for i in range(9):
        val = format_frame_rolls(scorecard.frames[i])
        rolls_str += f" {val} |"
    val10 = format_frame_10(scorecard.frames[9])
    rolls_str += f" {val10}  |"
    print(rolls_str)
    
    # Scores Row (Running Totals)
    scores_str = "|"
    for i in range(9):
        score = scorecard.frames[i].display_score
        s_str = str(score) if score is not None else ""
        scores_str += f"{s_str:^5}|"
        
    score10 = scorecard.frames[9].display_score
    s_str10 = str(score10) if score10 is not None else ""
    scores_str += f"{s_str10:^8}|"
    print(scores_str)
    
    print("=" * 65 + "\n")

def format_frame_rolls(frame):
    """Translates Frames 1-9 rolls into a 3-character bowling string."""
    if not frame.rolls:
        return "   "
    if len(frame.rolls) == 1:
        if frame.rolls[0] == 10:
            return " X "
        else:
            r1 = "-" if frame.rolls[0] == 0 else str(frame.rolls[0])
            return f"{r1}  "
    if len(frame.rolls) == 2:
        r1 = "-" if frame.rolls[0] == 0 else str(frame.rolls[0])
        if sum(frame.rolls) == 10:
            r2 = "/"
        else:
            r2 = "-" if frame.rolls[1] == 0 else str(frame.rolls[1])
        return f"{r1} {r2}"

def format_frame_10(frame):
    """Translates 10th Frame rolls into a 5-character bowling string."""
    if not frame.rolls:
        return "     "
    
    strs = []
    for i, r in enumerate(frame.rolls):
        if r == 10:
            # Check if this 10 is actually picking up a spare (e.g., 0 on roll 1, 10 on roll 2)
            if i == 1 and frame.rolls[0] < 10 and frame.rolls[0] + r == 10:
                strs.append("/")
            else:
                strs.append("X")
        elif r == 0:
            strs.append("-")
        else:
            if i == 1 and frame.rolls[0] + r == 10:
                strs.append("/")
            elif i == 2 and frame.rolls[0] == 10 and frame.rolls[1] < 10 and frame.rolls[1] + r == 10:
                strs.append("/")
            else:
                strs.append(str(r))
                
    while len(strs) < 3:
        strs.append(" ")
        
    return f"{strs[0]} {strs[1]} {strs[2]}"