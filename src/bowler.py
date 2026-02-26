import random
from dataclasses import dataclass

@dataclass
class BowlerStats:  
    approach_drift: float           # e.g., +2.0 (Slides left of stance)
    arm_swing_offset: float         # ----- 7.0 (Ball is 7 boards right of slide)
    ball_speed: float               # ----- 17.0 mph
    rev_rate: int                   # ----- 400 rpm
    axis_rotation: float            # ----- 55 degrees
    axis_tilt: float                # ----- 10 degrees
    loft_distance: float            # ----- 3.0 ft

    # Standard deviations to represent skill
    # Value of 0 is the most accurate bowler
    drift_consistency: float        # variance in sliding
    target_accuracy: float          # -------- in hitting arrows
    speed_control: float            # -------- in speed
    rev_consistency: int            # -------- in revs
    rotation_consistency: float     # -------- in hand position (e.g., +/- 5 degrees)
    tilt_consistency: float         # -------- in spin axis (e.g., +/- 2 degrees)

class Bowler:
    def __init__(self, name, stats: BowlerStats):
        self.name = name
        self.stats = stats

    def approach(self, stance_board, target_board):
        actual_drift = random.gauss(self.stats.approach_drift, self.stats.drift_consistency)
        slide_point = stance_board + actual_drift
        laydown_point = slide_point - self.stats.arm_swing_offset
        actual_target = random.gauss(target_board, self.stats.target_accuracy)
        launch_speed = random.gauss(self.stats.ball_speed, self.stats.speed_control)
        launch_revs = random.gauss(self.stats.rev_rate, self.stats.rev_consistency)
        actual_rotation = random.gauss(self.stats.axis_rotation, self.stats.rotation_consistency)
        actual_tilt = max(0, random.gauss(self.stats.axis_tilt, self.stats.tilt_consistency))

        return {
            "laydown_point": (laydown_point, 0.0),
            "actual_target": (actual_target, 15.0),
            "launch_speed": launch_speed,
            "launch_revs": launch_revs,
            "launch_rotation": actual_rotation,
            "launch_tilt": actual_tilt,
            "loft_distance": self.stats.loft_distance
        }