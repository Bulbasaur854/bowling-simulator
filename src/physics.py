import numpy as np

class PhysicsEngine:
    def __init__(self, lane):
        self.lane = lane

    def simulate_shot(self, ball, shot_params):
        """
        Simulates a shot with given ball and player shot parameters

        ball: Ball object for current throw
        shot_params: Comes from player.release_shot()
        """
        
        return "Hello"