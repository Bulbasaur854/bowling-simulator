# TODO Make it so the oil on lane gets "pushed"
# TODO The original pin loses its energy after hitting something, so we stop its raycast. What to do after pins hit something? What about the walls after the lane?

from src.io import (
    clear_terminal,
    get_throw_or_change,
    get_user_ball,
    get_user_bowler,
    get_valid_input,
    print_current_state,
    print_end_game_scorecard,
    print_quit_game_scorecard,
    print_lane_path,
    print_pin_deck_result,
    print_scorecard,
    print_welcome_screen,
)
from src.lane import Lane
from src.pindeck import PinDeck
from src.scorecard import Scorecard
from src.roster import AVAILABLE_BOWLERS
from src.constants import LANE_BOARDS, MAX_PINS, MIN_BOARD, TOTAL_FRAMES

def should_reset_deck_after_roll(frame):
    """
    Determine whether pins should be reset before the next shot.
    """
    if frame.frame_number < TOTAL_FRAMES:
        return frame.is_done()

    # 10th-frame deck reset rules:
    # - Strike on first ball -> reset for second ball
    # - Spare in first two balls -> reset for first ball
    # - Double in first two balls -> reset for third ball
    if len(frame.rolls) == 1:
        return frame.rolls[0] == MAX_PINS
    if len(frame.rolls) == 2:
        first, second = frame.rolls
        if first == MAX_PINS and second == MAX_PINS:
            return True
        if first < MAX_PINS and first + second == MAX_PINS:
            return True
    return False

def main():
    play_game()

def play_game():
    # Pre-game
    # --------
    print_welcome_screen()
    bowler = get_user_bowler(AVAILABLE_BOWLERS)
    current_ball = get_user_ball(bowler.strike_balls)

    lane = Lane()
    deck = PinDeck()
    scorecard = Scorecard()
    user_quit = False

    # Main loop
    # ---------
    while scorecard.current_frame_index < TOTAL_FRAMES:
        # Update the HUD
        clear_terminal()
        print_scorecard(scorecard)

        # Print the context
        current_frame = scorecard.frames[scorecard.current_frame_index]
        print_current_state(current_frame, deck)

        # Pre-shot menu
        action = get_throw_or_change(current_ball).upper()
        if action == "C":
            current_ball = get_user_ball(bowler.strike_balls)
            continue # restart the loop to update HUD
        if action == "S":
            current_ball = bowler.spare_ball
        if action == "Q":
            user_quit = True
            break

        # Get shot input
        stance = get_valid_input(f"Starting Position ({MIN_BOARD}-{LANE_BOARDS}): ")
        target = get_valid_input(f"Aiming Target ({MIN_BOARD}-{LANE_BOARDS}): ")

        # The simulation
        release_params = bowler.approach(stance, target)
        result = lane.simulate_shot(current_ball, release_params)
        print_lane_path(result["path"])

        # Collision and scoring
        hit_log = deck.process_ball_impact(result["impact_board"], result["entry_angle"])
        print_pin_deck_result(deck, hit_log, current_frame)
        knocked_pins = len(hit_log) if hit_log else 0
        scorecard.record_roll(knocked_pins)

        if should_reset_deck_after_roll(current_frame):
            deck.reset()
        
        input("\nPress Enter to continue...")

    # Post-game
    # ---------
    clear_terminal()
    if user_quit:
        print_quit_game_scorecard(scorecard)
    else:
        print_end_game_scorecard(scorecard)

if __name__ == "__main__":
    main()
