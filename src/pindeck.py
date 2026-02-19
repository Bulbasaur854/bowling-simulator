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
        self.HIT_THRESHOLD = self.BALL_RADIUS - self.PIN_RADIUS # ~6.2 boards

    def process_ball_impact(self, impact_board, entry_angle):
        """
        Pushes the ball through the 3-foot pin deck to see which pins it directly hits.
        """
        print(f"\n🎳 --- PIN DECK IMPACT --- 🎳")
        print(f" Ball entered at Board {impact_board:.2f} | Angle: {entry_angle:.2f}°\n")

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

                        # Ball deflection
                        deflection = offset * 0.4
                        current_angle += deflection
            
            # Progress ball on x and y
            lateral_ft = math.tan(angle_rad) * step_size_ft
            ball_x += lateral_ft / self.BOARD_WIDTH_FT
            ball_y += step_size_ft
        
        return hit_log