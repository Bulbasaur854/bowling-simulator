import numpy as np

class PhysicsEngine:
    def __init__(self, lane):
        self.lane = lane

    def simulate_shot(self, ball, shot_params):
        """
        shot_params comes from player.release_shot()
        {
            "speed": 17.0, (mph)
            "revs": 450,
            "board_at_arrows": 15.0,
            "axis_rotation": 55,
            ...
        }
        """
        
        # 1. SETUP INITIAL VECTOR
        # We need the Laydown point (Foul Line). 
        # For simplicity, let's assume players drift to align with their target.
        # If aiming at board 15 at 15ft, and walking straight, laydown might be ~20.
        # Let's calculate a "Launch Angle" based on a standard laydown for now.
        
        target_at_15ft = shot_params["board_at_arrows"]
        # Basic geometry: Assuming a drift of ~5-7 boards is normal. 
        # Let's derive Laydown from Target for now to ensure a valid line.
        # A standard "Track" shot might launch from board 22 to hit board 15.
        laydown_board = target_at_15ft + 5 # Simplified launch vector
        
        current_board = laydown_board
        current_speed_mph = shot_params["speed"]
        
        # Convert Speed to Feet Per Second (1 mph = 1.467 fps)
        velocity_fps = current_speed_mph * 1.467
        
        # Lateral Velocity (drift left/right)
        # Calculated from the vector (Laydown -> Target)
        # Delta Boards over 15ft
        slope = (target_at_15ft - laydown_board) / 15.0 
        lateral_velocity = slope * velocity_fps # Boards per second movement
        
        # 2. SIMULATION LOOP (0ft to 60ft)
        step_size_ft = 0.5
        steps = int(60 / step_size_ft)
        
        path = [] # Store path for visualization later [(x, y), ...]
        
        for step in range(steps):
            distance = step * step_size_ft
            
            # A. GET FRICTION
            # Get friction at current location
            friction = self.lane.get_friction(current_board, distance)
            
            # B. CALCULATE HOOK PHYSICS
            # This is the "Engine". 
            # If Friction > 0, the ball starts converting "Revs" into "Lateral Motion"
            if friction > 0:
                # Hook Power Formula (Simplified):
                # Revs * Differential * Friction * Coverstock
                hook_power = (shot_params["revs"] / 100) * ball.total_diff * 50
                
                # Apply Coverstock & Lane Friction
                # If Mass Bias exists, it adds "snap" at high friction
                bias_bonus = 1.0 + (ball.mass_bias * 10 if friction > 0.8 else 0)
                
                acceleration = hook_power * friction * ball.get_surface_friction_modifier() * bias_bonus
                
                # Right-hander hooks LEFT (Negative board direction)
                # We subtract from lateral_velocity (making it more negative/leftward)
                lateral_velocity -= (acceleration * 0.05) # Scaling factor for time step
            
            # C. UPDATE POSITION
            # Move the ball sideways based on current lateral velocity
            # We divide by velocity_fps because we are stepping by distance, not time.
            # Time for this step = step_size / velocity
            time_step = step_size_ft / velocity_fps
            current_board += lateral_velocity * time_step
            
            # Record Path
            path.append((distance, current_board))
            
            # Gutter Check
            if current_board < 1 or current_board > 39:
                return {"impact_board": -1, "entry_angle": 0, "path": path} # Gutter

        # 3. CALCULATE ENTRY ANGLE
        # Angle is based on the change in boards over the last few feet
        # Basic Trig: atan(delta_boards / delta_distance)
        last_pos = path[-1][1]
        prev_pos = path[-5][1] # Look back 2.5 ft
        delta_x = (prev_pos - last_pos) * (1.05 / 12) # Convert boards to feet width
        delta_y = 2.5 # feet
        entry_angle = np.degrees(np.arctan(delta_x / delta_y))

        return {
            "impact_board": round(current_board, 2),
            "entry_angle": round(entry_angle, 2),
            "path": path
        }