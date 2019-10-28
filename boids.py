import math

import utils


def vec_len(x, y):
    return math.sqrt(x**2 + y**2)


def dist(x1, x2, y1, y2):
    return math.sqrt(
        abs((x1 - x2)**2 + (y1 - y2)**2)
    )


def separation(boid_type, boid_data, max_dist):
    boids = boid_data.get(boid_type, [])
    location_dist_matrix = [
        [
            (
                b2['x'] - b1['x'],
                b2['y'] - b1['y'],
                dist(b1['x'], b2['x'], b1['y'], b2['y']) / max_dist,
            )
            for b1 in boids
        ]
        for b2 in boids
    ]
    result_vector = [(0, 0, 0) for x in range(len(boids))]
    for i, _ in enumerate(result_vector):
        # sum local boids distance
        result_vector[i] = (
            sum(x for (x, _, w) in location_dist_matrix[i] if w <= 1),
            sum(y for (_, y, w) in location_dist_matrix[i] if w <= 1),
            sum(w for (_, _, w) in location_dist_matrix[i] if w <= 1),
        )
        if 1 > result_vector[i][2] <= 0:
            vl = vec_len(boid_data[boid_type][i]['vx'], boid_data[boid_type][i]['vy'])
            result_vector[i] = (
                boid_data[boid_type][i]['vx'] / vl,
                boid_data[boid_type][i]['vy'] / vl,
            )
            continue
        # calculate destination as average vector of local boids
        result_vector[i] = (
            result_vector[i][0]/(result_vector[i][2] or 1),
            result_vector[i][1]/(result_vector[i][2] or 1),
        )
        result_vector[i] = (
            (result_vector[i][0] or boid_data[boid_type][i]['vx']),
            (result_vector[i][1] or boid_data[boid_type][i]['vy']),
        )
        result_vector[i] = (
            result_vector[i][0] / (vec_len(*result_vector[i]) or 1),
            result_vector[i][1] / (vec_len(*result_vector[i]) or 1),
        )
    return result_vector


def alignment(boid_type, boid_data, max_dist):
    boids = boid_data.get(boid_type, [])
    result_vector = [(0, 0, 0) for x in range(len(boids))]
    destination_dist_matrix = [
        [
            (
                b1['vx'] if b1 != b2 else 0,
                b1['vy'] if b1 != b2 else 0,
                dist(b1['x'], b2['x'], b1['y'], b2['y']) if b1 != b2 else float('inf')
            )
            for b1 in boids
        ]
        for b2 in boids
    ]
    for i, _ in enumerate(result_vector):
        # sum local boids destinations
        result_vector[i] = (
            sum(vx for (vx, _, d) in destination_dist_matrix[i] if d <= max_dist),
            sum(vy for (_, vy, d) in destination_dist_matrix[i] if d <= max_dist),
            sum(1 for (_, _, d) in destination_dist_matrix[i] if d <= max_dist),
        )
        if 1 > result_vector[i][2] <= 0:
            vl = vec_len(boid_data[boid_type][i]['vx'], boid_data[boid_type][i]['vy'])
            result_vector[i] = (
                boid_data[boid_type][i]['vx'] / vl,
                boid_data[boid_type][i]['vy'] / vl,
            )
            continue
        # calculate destination as average or other boids destination
        result_vector[i] = (
            result_vector[i][0] / (result_vector[i][2] or 1),
            result_vector[i][1] / (result_vector[i][2] or 1),
        )
        # normalize destination vector
        result_vector[i] = (
            (result_vector[i][0] or boid_data[boid_type][i]['vx']) / (vec_len(*result_vector[i]) or 1),
            (result_vector[i][1] or boid_data[boid_type][i]['vy']) / (vec_len(*result_vector[i]) or 1),
        )
    return result_vector


def cohesion(boid_type, boid_data, max_dist):
    boids = boid_data.get(boid_type, [])
    result_vector = [(0, 0, 0) for x in range(len(boids))]
    location_dist_matrix = [
        [
            (
                b1['x'] - b2['x'],
                b1['y'] - b2['y'],
                dist(b1['x'], b2['x'], b1['y'], b2['y']) / max_dist,
            )
            for b1 in boids
        ]
        for b2 in boids
    ]
    for i, _ in enumerate(result_vector):
        # sum local boids location
        result_vector[i] = (
            sum(x for (x, _, w) in location_dist_matrix[i] if w <= 1),
            sum(y for (_, y, w) in location_dist_matrix[i] if w <= 1),
            sum(w for (_, _, w) in location_dist_matrix[i] if w <= 1),
        )
        if 1 > result_vector[i][2] <= 0:
            vl = vec_len(boid_data[boid_type][i]['vx'], boid_data[boid_type][i]['vy'])
            result_vector[i] = (
                boid_data[boid_type][i]['vx'] / vl,
                boid_data[boid_type][i]['vy'] / vl,
            )
            continue
        # calculate destination as average vector of local boids
        result_vector[i] = (
            result_vector[i][0] / (result_vector[i][2] or 1),
            result_vector[i][1] / (result_vector[i][2] or 1),
        )
        # normalize destination vector
        result_vector[i] = (
            (result_vector[i][0] or boid_data[boid_type][i]['vx']) / (vec_len(*result_vector[i]) or 1),
            (result_vector[i][1] or boid_data[boid_type][i]['vy']) / (vec_len(*result_vector[i]) or 1),
        )
    return result_vector


def move(boid, vec, speed):
    vl = vec_len(*vec)
    vec = tuple(a * speed / vl for a in vec)
    return utils.sum_tuples(boid, vec)


if __name__ == '__main__':
    boid_data = {
        'boid': [
            {'x': 0, 'y': 12, 'vx': -1, 'vy': -10},
            {'x': 1, 'y': 4, 'vx': 12, 'vy': 63},
            {'x': 2, 'y': 41, 'vx': 13, 'vy': 31},
            {'x': 12, 'y': 21, 'vx': 14, 'vy': 38},
            {'x': 14, 'y': 11, 'vx': 11, 'vy': 32},
            {'x': 18, 'y': 7, 'vx': 10, 'vy': 312},
            {'x': 19, 'y': 4, 'vx': 18, 'vy': 35},
            {'x': 20, 'y': 2, 'vx': 14, 'vy': 33},
            {'x': 21, 'y': 11, 'vx': 12, 'vy': 13},
        ]
    }
    print(separation('boid', boid_data, 4))
    print(alignment('boid', boid_data, 8))
    print(cohesion('boid', boid_data, 12))
