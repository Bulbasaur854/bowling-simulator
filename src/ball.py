class Ball:
    def __init__(self, name, weight, rg, diff, mass_bias=0.0, grit=1500, cover_type="Solid Reactive"):
        self.name = name
        self.weight = weight
        self.rg = rg      
        self.total_diff = diff  
        self.mass_bias = mass_bias
        self.grit = grit
        self.cover_type = cover_type    

    def get_surface_friction_modifier(self):
        '''
        Lower grit (rougher) = more friction earlier.
        1500 grit is fairly aggressive compared to 4000 or Polished.
        '''
        # Baseline is 2000 grit = 1.0
        return 2000 / self.grit