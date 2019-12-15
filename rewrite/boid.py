import arcade

from rewrite import consts
from rewrite.rules import rule_functions


class BaseBoid:

    SIZE = 4
    COLOR = arcade.color.RED
    MAX_SPEED = 0.2
    SEPARATION_DISTANCES = {}
    HUNT_DISTANCES = {}

    def __init__(self, x, y, dx, dy, rules):
        self.x = x
        self.dx = dx
        self._dx = 0
        self.y = y
        self.dy = dy
        self._dy = 0
        self.rules = rules

    def __repr__(self):
        return f'Boid({self.x}, {self.y})'

    def draw(self, dt: int, boids):
        self.prepare_move(boids)
        self.move(dt)
        arcade.draw_circle_filled(
            self.x,
            self.y,
            self.SIZE,
            self.COLOR,
        )

    def prepare_move(self, boids):
        dx, dy = 0, 0
        for (boid_type, rules_dict) in self.rules.items():
            for (r, w) in rules_dict.items():
                rdx = 0
                rdy = 0

                rx, ry = rule_functions[r](self, boids[boid_type], w)
                rdx += rx
                rdy += ry

                dx += rdx/(len(boids[boid_type]) or 1)
                dy += rdy/(len(boids[boid_type]) or 1)

        self._dx = dx
        self._dy = dy

    def move(self, dt: int):

        # limit speed
        spd = ((self._dx ** 2) + (self._dy ** 2)) ** 0.5
        if spd > self.MAX_SPEED:
            self._dx /= spd / self.MAX_SPEED
            self._dy /= spd / self.MAX_SPEED

        self.x += self._dx / dt
        self.y += self._dy / dt
        self.dx = self._dx
        self.dy = self._dy
        self._dx = 0
        self._dy = 0


class Sheep(BaseBoid):
    COLOR = arcade.color.WHITE
    MAX_SPEED = 0.14

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SEPARATION_DISTANCES = {
            Sheep: (Sheep.SIZE * 3, Sheep.SIZE * 3),
            Dog: (Dog.SIZE * 2, Dog.SIZE * 2),
            Wolf: (50, 100)
        }


class Wolf(BaseBoid):
    COLOR = arcade.color.BLACK
    MAX_SPEED = 0.22

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.SEPARATION_DISTANCES = {
            Wolf: (20, 60),
            Dog: (50, 70),
        }

        self.HUNT_DISTANCES = {
            Sheep: 400,
        }


class Dog(BaseBoid):
    COLOR = arcade.color.BLUE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.SEPARATION_DISTANCES = {
            Sheep: (Sheep.SIZE * 3, Sheep.SIZE * 3),
            Dog: (Dog.SIZE * 3, Dog.SIZE * 3),
            # Wolf: (100, 400)
        }

        self.HUNT_DISTANCES = {
            Wolf: 200
        }
