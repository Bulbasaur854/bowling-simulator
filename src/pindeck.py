import math

class Pin:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.is_standing = True

class PinDeck:
    def __init__(self):
        # Pins setup
        # X-coordinates (width): 12 inches apart = ~11.25 boards (5.625 offset per pin)
        # Y-coordinates (depth): Each row is separated by ~10.4 inches (0.86 feet)    
        row_0 = 60.00
        row_1 = 60.86
        row_2 = 61.73
        row_3 = 62.60
        self.pins = [
            Pin(1, 20.0, row_0),
            
            Pin(2, 25.6, row_1),
            Pin(3, 14.4, row_1),
            
            Pin(4, 31.2, row_2),
            Pin(5, 20.0, row_2),
            Pin(6, 8.8,  row_2),
            
            Pin(7, 36.8, row_3),
            Pin(8, 25.6, row_3),
            Pin(9, 14.4, row_3),
            Pin(10, 3.2, row_3)
        ]
        self.BOARD_WIDTH_FT = (41.5 / 39) / 12 # ~0.088 feet
        # Collision sizes converted to boards
        self.BALL_RADIUS = 4.0 # 8.5 inch diameter / 2 = 4.25 inches (~4 boards)
        self.PIN_RADIUS = 2.2 # 4.75 inch belly / 2 = 2.375 inches (~2.2 boards)
        self.HIT_THRESHOLD = self.BALL_RADIUS + self.PIN_RADIUS # ~6.2 boards

    def process_ball_impact(self, impact_board, entry_angle):
        """
        Pushes the ball through the 3-foot pin deck to see which pins it directly hits.
        """
        print("="*55)
        print(f"🎳 PIN DECK IMPACT 🎳")
        print("="*55)
        print(f" Ball entered at Board {impact_board:.2f} | Angle: {entry_angle:.2f}°\n")

        if impact_board == -1:
            print(" ➖ GUTTER... ➖")
            return

        ball_x = impact_board
        ball_y = 60.0
        current_angle = entry_angle
        hit_log = []
        step_size_ft = 0.1

        while ball_y <= 63.0:
            angle_rad = math.radians(current_angle)

            for pin in self.pins:
                if not pin.is_standing:
                    continue

                # Is the ball at the y coord as this level of pins?
                y_dist_ft = abs(ball_y - pin.y)
                if y_dist_ft < 0.2:
                    x_dist_board = ball_x - pin.x # horizontal distance in boards

                    # Collision check
                    if abs(x_dist_board) <= self.HIT_THRESHOLD:
                        pin.is_standing = False

                        # Get which side the ball hit the pin
                        offset = round(x_dist_board, 2)
                        hit_type = "Head-on"
                        if offset < -1.0: hit_type = "Right side"
                        elif offset > 1.0: hit_type = "Left side"

                        hit_log.append(f" Hit Pin {pin.id:2d} | {hit_type:10s} | Offset: {offset:.2f} boards")

                        # Trigger the dmonio effect
                        self.cast_pin_ray(pin, offset, hit_log)

                        # Ball deflection
                        deflection = offset * 0.4
                        current_angle += deflection
            
            # Progress ball on x and y
            lateral_ft = math.tan(angle_rad) * step_size_ft
            ball_x += lateral_ft / self.BOARD_WIDTH_FT
            ball_y += step_size_ft
        
        return hit_log

    def cast_pin_ray(self, origin_pin, impact_offset, hit_log):
        """
        Simulates a pin flying through the deck after being hit.
        Uses recursion to trigger domino effects.
        """
        # Calculate flight path (Lateral drift in boards per foot)
        # If offset is negative (hit on the right), the pin flies left (positive drift)
        bounce_factor = 0.85 # Tuning multiplier for how sharply pins bounce
        drift_rate = -impact_offset * bounce_factor 
        
        flying_x = origin_pin.x
        flying_y = origin_pin.y
        step_size_ft = 0.1
                
        pin_hit_threshold = self.PIN_RADIUS * 2 # pin hitting a pin uses PIN_RADIUS * 2 (approx 4.4 boards)
        
        # Raycast backward through the deck
        while flying_y <= 64.0:
            flying_y += step_size_ft
            flying_x += drift_rate * step_size_ft
            
            for target_pin in self.pins:
                if not target_pin.is_standing:
                    continue
                
                # Check if the flying pin crosses the depth (Y) of a standing pin
                if abs(flying_y - target_pin.y) < 0.2:
                                        
                    dist_x = flying_x - target_pin.x # check horizontal collision (X)
                    
                    if abs(dist_x) <= pin_hit_threshold:
                        target_pin.is_standing = False
                        
                        hit_type = "Head-on"
                        if dist_x < -0.5: hit_type = "Right side"
                        elif dist_x > 0.5: hit_type = "Left side"
                        
                        hit_log.append(f"  -> Pin {origin_pin.id:2d} took out Pin {target_pin.id:2d} | {hit_type:10s} | Offset: {dist_x:.2f}")
                                                
                        self.cast_pin_ray(target_pin, dist_x, hit_log) # RECURSION: the target pin now becomes a flying pin                        
                        
                        return