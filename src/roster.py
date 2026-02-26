from src.ball import Ball
from src.bowler import Bowler, BowlerStats

# BALLS
# -----
hyroad = Ball(name="Hyroad", weight=15, rg=2.57, diff=0.046, mass_bias=0.0, grit=3000, cover_type="Solid")
widow_assassin = Ball(name="Widow Assassin", weight=15, rg=2.48, diff=0.058, mass_bias=0.024, grit=1000, cover_type="Solid")
white_dot = Ball(name="White Dot", weight=15, rg=2.65, diff=0.010, mass_bias=0.0, grit=5000, cover_type="Plastic")

# --- BOWLER STATS ---
stroker_stats = BowlerStats(rev_rate=280, ball_speed=15.5, approach_drift=0.0, arm_swing_offset=6.0, axis_rotation=25.0, axis_tilt=15.0, loft_distance=3.0, drift_consistency=0.0, target_accuracy=0.0, speed_control=0.0, rev_consistency=0, rotation_consistency=0.0, tilt_consistency=0.0)
two_hand_stats = BowlerStats(rev_rate=550, ball_speed=18.5, approach_drift=4.0, arm_swing_offset=5.0, axis_rotation=65.0, axis_tilt=5.0, loft_distance=3.0, drift_consistency=0.0, target_accuracy=0.0, speed_control=0.0, rev_consistency=0, rotation_consistency=0.0, tilt_consistency=0.0)
spare_stats = BowlerStats(rev_rate=150, ball_speed=19.0, approach_drift=0.0, arm_swing_offset=7.0, axis_rotation=10.0, axis_tilt=5.0, loft_distance=3.0, drift_consistency=0.0, target_accuracy=0.0, speed_control=0.0, rev_consistency=0, rotation_consistency=0.0, tilt_consistency=0.0)

# --- BOWLERS ---
stroker = Bowler("Norm D.", stroker_stats, strike_balls=[hyroad, widow_assassin], spare_ball=white_dot)
two_hander = Bowler("Jason B.", two_hand_stats, strike_balls=[hyroad, widow_assassin], spare_ball=white_dot)
beginner = Bowler("Straight Shooter", spare_stats, strike_balls=[hyroad, widow_assassin], spare_ball=white_dot)

# --- EXPORT LISTS ---
AVAILABLE_BOWLERS = [stroker, two_hander, beginner]