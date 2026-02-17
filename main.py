from src.ball import Ball
from src.bowler import Bowler, BowlerStats
from src.lane import Lane
from src.physics import PhysicsEngine
from src.output import print_lane_path

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
        rev_rate=550,
        ball_speed=18.0,
        approach_drift=1,
        arm_swing_offset=4,
        axis_rotation=60,
        axis_tilt=10,
        rev_consistency=10,
        speed_control=1,
        target_accuracy=1,
        drift_consistency=0.5,
        rotation_consistency=0,
        tilt_consistency=0
    )
    
    print(f"{'-'*16}")

    bowler = Bowler("Tair S.", my_stats)
    throw_result = bowler.throw_ball(24, 10)
    simulation_result = physics_engine.simulate_shot(black_widow, throw_result)
    print("\nShot Results")
    print(f" impact board: {simulation_result["impact_board"]}")
    print(f" entry angle: {simulation_result["entry_angle"]}")
    print(f" velocity at impact: {simulation_result["velocity_at_impact"]:.2f}")

    print_lane_path(simulation_result["path"])

    # laydown_point = result["laydown_point"]
    # actual_target = result["actual_target"]
    # launch_speed = result["launch_speed"]
    # launch_revs = result["launch_revs"]
    # actual_rotation = result["actual_rotation"]
    # actual_tilt = result["actual_tilt"]

    # print(f"Shot Results\n")
    # print(f" Release board: {laydown_point[0]:.2f}")
    # print(f" Hit board: {actual_target[0]:.2f}")
    # print(f" Launch speed: {launch_speed:.2f}")
    # print(f" Launch revs: {launch_revs:.2f}")
    # print(f" Rotation: {actual_rotation:.2f}")
    # print(f" Tilt: {actual_tilt:.2f}")

    print(f"{'-'*16}")

if __name__ == "__main__":
    test_stuff()
