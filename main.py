import itertools
from collections import defaultdict

import numpy as np

import arcade

import consts
from boid import Sheep, Dog, Wolf
from rules import rule_functions
from simulations import simulation, sim_data_1

SCREEN_WIDTH = consts.WIDTH
SCREEN_HEIGHT = consts.HEIGHT
SCREEN_TITLE = "Boid Populations"

state = {}


def draw(_delta_time):
    """
    Use this function to draw everything to the screen.
    """

    # Start the render. This must happen before any drawing
    # commands. We do NOT need an stop render command.
    arcade.start_render()

    update_coords()

    global state
    for boid in state['objects']:
        arcade.draw_circle_filled(
            state['boids_xy'][boid.idx].real,
            state['boids_xy'][boid.idx].imag,
            boid.SIZE,
            boid.COLOR,
        )

    for obstacle in state['obstacles']:
        arcade.draw_circle_outline(
            state['obstacles_xy'][obstacle.idx].real,
            state['obstacles_xy'][obstacle.idx].imag,
            obstacle.SIZE,
            obstacle.COLOR,
        )


def update_coords():
    global state

    for rule, fun in rule_functions.items():
        res = fun(
            state['boids_dxy'],
            state['boids_dist'],
            state['boids_towards'],
            state['max_dist'][rule],
            state['obstacles_dist'],
            state['obstacles_towards'],
            state['checkpoint_towards'],
            state['wall_dist'],
            state['wall_towards'],
        )
        res = (state['weights'][rule] * np.identity(state['weights'][rule].shape[0])) @ np.nan_to_num(res)
        state['boids_dxy'] += res

    state['boids_dxy'] = np.nan_to_num(state['boids_dxy'] / np.absolute(state['boids_dxy']))

    state['boids_xy'] += state['boids_dxy'] * state['speed']
    state['boids_towards'] = state['boids_xy'][..., np.newaxis] - state['boids_xy']
    MA = np.tile(state['boids_xy'][:, np.newaxis], state['boids_xy'].size)
    state['boids_dist'] = abs(MA - MA.T)
    state['obstacles_towards'] = np.array(state['boids_xy'][..., np.newaxis] - state['obstacles_xy'])
    state['obstacles_dist'] = abs(state['obstacles_towards'])
    state['checkpoint_xy'] = np.array([complex(*b.checkpoint) for b in state['objects']])
    state['checkpoint_towards'] = np.array(state['boids_xy'] - state['checkpoint_xy'])
    state['wall_dist'] = np.array([
        [xy.real, xy.imag, consts.WIDTH - xy.real, consts.HEIGHT - xy.imag]
        for xy in state['boids_xy']
    ])


