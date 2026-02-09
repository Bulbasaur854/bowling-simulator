import numpy as np

class PhysicsEngine:
    def __init__(self, lane):
        self.lane = lane

    def simulate_shot(self, ball, shot_params):
        """
        Simulates the shot according to given shot_params.
        Assuming ball is thrown in a straight line to board_at_arrows.

        ball: Ball object for current throw
        shot_params: Comes from bowler.throw_ball()
        """
        
        
