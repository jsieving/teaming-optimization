class Student:
    def __init__(self, name, commitment=0, interests=None, preferences=None, silver_bullets=None,
                 intr_mgmt=0, exp_mgmt=0, intr_elec=0, exp_elec=0, intr_prog=0, exp_prog=0,
                 intr_cad=0, exp_cad=0, intr_fab=0, exp_fab=0):
        
        self.name = name
        self.commitment = commitment
        self.interests = interests or set()

        self.preferences = preferences or set()
        self.silver_bullets = silver_bullets or set()

        self.intr_mgmt = intr_mgmt
        self.exp_mgmt = exp_mgmt
        self.mgmt = intr_mgmt + exp_mgmt

        self.intr_elec = intr_elec
        self.exp_elec = exp_elec
        self.elec = intr_elec + exp_elec

        self.intr_prog = intr_prog
        self.exp_prog = exp_prog
        self.prog = intr_prog + exp_elec

        self.intr_cad = intr_cad
        self.exp_cad = exp_cad
        self.cad = intr_cad + exp_cad

        self.intr_fab = intr_fab
        self.exp_fab = exp_fab
        self.fab = intr_fab + exp_fab

    def __repr__(self):
        return self.name