def main():
    sim = simulation(sim_data_1)

    boids_xy = np.array([np.complex(x, y) for (x, y) in sim['boids_xy']])
    boids_dxy = np.array([np.complex(0, 0) for _ in sim['boids_xy']])
    boids_towards = boids_xy[..., np.newaxis] - boids_xy
    MA = np.tile(boids_xy[:, np.newaxis], boids_xy.size)
    boids_dist = abs(MA - MA.T)
    obstacles_xy = np.array([complex(x, y) for (x, y) in sim['obstacles_xy']])
    obstacles_towards = np.array(boids_xy[..., np.newaxis] - obstacles_xy)
    obstacles_dist = abs(obstacles_towards)
    checkpoint_xy = np.array(
        [
            complex(*b.checkpoint)
            for b in itertools.chain(
                sim['boids'][Sheep]['objects'],
                sim['boids'][Dog]['objects'],
                sim['boids'][Wolf]['objects'],
            )
        ]
    )
    checkpoint_towards = boids_xy - checkpoint_xy
    wall_dist = np.array([
        [xy.real, xy.imag, consts.WIDTH - xy.real, consts.HEIGHT - xy.imag]
        for xy in boids_xy
    ])
    wall_towards = np.array([
        [complex(-1, 0), complex(0, -1), complex(1, 0), complex(0, 1)]
        for _ in boids_xy
    ])

    global state
    state = {
        'objects': [
            b for b in
            itertools.chain(
                sim['boids'][Sheep]['objects'],
                sim['boids'][Dog]['objects'],
                sim['boids'][Wolf]['objects'],
            )
        ],
        'boids_xy': boids_xy,
        'boids_dxy': boids_dxy,
        'boids_towards': boids_towards,
        'boids_dist': boids_dist,
        'obstacles': sim['obstacles'],
        'obstacles_xy': obstacles_xy,
        'obstacles_towards': obstacles_towards,
        'obstacles_dist': obstacles_dist,
        'checkpoint_xy': checkpoint_xy,
        'checkpoint_towards': checkpoint_towards,
        'wall_dist': wall_dist,
        'wall_towards': wall_towards,
        'max_dist': defaultdict(lambda: np.array([[0] * len(boids_xy)]), **{
            consts.WALLS: np.array([
                consts.WALL_DISTANCE
                for _ in range(len(boids_xy))
            ]),
            consts.OBSTACLES: np.array([
                consts.OBSTACLE_DISTANCE
                for _ in range(len(boids_xy))
            ]),
            consts.SEPARATION: np.array(
                [[
                    x for x in
                    itertools.chain(
                        [Sheep(100, []).SEPARATION_DISTANCES.get(Sheep, 0)] * len(sim['boids'][Sheep]['objects']),
                        [Sheep(100, []).SEPARATION_DISTANCES.get(Dog, 0)] * len(sim['boids'][Dog]['objects']),
                        [Sheep(100, []).SEPARATION_DISTANCES.get(Wolf, 0)] * len(sim['boids'][Wolf]['objects']),
                    )
                ]] * len(sim['boids'][Sheep]['objects']) + [[
                    x for x in
                    itertools.chain(
                        [Dog(100, []).SEPARATION_DISTANCES.get(Sheep, 0)] * len(sim['boids'][Sheep]['objects']),
                        [Dog(100, []).SEPARATION_DISTANCES.get(Dog, 0)] * len(sim['boids'][Dog]['objects']),
                        [Dog(100, []).SEPARATION_DISTANCES.get(Wolf, 0)] * len(sim['boids'][Wolf]['objects']),
                    )
                ]] * len(sim['boids'][Dog]['objects']) + [[
                    x for x in
                    itertools.chain(
                        [Wolf(100, []).SEPARATION_DISTANCES.get(Sheep, 0)] * len(sim['boids'][Sheep]['objects']),
                        [Wolf(100, []).SEPARATION_DISTANCES.get(Dog, 0)] * len(sim['boids'][Dog]['objects']),
                        [Wolf(100, []).SEPARATION_DISTANCES.get(Wolf, 0)] * len(sim['boids'][Wolf]['objects']),
                    )
                ]] * len(sim['boids'][Wolf]['objects'])
            ),
            consts.ALIGNMENT: np.array(
                [[
                    x for x in
                    itertools.chain(
                        [64] * len(sim['boids'][Sheep]['objects']),
                        [0] * len(sim['boids'][Dog]['objects']),
                        [0] * len(sim['boids'][Wolf]['objects']),
                    )
                ]] * len(sim['boids'][Sheep]['objects']) + [[
                    x for x in
                    itertools.chain(
                        [0] * len(sim['boids'][Sheep]['objects']),
                        [0] * len(sim['boids'][Dog]['objects']),
                        [0] * len(sim['boids'][Wolf]['objects']),
                    )
                ]] * len(sim['boids'][Dog]['objects']) + [[
                    x for x in
                    itertools.chain(
                        [0] * len(sim['boids'][Sheep]['objects']),
                        [0] * len(sim['boids'][Dog]['objects']),
                        [0] * len(sim['boids'][Wolf]['objects']),
                    )
                ]] * len(sim['boids'][Wolf]['objects'])
            ),
            consts.COHESION: np.array(
                [[
                    x for x in
                    itertools.chain(
                        [64] * len(sim['boids'][Sheep]['objects']),
                        [64] * len(sim['boids'][Dog]['objects']),
                        [0] * len(sim['boids'][Wolf]['objects']),
                    )
                ]] * len(sim['boids'][Sheep]['objects']) + [[
                    x for x in
                    itertools.chain(
                        [64] * len(sim['boids'][Sheep]['objects']),
                        [64] * len(sim['boids'][Dog]['objects']),
                        [0] * len(sim['boids'][Wolf]['objects']),
                    )
                ]] * len(sim['boids'][Dog]['objects']) + [[
                    x for x in
                    itertools.chain(
                        [0] * len(sim['boids'][Sheep]['objects']),
                        [0] * len(sim['boids'][Dog]['objects']),
                        [0] * len(sim['boids'][Wolf]['objects']),
                    )
                ]] * len(sim['boids'][Wolf]['objects'])
            ),
            consts.HUNT: np.array(
                [[
                    x for x in
                    itertools.chain(
                        [0] * len(sim['boids'][Sheep]['objects']),
                        [0] * len(sim['boids'][Dog]['objects']),
                        [0] * len(sim['boids'][Wolf]['objects']),
                    )
                ]] * len(sim['boids'][Sheep]['objects']) + [[
                    x for x in
                    itertools.chain(
                        [0] * len(sim['boids'][Sheep]['objects']),
                        [0] * len(sim['boids'][Dog]['objects']),
                        [160] * len(sim['boids'][Wolf]['objects']),
                    )
                ]] * len(sim['boids'][Dog]['objects']) + [[
                    x for x in
                    itertools.chain(
                        [160] * len(sim['boids'][Sheep]['objects']),
                        [0] * len(sim['boids'][Dog]['objects']),
                        [0] * len(sim['boids'][Wolf]['objects']),
                    )
                ]] * len(sim['boids'][Wolf]['objects'])
            ),
        }),
        'weights': {
            consts.ALIGNMENT: np.array(
                [[
                    x for x in
                    itertools.chain(
                        [sim['boids'][Sheep]['rules'][Sheep][consts.ALIGNMENT]] * len(sim['boids'][Sheep]['objects']),
                        [0] * len(sim['boids'][Dog]['objects']),
                        [0] * len(sim['boids'][Wolf]['objects']),
                    )
                ]] * len(sim['boids'][Sheep]['objects']) + [
                    [0] * len(sim['boids_xy'])
                ] * (len(sim['boids'][Dog]['objects']) + len(sim['boids'][Wolf]['objects']))
            ),
            consts.COHESION: np.array(
                [[
                    x for x in
                    itertools.chain(
                        [sim['boids'][Sheep]['rules'][Sheep][consts.COHESION]] * len(sim['boids'][Sheep]['objects']),
                        [sim['boids'][Sheep]['rules'][Dog][consts.COHESION]] * len(sim['boids'][Dog]['objects']),
                        [0] * len(sim['boids'][Wolf]['objects']),
                    )
                ]] * len(sim['boids'][Sheep]['objects']) + [[
                    x for x in
                    itertools.chain(
                        [sim['boids'][Dog]['rules'][Sheep][consts.COHESION]] * len(sim['boids'][Sheep]['objects']),
                        [0] * len(sim['boids'][Dog]['objects']),
                        [0] * len(sim['boids'][Wolf]['objects']),
                    )
                ]] * len(sim['boids'][Dog]['objects']) + [
                    [0] * len(sim['boids_xy'])
                ] * len(sim['boids'][Wolf]['objects'])
            ),
            consts.SEPARATION: np.array(
                [[
                    x for x in
                    itertools.chain(
                        [sim['boids'][Sheep]['rules'][Sheep][consts.SEPARATION]] * len(sim['boids'][Sheep]['objects']),
                        [sim['boids'][Sheep]['rules'][Dog][consts.SEPARATION]] * len(sim['boids'][Dog]['objects']),
                        [sim['boids'][Sheep]['rules'][Wolf][consts.SEPARATION]] * len(sim['boids'][Wolf]['objects']),
                    )
                ]] * len(sim['boids'][Sheep]['objects']) + [[
                    x for x in
                    itertools.chain(
                        [sim['boids'][Dog]['rules'][Sheep][consts.SEPARATION]] * len(sim['boids'][Sheep]['objects']),
                        [sim['boids'][Dog]['rules'][Dog][consts.SEPARATION]] * len(sim['boids'][Dog]['objects']),
                        [0] * len(sim['boids'][Wolf]['objects']),
                    )
                ]] * len(sim['boids'][Dog]['objects']) + [[
                    x for x in
                    itertools.chain(
                        [0] * len(sim['boids'][Sheep]['objects']),
                        [sim['boids'][Wolf]['rules'][Dog][consts.SEPARATION]] * len(sim['boids'][Dog]['objects']),
                        [sim['boids'][Wolf]['rules'][Wolf][consts.SEPARATION]] * len(sim['boids'][Wolf]['objects']),
                    )
                ]] * len(sim['boids'][Wolf]['objects'])
            ),
            consts.WALLS: np.identity(boids_xy.shape[0]) * np.array([
                x for x in
                itertools.chain(
                    [sim['boids'][Sheep]['rules'][Sheep][consts.WALLS]] * len(sim['boids'][Sheep]['objects']),
                    [sim['boids'][Dog]['rules'][Dog][consts.WALLS]] * len(sim['boids'][Dog]['objects']),
                    [sim['boids'][Wolf]['rules'][Wolf][consts.WALLS]] * len(sim['boids'][Wolf]['objects']),
                )
            ]),
            consts.OBSTACLES: np.identity(boids_xy.shape[0]) * np.array([
                x for x in
                itertools.chain(
                    [sim['boids'][Sheep]['rules'][Sheep][consts.OBSTACLES]] * len(sim['boids'][Sheep]['objects']),
                    [sim['boids'][Dog]['rules'][Dog][consts.OBSTACLES]] * len(sim['boids'][Dog]['objects']),
                    [sim['boids'][Wolf]['rules'][Wolf][consts.OBSTACLES]] * len(sim['boids'][Wolf]['objects']),
                )
            ]),
            consts.CHECKPOINT: np.identity(boids_xy.shape[0]) * np.array([
                x for x in
                itertools.chain(
                    [sim['boids'][Sheep]['rules'][Sheep][consts.CHECKPOINT]] * len(sim['boids'][Sheep]['objects']),
                    [sim['boids'][Dog]['rules'][Dog][consts.CHECKPOINT]] * len(sim['boids'][Dog]['objects']),
                    [0] * len(sim['boids'][Wolf]['objects']),
                )
            ]),
            consts.HUNT: np.identity(boids_xy.shape[0]) * np.array([
                x for x in
                itertools.chain(
                    [0] * len(sim['boids'][Sheep]['objects']),
                    [sim['boids'][Dog]['rules'][Wolf][consts.HUNT]] * len(sim['boids'][Dog]['objects']),
                    [sim['boids'][Wolf]['rules'][Sheep][consts.HUNT]] * len(sim['boids'][Wolf]['objects']),
                )
            ]),
            consts.MAINTENANCE: np.identity(boids_xy.shape[0]) * np.array([
                x for x in
                itertools.chain(
                    [sim['boids'][Sheep]['rules'][Sheep][consts.MAINTENANCE]] * len(sim['boids'][Sheep]['objects']),
                    [sim['boids'][Dog]['rules'][Dog][consts.MAINTENANCE]] * len(sim['boids'][Dog]['objects']),
                    [sim['boids'][Wolf]['rules'][Wolf][consts.MAINTENANCE]] * len(sim['boids'][Wolf]['objects']),
                )
            ]),
        },
        'speed': np.array([
            x for x in
            itertools.chain(
                [Sheep.MAX_SPEED] * len(sim['boids'][Sheep]['objects']),
                [Dog.MAX_SPEED] * len(sim['boids'][Dog]['objects']),
                [Wolf.MAX_SPEED] * len(sim['boids'][Wolf]['objects']),
            )
        ])
    }

    # Open up our window
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_background_color(arcade.color.GREEN)

    # Tell the computer to call the draw command at the specified interval.
    arcade.schedule(draw, 1 / 60)

    # Run the program
    arcade.run()

    # When done running the program, close the window.
    # arcade.close_window()


if __name__ == "__main__":
    main()
