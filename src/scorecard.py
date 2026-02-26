from src.constants import (
    FINAL_FRAME_INDEX,
    FIRST_FRAME_NUMBER,
    MAX_PINS,
    REGULAR_FRAMES,
    TOTAL_FRAMES,
)

class Frame:
    def __init__(self, frame_number):
        self.frame_number = frame_number
        self.rolls = []
        self.status = "Empty"
        self.display_score = None

    def is_done(self):
        """Determines if the frame has completed all rolls."""
        if self.frame_number < TOTAL_FRAMES:
            return self.status in ["Open", "Spare", "Strike"]        
        else: # 10th frame rules
            num_of_rolls = len(self.rolls)
            if num_of_rolls == 3:
                return True
            if num_of_rolls == 2 and sum(self.rolls) < MAX_PINS: # open 10th frame
                return True
            return False

class Scorecard:
    def __init__(self):
        self.frames = [Frame(i) for i in range(FIRST_FRAME_NUMBER, TOTAL_FRAMES + 1)]
        self.raw_rolls = []
        self.current_frame_index = 0

    def record_roll(self, pins_down):
        """Logs a roll, updates current frame status and recalculates score"""
        if self.current_frame_index >= TOTAL_FRAMES or self.frames[FINAL_FRAME_INDEX].is_done():
            return # game is over

        # Add the current roll score to both the frame and the scorecard 
        self.raw_rolls.append(pins_down)
        current_frame = self.frames[self.current_frame_index]
        current_frame.rolls.append(pins_down)

        # Update frame status
        if current_frame.frame_number < TOTAL_FRAMES:
            if len(current_frame.rolls) == 1:
                if pins_down == MAX_PINS:
                    current_frame.status = "Strike"
                else:
                    current_frame.status = "Incomplete"
            elif len(current_frame.rolls) == 2:
                if sum(current_frame.rolls) == MAX_PINS:
                    current_frame.status = "Spare"
                else:
                    current_frame.status = "Open"
        else: # 10th Frame            
            if current_frame.is_done():
                current_frame.status = "Done"
            else:
                current_frame.status = "Incomplete"
                
        # Move to next frame if done
        if current_frame.is_done() and self.current_frame_index < REGULAR_FRAMES:
            self.current_frame_index += 1
        elif current_frame.frame_number == TOTAL_FRAMES and current_frame.is_done():
            self.current_frame_index = TOTAL_FRAMES
            
        self.recalculate_scores()

    def recalculate_scores(self):
        """Loops through the flat rolls list to calculate the running total."""
        running_total = 0
        roll_index = 0
        
        for i in range(TOTAL_FRAMES):
            frame = self.frames[i]
            
            # if we haven't reached this frame in the rolls yet, stop calculating
            if roll_index >= len(self.raw_rolls):
                break
                
            if frame.frame_number < TOTAL_FRAMES:
                if frame.status == "Strike":
                    # look ahead 2 rolls
                    if roll_index + 2 < len(self.raw_rolls):
                        running_total += MAX_PINS + self.raw_rolls[roll_index+1] + self.raw_rolls[roll_index+2]
                        frame.display_score = running_total
                    roll_index += 1 # strike consumes 1 roll in the flat list
                    
                elif frame.status == "Spare":
                    # look ahead to next frame's 1 roll
                    if roll_index + 2 < len(self.raw_rolls):
                        running_total += MAX_PINS + self.raw_rolls[roll_index+2]
                        frame.display_score = running_total
                    roll_index += 2 # spare consumes 2 rolls
                    
                elif frame.status == "Open":
                    running_total += sum(frame.rolls)
                    frame.display_score = running_total
                    roll_index += 2 # open frame consumes 2 rolls
            else: # 10th Frame Math (No look-ahead bonuses)                
                if frame.is_done():
                    running_total += sum(frame.rolls)
                    frame.display_score = running_total
