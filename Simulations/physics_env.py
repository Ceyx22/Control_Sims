import numpy as np
import threading

class physics_env:
    def __init__(self):
        self.origin = np.array([0, 0, 0])
        self.ground_level = 0
        self.update_available = False;
        self.quit = False;
        self.thread = threading.Thread(name="GUI thread", target=self.run)

    def get_thread(self):
        return self.thread

    def run(self):
        while not self.quit:
            self.detect_ground()

    def detect_ground(self, object_pos):
        if self.ground_level == object_pos[1]:
            return

