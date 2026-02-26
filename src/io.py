import os, subprocess

def get_user_bowler(bowler_list):
    """
    Get user bowler choice and returns the bowler object
    """
    print("\nPlease pick a bowler:")
    for i, bowler in enumerate(bowler_list):
        print(f" {i + 1}. {bowler.name}")
        
    while True:
        try:
            choice = int(input("Answer: ")) - 1
            if 0 <= choice < len(bowler_list):
                return bowler_list[choice]
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")

def get_user_ball(ball_list):
    """
    Get user ball choice and returns the ball object
    """
    print("\nChoose your ball:")
    for i, ball in enumerate(ball_list):
        print(f" {i + 1}. {ball.name} ({ball.cover_type})")
        
    while True:
        try:
            choice = int(input("Answer: ")) - 1
            if 0 <= choice < len(ball_list):
                return ball_list[choice]
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")

def get_throw_or_change(current_ball):
    """
    Get user choice to change ball or not.
    """
    print(f"Current Ball: {current_ball.name}")
    action = input("[T]hrow or [C]hange Ball? ").upper()

    return action

def get_valid_input(request_string):
    """
    Get user input and clamp between 1 and 39
    """
    ans = int(input(request_string))

    return max(1, min(ans, 39))

def print_shot_simulation(start_x, start_y, target_x, target_y, launch_angle_rad, vel_x, vel_y):
    """
    Takes a bowler shot simulation results and prints them nicely to terminal.
    """ 
    print("\nSimulating Shot")
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

def print_pin_deck_result(deck, hit_log, current_frame):
    """
    Takes the simulation results and prints them nicely to temrinal.
    """
    if hit_log:
        for log in hit_log:
            print(log)
    
        # Check the total count
        pins_down = len(hit_log)    
        if pins_down == 10:
            if len(current_frame.rolls) == 0:
                print(" STRIKE!")
            else:
                print(" SPARE!")
        else:
            # Find which pins are still standing
            standing_pins = [str(pin.id) for pin in deck.pins if pin.is_standing]
            if len(standing_pins) == 0:
                print(" SPARE!")
            else:
                print(f" Count: {pins_down} | Left Standing: {', '.join(standing_pins)}")
    else:
        print(" Count: 0 | Left Standing: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10")

def print_scorecard(scorecard):
    """
    Draws a live TV-style 10-frame bowling scorecard to the terminal.
    """
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

def print_welcome_screen():
    """
    Outputs the welcome screen.
    """
    print("\n" + '='*55)
    print("BOWNLING SIMU")
    print('='*55)

def print_current_state(current_frame, deck):
    """
    Prints the HUD context for the player before they take their shot.
    Tells them the frame, the ball number, and what pins are standing.
    """
    ball_number = len(current_frame.rolls) + 1    
    standing_pins = [str(pin.id) for pin in deck.pins if pin.is_standing]
    
    print(f"\n--- FRAME {current_frame.frame_number} | BALL {ball_number} ---")
    
    if len(standing_pins) == 10:
        print(" Target: Full rack standing.")
    elif len(standing_pins) == 0:
        print(" Target: None. (Waiting for deck reset...)")
    else:
        print(f" Target: You left the {', '.join(standing_pins)}")
        
    print("-" * 55)

def print_end_game_scorecard(scorecard):
    """
    Ouputs the final score of the game.
    """
    print_scorecard(scorecard)
    print("GAME OVER\n" + '-'*9)
    print(f"Final Score: {scorecard.frames[9].display_score}")

def format_frame_rolls(frame):
    """
    Translates Frames 1-9 rolls into a 3-character bowling string.
    """
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
    """
    Translates 10th Frame rolls into a 5-character bowling string.
    """
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

def clear_terminal():
    command = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run(command, shell=True)