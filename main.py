from src.ball import Ball
from src.bowler import Bowler, BowlerStats
from src.lane import Lane
from src.physics import PhysicsEngine

def test_stuff():
    lane = Lane()
    physics_engine = PhysicsEngine(lane)

    black_widow = Ball(
        name="Hammer Black Widow 3.0 Dynasty",
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

    pro_stats = BowlerStats(
        rev_rate=450, 
        ball_speed=18.0, 
        axis_rotation=60, 
        axis_tilt=10,
        board_deviation=0.5, # Very tight targeting (+/- 0.5 boards)
        speed_deviation=0.2, # Precision speed control
        revs_deviation=15 # Consistent release
    )
    player = Bowler("Jason B.", pro_stats)

    print(f"\n{'='*40}")
    print(f" NOW BOWLING: {player.name}")
    print(f" Ball: {black_widow.name} ({black_widow.cover_type})")
    print(f" Pattern: {lane.name} ({lane.length_ft}ft)")
    print(f"{'='*40}\n")
    
    shot_params = player.release_shot(target_board=15)
    print(f"{'='*40}")
    print(f" Speed: {shot_params["speed"]}")
    print(f" Revs: {shot_params["revs"]}")
    print(f" Board at arrows: {shot_params["board_at_arrows"]}")
    print(f" Axis rotation: {shot_params["axis_rotation"]}")
    print(f" Axis tilt: {shot_params["axis_tilt"]}")
    print(f"{'='*40}\n")

    result = physics_engine.simulate_shot(black_widow, shot_params)
    print(f"{result}")

if __name__ == "__main__":
    test_stuff()
