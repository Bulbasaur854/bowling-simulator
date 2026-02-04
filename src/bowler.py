import random
from dataclasses import dataclass

@dataclass
class BowlerStats:
    rev_rate: int          # e.g., 450 RPM
    ball_speed: float      # e.g., 17.0 MPH (at release)
    axis_rotation: float   # e.g., 55 degrees (side roll)
    axis_tilt: float       # e.g., 12 degrees (spin)
    
    # Standard deviations, lower is better. 
    # A pro might be 0.5 boards, an amateur 3.0.
    board_deviation: float  # Variance in hitting the target board
    speed_deviation: float  # Variance in speed control (e.g., +/- 0.2 mph)
    revs_deviation: float # Variance in rev rate (e.g., +/- 20 rpm)

class Bowler:
    def __init__(self, name, stats: BowlerStats):
        self.name = name
        self.stats = stats

    def release_shot(self, target_board, target_speed_modifier=0.0):
        """
        Calculates the actual release parameters based on the intended target
        and the bowler's consistency stats.
        
        target_board: The board the bowler is trying to hit at the arrows (15ft).
        target_speed_modifier: Adjusts base speed (e.g., -1.0 for a slow hook).
        """
        
        # 1. Calculate Actual Speed (Base + Modifier + Variance)
        intended_speed = self.stats.ball_speed + target_speed_modifier
        actual_speed = random.gauss(intended_speed, self.stats.speed_deviation)
        
        # 2. Calculate Actual Rev Rate (Base + Variance)
        actual_revs = random.gauss(self.stats.rev_rate, self.stats.revs_deviation)
        
        # 3. Calculate Actual Target Hit (Intended Board + Variance)
        # We assume the bowler is aiming at the arrows (15ft mark)
        actual_board_at_arrows = random.gauss(target_board, self.stats.board_deviation)
        
        return {
            "speed": round(actual_speed, 2),
            "revs": int(actual_revs),
            "board_at_arrows": round(actual_board_at_arrows, 2),
            "axis_rotation": self.stats.axis_rotation, # Assuming constant for now
            "axis_tilt": self.stats.axis_tilt
        }