class Student:
    def __init__(self, name, commitment=0, interests=None, golden_bullets=None, silver_bullets=None,
                 intr_mgmt=0, exp_mgmt=0, intr_elec=0, exp_elec=0, intr_prog=0, exp_prog=0,
                 intr_cad=0, exp_cad=0, intr_fab=0, exp_fab=0):
        
        self.name = name
        self.commitment = commitment
        self.interests = interests if interests else []

        self.golden_bullets = golden_bullets if golden_bullets else []
        self.silver_bullets = silver_bullets if silver_bullets else []

        self.intr_mgmt = intr_mgmt
        self.exp_mgmt = exp_mgmt

        self.intr_elec = intr_elec
        self.exp_elec = exp_elec

        self.intr_prog = intr_prog
        self.exp_prog = exp_prog

        self.intr_cad = intr_cad
        self.exp_cad = exp_cad

        self.intr_fab = intr_fab
        self.exp_fab = exp_fab
