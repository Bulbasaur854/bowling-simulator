import numpy as np

class Lane:  
  def __init__(self, name='House Pattern', length_ft=40, oil_ratio=10.0):
    self.name = name
    self.length_ft = length_ft
    self.oil_ratio = oil_ratio
    # Lane is 39 boards wide and 60 feet long devided into 0.1ft increments
    # Resolution: 39 x 600
    self.grid = np.zeros((39, 600))

    self._apply_oil_pattern()

  def _apply_oil_pattern(self):
    '''
    Creates a basic tiered oil pattern. 
    High volume in the center, tapering to dry on the outside.
    '''
    length_units = int(self.length_ft * 10)

    for y in range(length_units):
      # For each 0.1ft for the  length of the oil pattern
      # Calculate 'taper' factor to make oil thinner down the lane
      taper = 1.0 - (y / length_units) * 0.5

      for x in range(39):
        # Board indexes are 0-38
        # For each board, get the distance from the center of the lane (board 19)
        dist_from_center = abs(19 - x)

        if dist_from_center <= 5: # Middle
          oil_val = 1.0
        elif dist_from_center <= 12: # Mid-outside
          oil_val = 0.5
        else: # Outside
          oil_val = 0.1

        self.grid[x, y] = oil_val * taper

  def get_friction(self, board, distance_ft):
    """
    Returns the friction coefficient at a specific point.
    Friction is the inverse of oil volume.
    0 oil   =     1.0 friction (full hook potential)
    1.0 oil =     0.0 friction (skidding)
    
    board:        1.0 to 39.0 (float)
    distance_ft:  0.0 to 60.0 (float)
    """
    if distance_ft >= 60: return 0.0 # Pin deck is dry
    
    # Convert physical units to array indices
    x_idx = int(np.clip(board - 1, 0, 38))
    y_idx = int(np.clip(distance_ft * 10, 0, 599))
    
    oil_volume = self.grid[x_idx, y_idx]

    return 1.0 - oil_volume