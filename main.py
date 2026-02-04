from src.ball import Ball
from src.bowler import Bowler, BowlerStats
from src.lane import Lane

def test_stuff():

    # checks = [
    #     ("Foul Line (Heavy Oil)", 20, 0),
    #     ("Foul Line (Dry Outside)", 5, 0),
    #     ("Backend (Dry Backend)", 20, 50),
    #     ("Pin Deck (Always Dry)", 20, 60),
    #     ("Foul Line (Board 1)", 1, 0),
    #     ("Foul Line (Board 39)", 39, 0),
    #     ("Midlane (20ft)", 20, 20),
    #     ("Midlane (35ft)", 20, 35),
    #     ("Clamped Board Low", -5, 10),
    #     ("Clamped Board High", 50, 10),
    #     ("Clamped Distance Low", 20, -5),
    # ]
    # lane = Lane()
    # for name, board, ft in checks:
    #     print(f"Board {board:02d} | {ft:02d}ft | {lane.get_friction(board, ft)}")

    # spare_ball = Ball(
    #     name="White Dot",
    #     weight=15,
    #     rg=2.65,
    #     diff=0.01,
    #     mass_bias=0.0,
    #     grit=5000,
    #     cover_type="Plastic"
    # )
    # black_widow = Ball(
    #     name="Hammer Black Widow 3.0 Dynasty",
    #     weight=15,
    #     rg=2.5,
    #     diff=0.058,
    #     mass_bias=0.016,
    #     grit=2000,
    #     cover_type="Reactive"
    # )
    # print(f"White Dot surface friction modifier: {spare_ball.get_surface_friction_modifier()}")
    # print(f"Black Widow surface friction modifier: {black_widow.get_surface_friction_modifier()}")

    # pro_stats = BowlerStats(
    #     rev_rate=450, 
    #     ball_speed=18.0, 
    #     axis_rotation=60, 
    #     axis_tilt=10,
    #     board_deviation=0.5, # Very tight targeting (+/- 0.5 boards)
    #     speed_deviation=0.2, # Precision speed control
    #     revs_deviation=15 # Consistent release
    # )

    # jason = Bowler("Jason B.", pro_stats)
    # print(f"{jason.release_shot(target_board=10)}")

if __name__ == "__main__":
    test_stuff()
