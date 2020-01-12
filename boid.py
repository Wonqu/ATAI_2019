import arcade


class BaseBoid:
    SIZE = 4
    COLOR = arcade.color.RED
    MAX_SPEED = 30
    SEPARATION_DISTANCES = {}
    HUNT_DISTANCES = {}
    ALIVE = True
    DEAD = False
    KILL_DIST = 5

    def __init__(self, idx, checkpoints):
        self.idx = idx
        self.checkpoints = checkpoints
        self.checkpoint_idx = 0
        if checkpoints:
            self._last_checkpoint = checkpoints[0]
        else:
            self._last_checkpoint = (0, 0)
        self.alive = self.ALIVE

    def __repr__(self):
        return f'{self.__class__.__name__}[{self.idx}]'

    def kill_dist(self, other):
        return -1

    @property
    def checkpoint(self):
        if self.checkpoints:
            return self.checkpoints[self.checkpoint_idx]
        return self._last_checkpoint

    def next_checkpoint(self):
        if self.checkpoint_idx < len(self.checkpoints) - 1:
            self.checkpoint_idx += 1
            self._last_checkpoint = self.checkpoints[self.checkpoint_idx]
        else:
            self.checkpoints = []
            self.checkpoint_idx = 0

    def kill(self):
        self.alive = self.DEAD


class Sheep(BaseBoid):
    COLOR = arcade.color.WHITE
    MAX_SPEED = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SEPARATION_DISTANCES = {
            Sheep: Sheep.SIZE * 5,
            Dog: Dog.SIZE * 5,
            Wolf: 160
        }


class Wolf(BaseBoid):
    COLOR = arcade.color.BLACK
    MAX_SPEED = 3.4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.SEPARATION_DISTANCES = {
            Wolf: 24,
            Dog: 80
        }

        self.HUNT_DISTANCES = {
            Sheep: 200,
        }

    def kill_dist(self, other):
        return self.KILL_DIST if isinstance(other, Sheep) else super().kill_dist(other)


class Dog(BaseBoid):
    COLOR = arcade.color.BLUE
    MAX_SPEED = 3.2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.SEPARATION_DISTANCES = {
            Sheep: Sheep.SIZE * 5,
            Dog: Dog.SIZE * 5,
        }

        self.HUNT_DISTANCES = {
            Wolf: 200
        }

    def kill_dist(self, other):
        return self.KILL_DIST if isinstance(other, Wolf) else super().kill_dist(other)


class Obstacle(BaseBoid):
    COLOR = arcade.color.GRAY
