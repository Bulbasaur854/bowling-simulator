from src.ball import Ball
from src.bowler import Bowler, BowlerStats
from src.lane import Lane
from src.physics import PhysicsEngine
from src.output import print_lane_path

def test_stuff():
    lane = Lane()
    physics_engine = PhysicsEngine(lane)

    # BALLS
    # -----

    # Weaker, symmetrical solid ball
    hyroad = Ball(name="Symmetrical Benchmark", weight=15, rg=2.57, diff=0.046, mass_bias=0.0, grit=3000, cover_type="Solid")
    # Strong, asymmetrical hooking monster
    widow_assassin = Ball(name="High Asym Solid", weight=15, rg=2.48, diff=0.058, mass_bias=0.024, grit=1000, cover_type="Solid")
    # Plastic, pancake core
    white_dot = Ball(name="Plastic Spare", weight=15, rg=2.65, diff=0.010, mass_bias=0.0, grit=5000, cover_type="Plastic")

    # BOWLERS STATS
    # -------------
    # Keep consistencies near zero for testing

    # Low revs, low rotation, precision player
    stroker_stats = BowlerStats(
        rev_rate=280, 
        ball_speed=15.5, 
        approach_drift=0.0, 
        arm_swing_offset=6.0, 
        axis_rotation=25.0, # staying up the back of the ball
        axis_tilt=15.0,        
        drift_consistency=0.0, target_accuracy=0.0, speed_control=0.0, 
        rev_consistency=0, rotation_consistency=0.0, tilt_consistency=0.0
    )
    # Huge power, high rotation
    two_hand_stats = BowlerStats(
        rev_rate=550, 
        ball_speed=18.5, 
        approach_drift=4.0, # deep left stance, drifts even further left
        arm_swing_offset=5.0, # ball is closer to the body for two-handers
        axis_rotation=65.0, # heavy side-roll
        axis_tilt=5.0, # very end-over-end tilt
        drift_consistency=0.0, target_accuracy=0.0, speed_control=0.0, 
        rev_consistency=0, rotation_consistency=0.0, tilt_consistency=0.0
    )
    # Throwing hard and flat to pick up spares
    spare_stats = BowlerStats(
        rev_rate=150, # killing the wrist
        ball_speed=19.0, # throwing it hard
        approach_drift=0.0, 
        arm_swing_offset=7.0, 
        axis_rotation=10.0, # pure forward roll
        axis_tilt=5.0,
        drift_consistency=0.0, target_accuracy=0.0, speed_control=0.0, 
        rev_consistency=0, rotation_consistency=0.0, tilt_consistency=0.0
    )

    # BOWLERS
    # -------

    stroker = Bowler("Norm D.", stroker_stats)
    two_hander = Bowler("Jason B.", two_hand_stats)
    beginner = Bowler("Straight Shooter", spare_stats)

    test_shots = [
        # (stroker, hyroad, 15.0, 10.0),
        (two_hander, widow_assassin, 38.0, 20.0),
        (two_hander, hyroad, 38.0, 20.0),
        # (beginner, white_dot, 15.0, 15.0)
    ]

    for player, ball, stance, target in test_shots:
        print(f"\n{'*'*50}")
        print(f" TESTING: {player.name} with {ball.name}")
        print(f"{'*'*50}")
        
        shot_params = player.throw_ball(stance, target)
        result = physics_engine.simulate_shot(ball, shot_params)
        
        print(f"Impact Board: {result['impact_board']}")
        print_lane_path(result['path'])

if __name__ == "__main__":
    test_stuff()
