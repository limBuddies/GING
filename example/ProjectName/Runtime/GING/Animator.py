class Animator:
    def __init__(self):
        self.current_state = "enter"
        self.current_frame = 0
        self.frames = []
        self.triggers = []
        self.animations = []
        self.transitions = []
