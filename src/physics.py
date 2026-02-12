import math
import numpy as np

class PhysicsEngine:
    def __init__(self, lane):
        self.lane = lane

        self.BOARD_WIDTH_FT = (41.5 / 39) / 12  # ~0.088 feet
        self.TIME_STEP = 0.01                   # 10ms per frame
        self.GRAVITY_FT = 32.174                # gravity in ft/s^2

    def simulate_shot(self, ball, shot_params):
        """
        Simulates the shot according to given shot_params.
        Assuming ball is thrown in a straight line to board_at_arrows.

        ball: Ball object for current throw
        shot_params: Comes from bowler.throw_ball()
        """
        print("Simulating Shot")

        start_x, start_y = shot_params["laydown_point"]
        target_x, target_y = shot_params["actual_target"]
        print(f" start: ({start_x:.2f}, {start_y:.2f})\n target: ({target_x:.2f}, {target_y:.2f})")

        # Calculate launch vector
        delta_x_ft = (target_x - start_x) * self.BOARD_WIDTH_FT
        delta_y_ft = target_y - start_y
        launch_angle_rad = math.atan2(delta_x_ft, delta_y_ft)
        print(f" launch angle: {launch_angle_rad:.2f}")

        # Get the velocity 
        speed_ft_per_sec = shot_params["launch_speed"] * 1.467 # mph -> feet per second 
        vel_x = speed_ft_per_sec * math.sin(launch_angle_rad)
        vel_y = speed_ft_per_sec * math.cos(launch_angle_rad)
        print(f" veloc: ({vel_x:.2f}, {vel_y:.2f})")

        current_x = start_x
        current_y = 0.0
        current_revs = shot_params["launch_revs"]
        current_rotation = shot_params["launch_rotation"]
        current_tilt = shot_params["launch_tilt"]
        path = []

        while current_y < 60.0:
            path.append((current_y, current_x)) # store (y, board)

            # Get lane conditions
            board_to_check = max(1.0, min(39.0, current_x))
            current_friction = self.lane.get_friction(board_to_check, current_y)
            # print(f"\ncurrent fric:\t{current_friction:.2f}")

            # Calculate hook acceleration
            # If there is friction, the ball tries to hook
            # Hook force direction is perpendicular to velocity
            # For simplicity, we push -X based on rotation
            if current_friction > 0.05:
                # Calculate hook power
                # Simplified physics modal, using this formula:
                # Accel = (Revs * Diff * Friction) * Rotation
                surface_factor = ball.surface_friction_modifier
                rotation_factor = math.sin(math.radians(current_rotation)) # convert rotation to a vector scalar
                bias_boost = 1.0 + (ball.mass_bias * 20 * current_friction) # bias boost for asymmetrical core

                hook_accel = (
                    current_revs * 
                    ball.total_diff * 
                    current_friction * 
                    surface_factor * 
                    rotation_factor * 
                    bias_boost
                    ) * 0.003
                # print(f"current hook:\t{hook_accel:.5f}")

                # Apply accelration to velocity
                # Fromula converts g-force to feet per second
                vel_x += hook_accel * self.TIME_STEP * 32.174

                # As ball hooks, it loses rotation and tilt (roll out)
                # High friction reduces rotation faster
                decay_rate = surface_factor * self.TIME_STEP * 2.0
                current_rotation = max(0, current_rotation - (decay_rate * 14))
                current_revs = max(0, current_revs - (decay_rate * 10))
                # print(f"current rota:\t{current_rotation:.5f}")
                # print(f"current revs:\t{current_revs:.5f}")

            x_movement_ft = vel_x * self.TIME_STEP
            current_x += x_movement_ft / self.BOARD_WIDTH_FT # convert velocity to boards units
            current_y += vel_y * self.TIME_STEP

            # Gutter check
            if current_x < 0.5 or current_x > 39.5:
                return {
                    "impact_board": -1, 
                    "entry_angle": 0.0, 
                    "path": path,
                    "velocity_at_impact": vel_x
                }
        
        # Calculate entry angle at 60ft and convert radians to degrees
        # Angle = arctan(v_x / v_y)
        final_angle = math.degrees(math.atan2(abs(vel_x), vel_y))

        return {
            "impact_board": round(current_x, 2),
            "entry_angle": round(final_angle, 2),
            "path": path,
            "velocity_at_impact": math.sqrt(vel_x**2 + vel_y**2)
        }

            

