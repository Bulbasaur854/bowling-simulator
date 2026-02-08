class Ball:
    def __init__(self, name, weight, rg, diff, mass_bias=0.0, grit=1500, cover_type="Solid Reactive"):
        self.name = name
        self.weight = weight
        self.rg = rg      
        self.total_diff = diff  
        self.mass_bias = mass_bias
        self.grit = grit
        self.cover_type = cover_type
        self.surface_friction_modifier = 2000 / self.grit