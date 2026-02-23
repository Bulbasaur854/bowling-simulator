from src.ball import Ball
from src.bowler import Bowler, BowlerStats
from src.lane import Lane
from src.io import *
from src.pindeck import PinDeck

# TODO Currently, the original pin loses its energy after hitting something, so we stop its raycast
#   What to do after pins hit something?
#   What about the walls after the lane?
# TODO Players often have a first shot release, and one for spares
# TODO Clean up
#   Get rid of magic numbers
#   Remove print statements from functions

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
    loft_distance=3.0,
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
    loft_distance=3.0,
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
    loft_distance=3.0,
    drift_consistency=0.0, target_accuracy=0.0, speed_control=0.0, 
    rev_consistency=0, rotation_consistency=0.0, tilt_consistency=0.0
)

# BOWLERS
# -------
stroker = Bowler("Norm D.", stroker_stats)
two_hander = Bowler("Jason B.", two_hand_stats)
beginner = Bowler("Straight Shooter", spare_stats)

def test_stuff():
    lane = Lane()    
    deck = PinDeck()

    player_choice = get_user_bowler()
    stance = float(input("Starting position: "))
    target = float(input("Aiming target: "))    
    match (player_choice):
        case (1): shot_params = stroker.throw_ball(stance, target)
        case (2): shot_params = two_hander.throw_ball(stance, target)
        case (3): shot_params = beginner.throw_ball(stance, target)

    # test_2_rolls(lane, player_choice, shot_params, deck)

def test_2_rolls(lane, player_choice, shot_params, deck):
    # ==========================
    #         ROLL 1
    # ==========================
    result_1 = lane.simulate_shot(widow_assassin, shot_params)
    print_lane_path(result_1["path"])
    
    hit_log_1 = deck.process_ball_impact(result_1["impact_board"], result_1["entry_angle"])
    print_pin_deck_result(deck, hit_log_1)

    # Check if we need to throw a second ball
    standing_pins = [pin for pin in deck.pins if pin.is_standing]    
    if len(standing_pins) > 0:
        # ==========================
        #         ROLL 2
        # ==========================        
        stance_2 = float(input("Roll 2 Starting position: "))
        target_2 = float(input("Roll 2 Aiming target: "))
        
        # Re-run the throw logic for the new inputs
        match (player_choice):
            case (1): shot_params_2 = stroker.throw_ball(stance_2, target_2)
            case (2): shot_params_2 = two_hander.throw_ball(stance_2, target_2)
            case (3): shot_params_2 = beginner.throw_ball(stance_2, target_2)
            
        result_2 = lane.simulate_shot(widow_assassin, shot_params_2)
        print_lane_path(result_2["path"])
        
        # Pass the SAME deck into the impact processor!
        hit_log_2 = deck.process_ball_impact(result_2["impact_board"], result_2["entry_angle"])
        print_pin_deck_result(deck, hit_log_2)
        
        # Final check for spare
        if len([pin for pin in deck.pins if pin.is_standing]) == 0:
            print(" SPARE!")
        else:
            print(" OPEN FRAME")

    # The frame is over. Reset the deck for the next bowler/frame!
    deck.reset()

if __name__ == "__main__":
    test_stuff()
