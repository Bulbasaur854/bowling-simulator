from src.lane import Lane

checks = [
        ("Foul Line (Heavy Oil)", 20, 0),
        ("Foul Line (Dry Outside)", 5, 0),
        ("Backend (Dry Backend)", 20, 50),
        ("Pin Deck (Always Dry)", 20, 60),
        ("Foul Line (Board 1)", 1, 0),
        ("Foul Line (Board 39)", 39, 0),
        ("Midlane (20ft)", 20, 20),
        ("Midlane (35ft)", 20, 35),
        ("Clamped Board Low", -5, 10),
        ("Clamped Board High", 50, 10),
        ("Clamped Distance Low", 20, -5),
    ]

def main():
    lane = Lane()

    for name, board, ft in checks:
        print(f"Board {board:02d} | {ft:02d}ft | {lane.get_friction(board, ft)}")

if __name__ == "__main__":
    main()
