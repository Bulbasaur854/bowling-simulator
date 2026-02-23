def get_user_bowler():
    print("\n" + "="*55)
    print(f"Lets bowl! Please pick a bowler:\n")
    print(" 1. Norm D.")
    print(" 2. Jason B.")
    print(" 3. New B.")
    player_choice = int(input("\nAnswer: "))    
    print("\n" + "="*55)
    
    return player_choice

def print_shot_simulation(start_x, start_y, target_x, target_y, launch_angle_rad, vel_x, vel_y):
    print("\nSimulating Shot")
    print(f" start: ({start_x:.2f}, {start_y:.2f})\n target: ({target_x:.2f}, {target_y:.2f})")
    print(f" launch angle: {launch_angle_rad:.2f}")
    print(f" veloc: ({vel_x:.2f}, {vel_y:.2f})")

def print_lane_path(path):
    print("\n" + "="*55)
    print(" 🎳 LANE PATH VISUALIZATION (Top-Down) 🎳")
    print("="*55)
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

    print("="*55 + "\n")

def print_pin_deck_result(deck, hit_log):
    """
    Takes the simulation results from the PinDeck and formats them 
    into a clean terminal output, including strike/spare analysis.
    """
    if hit_log:
        for log in hit_log:
            print(log)
        print("-"*55)
    
        # Check the total count
        pins_down = len(hit_log)    
        if pins_down == 10:
            print(" ❌ STRIKE! ❌")
        else:
            # Find which pins are still standing
            standing_pins = [str(pin.id) for pin in deck.pins if pin.is_standing]
            print(f" Count: {pins_down} | Left Standing: {', '.join(standing_pins)}")
    else:
        print("-"*55)
        print(" Count: 0 | Left Standing: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10")

    print("="*55 + "\n")