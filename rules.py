from typing import List

import numpy as np

import consts
from boid import BaseBoid


def alignment(
    boids_dxy: np.ndarray,
    boids_dist: np.ndarray,
    boids_towards: np.ndarray,
    max_dist: np.ndarray,
    obstacles_dist: np.ndarray,
    obstacles_towards: np.ndarray,
    checkpoint_towards: np.ndarray,
    wall_dist: np.ndarray,
    wall_towards: np.ndarray,
    objects: List[BaseBoid],
    kill_dist: np.ndarray,
) -> np.ndarray:
    which_calc = boids_dist <= max_dist.astype(int)
    result = np.multiply(
        which_calc,
        boids_dxy
    ).sum(axis=1)
    return result / np.absolute(result)


def cohesion(
    boids_dxy: np.ndarray,
    boids_dist: np.ndarray,
    boids_towards: np.ndarray,
    max_dist: np.ndarray,
    obstacles_dist: np.ndarray,
    obstacles_towards: np.ndarray,
    checkpoint_towards: np.ndarray,
    wall_dist: np.ndarray,
    wall_towards: np.ndarray,
    objects: List[BaseBoid],
    kill_dist: np.ndarray,
) -> np.ndarray:
    which_calc = (boids_dist <= max_dist.astype(int))
    result = np.multiply(
        which_calc,
        boids_towards
    ).sum(axis=1)
    result = result / np.absolute(result)
    return result


def maintenance(
    boids_dxy: np.ndarray,
    boids_dist: np.ndarray,
    boids_towards: np.ndarray,
    max_dist: np.ndarray,
    obstacles_dist: np.ndarray,
    obstacles_towards: np.ndarray,
    checkpoint_towards: np.ndarray,
    wall_dist: np.ndarray,
    wall_towards: np.ndarray,
    objects: List[BaseBoid],
    kill_dist: np.ndarray,
) -> np.ndarray:
    return boids_dxy / np.absolute(boids_dxy)


def obstacles(
    boids_dxy: np.ndarray,
    boids_dist: np.ndarray,
    boids_towards: np.ndarray,
    max_dist: np.ndarray,
    obstacles_dist: np.ndarray,
    obstacles_towards: np.ndarray,
    checkpoint_towards: np.ndarray,
    wall_dist: np.ndarray,
    wall_towards: np.ndarray,
    objects: List[BaseBoid],
    kill_dist: np.ndarray,
) -> np.ndarray:
    max_dist = np.column_stack(((max_dist,) * obstacles_dist.shape[1]))
    which_calc = (obstacles_dist <= max_dist).astype(int)
    result = np.multiply(
        which_calc,
        obstacles_towards
    ).sum(axis=1)
    return result / np.absolute(result)


def separation(
    boids_dxy: np.ndarray,
    boids_dist: np.ndarray,
    boids_towards: np.ndarray,
    max_dist: np.ndarray,
    obstacles_dist: np.ndarray,
    obstacles_towards: np.ndarray,
    checkpoint_towards: np.ndarray,
    wall_dist: np.ndarray,
    wall_towards: np.ndarray,
    objects: List[BaseBoid],
    kill_dist: np.ndarray,
) -> np.ndarray:
    which_calc = (boids_dist <= max_dist).astype(int)
    print(which_calc)
    result = np.multiply(
        which_calc,
        boids_towards
    ).sum(axis=1)
    return result / np.absolute(result)


def hunt(
    boids_dxy: np.ndarray,
    boids_dist: np.ndarray,
    boids_towards: np.ndarray,
    max_dist: np.ndarray,
    obstacles_dist: np.ndarray,
    obstacles_towards: np.ndarray,
    checkpoint_towards: np.ndarray,
    wall_dist: np.ndarray,
    wall_towards: np.ndarray,
    objects: List[BaseBoid],
    kill_dist: np.ndarray,
) -> np.ndarray:
    which_calc = (boids_dist <= max_dist.astype(int)).astype(float)
    which_calc2 = np.zeros(which_calc.shape)
    which_calc2[np.arange(len(boids_dist)), boids_dist.argmin(axis=1)] = 1
    which_calc = which_calc * which_calc2
    result = np.multiply(
        which_calc,
        -boids_towards
    ).sum(axis=1)
    return result / np.absolute(result)


def checkpoint(
    boids_dxy: np.ndarray,
    boids_dist: np.ndarray,
    boids_towards: np.ndarray,
    max_dist: np.ndarray,
    obstacles_dist: np.ndarray,
    obstacles_towards: np.ndarray,
    checkpoint_towards: np.ndarray,
    wall_dist: np.ndarray,
    wall_towards: np.ndarray,
    objects: List[BaseBoid],
    kill_dist: np.ndarray,
) -> np.ndarray:
    return checkpoint_towards / np.absolute(checkpoint_towards)


def walls(
    boids_dxy: np.ndarray,
    boids_dist: np.ndarray,
    boids_towards: np.ndarray,
    max_dist: np.ndarray,
    obstacles_dist: np.ndarray,
    obstacles_towards: np.ndarray,
    checkpoint_towards: np.ndarray,
    wall_dist: np.ndarray,
    wall_towards: np.ndarray,
    objects: List[BaseBoid],
    kill_dist: np.ndarray,
) -> np.ndarray:
    which_calc = np.multiply(
        (0 < abs(wall_dist)).astype(int),
        (abs(wall_dist) <= np.column_stack((max_dist, max_dist, max_dist, max_dist))).astype(int)
    )
    result = np.multiply(
        which_calc,
        -wall_towards
    ).sum(axis=1)
    return result / np.absolute(result)


def kill(
    boids_dxy: np.ndarray,
    boids_dist: np.ndarray,
    boids_towards: np.ndarray,
    max_dist: np.ndarray,
    obstacles_dist: np.ndarray,
    obstacles_towards: np.ndarray,
    checkpoint_towards: np.ndarray,
    wall_dist: np.ndarray,
    wall_towards: np.ndarray,
    objects: List[BaseBoid],
    kill_dist: np.ndarray,
) -> np.ndarray:
    to_kill = np.asarray(boids_dist <= kill_dist).nonzero()[1]
    for obj in objects:
        if obj.idx in to_kill:
            obj.kill()
    return np.zeros(boids_dist.shape[0])


rule_functions = {
    consts.ALIGNMENT: alignment,
    consts.CHECKPOINT: checkpoint,
    consts.COHESION: cohesion,
    consts.HUNT: hunt,
    consts.MAINTENANCE: maintenance,
    consts.OBSTACLES: obstacles,
    consts.SEPARATION: separation,
    consts.WALLS: walls,
    consts.KILL: kill,
}

