# Bowling Simulator

Terminal-based 10-frame bowling simulation game in Python.

You choose a bowler, pick balls, aim each shot, and the game simulates:
- lane path/hook behavior
- pin impact + simple domino pin action
- live bowling scorecard (including 10th-frame bonus logic)

## Requirements

- Python 3.14+
- `uv` package manager

## Play The Release EXE (Windows)

A prebuilt executable is published in GitHub Releases.

Steps:
1. Go to **Releases**.
2. Download the latest `bowling-sim.exe` asset.
3. Run the downloaded file (double-click in File Explorer).

If Windows SmartScreen appears, click **More info** -> **Run anyway**.

## Run Manually (Source)

Download the source files and then:

```bash
uv sync
uv run python main.py
```

## Controls

At the pre-shot prompt:
- `T`: throw
- `C`: change to another strike ball
- `S`: switch to your bowler's spare ball
- `Q`: quit game early

During shot setup:
- Enter `Starting Position` and `Aiming Target` as board numbers (`1-39`).
- Invalid numeric input is handled and reprompted.