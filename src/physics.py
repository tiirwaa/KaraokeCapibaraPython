import numpy as np

class Physics:
    def __init__(self, width, height, scale=2):
        self.width = width
        self.height = height
        self.scale = scale
        self.gravity = np.array([0.0, 0.5])
        self.velocity = np.array([0.0, 0.0])
        self.position = np.array([width // 2, height // 2 + 200], dtype=float)
        self.body_h = 220 * scale
        self.body_w = 140 * scale
        self.floor_height = 140
        self.max_center_y = height - self.floor_height - (self.body_h / 2) + 30
        self.side_margin = int(self.body_w / 2 + 20)

    def update(self, dt):
        self.velocity += self.gravity * dt
        self.position += self.velocity * dt

        if self.position[1] >= self.max_center_y:
            self.position[1] = self.max_center_y
            self.velocity[1] *= -0.8

        if self.position[0] <= self.side_margin or self.position[0] >= self.width - self.side_margin:
            self.velocity[0] *= -1

    def is_on_ground(self):
        return self.position[1] >= self.max_center_y