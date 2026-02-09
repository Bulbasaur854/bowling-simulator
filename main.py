from src.ball import Ball
from src.bowler import Bowler, BowlerStats
from src.lane import Lane
from src.physics import PhysicsEngine

def test_stuff():
    lane = Lane()
    physics_engine = PhysicsEngine(lane)

    black_widow = Ball(
        name="Black Widow",
        weight=15,
        rg=2.5,
        diff=0.058,
        mass_bias=0.016,
        grit=2000,
        cover_type="Reactive"
    )
    spare_ball = Ball(
        name="White Dot",
        weight=15,
        rg=2.65,
        diff=0.01,
        mass_bias=0.0,
        grit=5000,
        cover_type="Plastic"
    )

    my_stats = BowlerStats(
        rev_rate=450,
        ball_speed=18.0,
        approach_drift=-5,
        arm_swing_offset=7,
        axis_rotation=60,
        axis_tilt=10,
        rev_consistency=30,
        speed_control=1,
        target_accuracy=2,
        drift_consistency=0.5,
        rotation_consistency=2,
        tilt_consistency=2
    )
    
    print(f"{'-'*16}")

    bowler = Bowler("Tair S.", my_stats)
    result = bowler.throw_ball(20, 10)

    laydown_point = result["laydown_point"]
    aim_point = result["aim_point"]
    launch_speed = result["launch_speed"]
    launch_revs = result["launch_revs"]
    axis_rotation = result["axis_rotation"]
    axis_tilt = result["axis_tilt"]

    print(f"Shot Results\n")
    print(f" Release board: {laydown_point[0]:.2f}")
    print(f" Hit board: {aim_point[0]:.2f}")
    print(f" Launch speed: {launch_speed:.2f}")
    print(f" Launch revs: {launch_revs:.2f}")
    print(f" Rotation: {axis_rotation:.2f}")
    print(f" Tilt: {axis_tilt:.2f}")

    print(f"{'-'*16}")

if __name__ == "__main__":
    test_stuff()
