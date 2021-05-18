import time


class Animator:
    def __init__(self):
        self.current_state = "enter"
        self.current_frame = 0
        self.playing = True
        self.frames = []
        self.triggers = []
        self.animations = {}
        self.transitions = []
        self._last_frame = time.time()

    def tick(self):
        if self.current_state == "enter":
            for t in self.transitions:
                if t["start"] == "enter":
                    self.current_state = t["end"]
                    self.current_frame = self.animations[self.current_state]["from"]
                    return self.frames[self.current_frame]
            return None
        else:
            anime = self.animations[self.current_state]
            frame_count = anime["to"] - anime["from"] + 1
            if time.time() - self._last_frame > self.animations[self.current_state]["interval"]:
                self._last_frame = time.time()
                if self.playing:
                    self.current_frame += 1
                    if self.current_frame == self.animations[self.current_state]["from"] + frame_count:
                        self.current_frame = self.animations[self.current_state]["from"]
                else:
                    self.current_frame = self.animations[self.current_state]["from"]
            return self.frames[self.current_frame]

    def trigger(self, name):
        if name in self.triggers:
            for t in self.transitions:
                if t["trigger"] == name and t["start"] == self.current_state:
                    self.current_state = t["end"]
                    self._last_frame = time.time()
                    self.current_frame = self.animations[self.current_state]["from"]
