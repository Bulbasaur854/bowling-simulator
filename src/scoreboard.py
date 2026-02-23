class Frame:
    def __init__(self, frame_number):
        self.frame_number = frame_number
        self.rolls = []
        self.status = "Empty"
        self.display_score = None

    def is_done(self):
        """Determines if the frame has completed all rolls."""
        if self.frame_number < 10:
            return self.status in ["Open", "Spare", "Strike"]        
        else: # 10th frame rules
            num_of_rolls = len(self.rolls)
            sum_of_rolls = sum(self.rolls)
            if num_of_rolls == 3:
                return True
            if num_of_rolls == 2 and sum(sum_of_rolls) < 10: #open 10th frame
                return True
            return False