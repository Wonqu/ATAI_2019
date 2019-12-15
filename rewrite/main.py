import arcade
from rewrite import consts
from rewrite.boid import Sheep, Dog, Wolf

SCREEN_WIDTH = consts.WIDTH
SCREEN_HEIGHT = consts.HEIGHT
SCREEN_TITLE = "Boid Populations"

NUM_SHEEP = 40
NUM_DOGS = 1
NUM_WOLVES = 8


boids = {
    Sheep: [
        Sheep(
            arcade.random.randint(200, SCREEN_WIDTH-200),
            arcade.random.randint(200, SCREEN_HEIGHT-200),
            arcade.random.random(),
            arcade.random.random(),
            {
                Sheep: {
                    consts.MAINTENANCE: 50,
                    consts.ALIGNMENT: 2,
                    consts.COHESION: 2,
                    consts.SEPARATION: 100,
                    consts.WALLS: 10000,
                    consts.CENTER: 1,
                },
                Wolf: {
                    consts.SEPARATION: 100
                },
                Dog: {
                    consts.COHESION: 2,
                    consts.SEPARATION: 20,
                }
            }
        ) for _ in range(NUM_SHEEP)
    ],
    Dog: [
        Dog(
            arcade.random.randint(200, SCREEN_WIDTH-200),
            arcade.random.randint(200, SCREEN_HEIGHT-200),
            arcade.random.random(),
            arcade.random.random(),
            {
                Dog: {
                    consts.MAINTENANCE: 50,
                    # consts.ALIGNMENT: 2,
                    # consts.COHESION: 6,
                    consts.SEPARATION: 100,
                    consts.WALLS: 10000,
                    consts.CENTER: 2,
                },
                Wolf: {
                    consts.HUNT: 2
                },
                Sheep: {
                    consts.COHESION: 2
                }
            }
        ) for _ in range(NUM_DOGS)
    ],
    Wolf: [
        Wolf(
            arcade.random.randint(200, SCREEN_WIDTH-200),
            arcade.random.randint(200, SCREEN_HEIGHT-200),
            arcade.random.random(),
            arcade.random.random(),
            {
                Wolf: {
                    consts.MAINTENANCE: 50,
                    # consts.ALIGNMENT: 2,
                    # consts.COHESION: 1,
                    consts.SEPARATION: 50,
                    consts.WALLS: 10000,
                    consts.CENTER: 1,
                },
                Sheep: {
                    consts.HUNT: 10
                },
                Dog: {
                    consts.SEPARATION: 200
                }
            }
        ) for _ in range(NUM_WOLVES)
    ],
}


def draw(_delta_time):
    """
    Use this function to draw everything to the screen.
    """

    # Start the render. This must happen before any drawing
    # commands. We do NOT need an stop render command.
    arcade.start_render()

    for boid_type, boid_list in boids.items():
        for boid in boid_list:
            boid.draw(_delta_time, boids)

    if len(boids[Sheep]) == 0:
        print('Wolves win!')
        arcade.unschedule(draw)
        arcade.close_window()
    elif len(boids[Wolf]) == 0:
        print('Dogs and Sheep win!')
        arcade.unschedule(draw)
        arcade.close_window()


def main():
    # Open up our window
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_background_color(arcade.color.GREEN)

    # Tell the computer to call the draw command at the specified interval.
    arcade.schedule(draw, 1 / 30)

    # Run the program
    arcade.run()

    # When done running the program, close the window.
    # arcade.close_window()


if __name__ == "__main__":
    main()
