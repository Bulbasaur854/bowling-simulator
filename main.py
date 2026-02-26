from src.io import (
    clear_terminal,
    get_throw_or_change,
    get_user_ball,
    get_user_bowler,
    get_valid_input,
    print_current_state,
    print_end_game_scorecard,
    print_lane_path,
    print_pin_deck_result,
    print_scorecard,
    print_welcome_screen,
)
from src.lane import Lane
from src.pindeck import PinDeck
from src.scorecard import Scorecard
from src.roster import AVAILABLE_BOWLERS, AVAILABLE_BALLS 

# TODO Clean up - get rid of magic numbers and remove print statements from functions
# TODO Add a way to quit the game elegantly

def main():
    play_game()

def play_game():
    # Pre-game
    # --------
    print_welcome_screen()
    bowler = get_user_bowler(AVAILABLE_BOWLERS)
    current_ball = get_user_ball(AVAILABLE_BALLS)

    lane = Lane()
    deck = PinDeck()
    scorecard = Scorecard()

    # Main loop
    # ---------
    while scorecard.current_frame_index < 10:
        # Update the HUD
        clear_terminal()
        print_scorecard(scorecard)

        # Print the context
        current_frame = scorecard.frames[scorecard.current_frame_index]
        print_current_state(current_frame, deck)

        # Pre-shot menu
        action = get_throw_or_change(current_ball).upper()
        if action == "C":
            current_ball = get_user_ball(AVAILABLE_BALLS)
            continue # restart the loop to update HUD

        # Get shot input
        stance = get_valid_input("Starting Position (1-39): ")
        target = get_valid_input("Aiming Target (1-39): ")

        # The simulation
        release_params = bowler.approach(stance, target)
        result = lane.simulate_shot(current_ball, release_params)
        print_lane_path(result["path"])

        # Collision and scoring
        hit_log = deck.process_ball_impact(result["impact_board"], result["entry_angle"])
        print_pin_deck_result(deck, hit_log, current_frame)
        knocked_pins = len(hit_log) if hit_log else 0
        scorecard.record_roll(knocked_pins)

        if current_frame.is_done():
            deck.reset()
        
        input("\nPress Enter to continue...")

    # Post-game
    # ---------
    clear_terminal()
    print_end_game_scorecard(scorecard)

if __name__ == "__main__":
    main()
