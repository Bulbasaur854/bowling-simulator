import numpy as np

class PhysicsEngine:
    def __init__(self, lane):
        self.lane = lane

    def simulate_shot(self, ball, shot_params):
        """
        Simulates the shot according to given shot_params.
        Assuming ball is thrown in a straight line to board_at_arrows.

        ball: Ball object for current throw
        shot_params: Comes from player.release_shot()
        """
        speed = shot_params["speed"]
        revs = shot_params["revs"]
        board_at_arrows = shot_params["board_at_arrows"]
        axis_rotation = shot_params["axis_rotation"]
        axis_tilt = shot_params["axis_tilt"]

        
