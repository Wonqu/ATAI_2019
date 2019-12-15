import itertools
import math

from operator import itemgetter

import numpy as np

import consts

xy = itemgetter('x', 'y')
vxy = itemgetter('vx', 'vy')


def sum_vecs(*vecs, n=2):
    if vecs:
        return tuple(
            sum([v[i] for v in vecs])
            for i, t in enumerate(vecs[0])
        )
    return tuple(0. for _ in range(n))


def norm_vec(vec):
    v_len = vec_len(vec)
    if v_len:
        return tuple(x / v_len for x in vec)
    return tuple(0. for _ in vec)


def mul_vec(vec, scalar):
    return tuple(x * scalar for x in vec)


def mul_vec_weight(vec, dist, max_dist, weight_f):
    return mul_vec(vec, weight_f(dist, max_dist))


def vec(p1, p2):
    return p2[0] - p1[0], p2[1] - p1[1]


def vec_len(_vec):
    return math.sqrt(sum(x**2 for x in _vec))


def dist(vec_1, vec_2):
    return math.sqrt(
        sum(
            (xk - yk)**2
            for (xk, yk) in zip(vec_1, vec_2)
        )
    )


def dist_from_line(p1, p2, _vec):
    x0, y0 = _vec
    x1, y1 = p1
    x2, y2 = p2
    return abs(
        (y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1
    ) / math.sqrt(
        (y2 - y1)**2 + (x2 - x1)**2
    )


def overflow(_vec, map_sizes, boid_size):
    return _vec


def cummulative_sums(xs):
    return [sum(xs[:i]) for i in range(len(xs)+1)]


def ranges(xs):
    return [(xs[i], xs[i+1]) for i in range(len(xs) - 1)]


def dist_matrix(bs):
    z = np.array([[complex(*xy(b)) for b in bs]])
    return abs(z.T - z).tolist()


def lines_dist_matrix(bs, obs, bounces):
    # boid coordinates as vector of pairs
    b_vector = np.array([[xy(b) for b in bs]], dtype=[('Px', 'float32'), ('Py', 'float32')]).T

    # obstacles coordinates as vector of (x1, y1, x2, y2, xc, yc, bounce)
    xs = [
        x
        for (p1, p2, p3, p4), ce, b in list(zip(
            obs,
            list(mul_vec(sum_vecs(*v), 1 / (len(v) * 2)) for v in obs),  # centers
            bounces,
        ))
        for x in [
            tuple([*p1, ce[0] + ce[2], ce[1] + ce[3], b]),
            tuple([*p2, ce[0] + ce[2], ce[1] + ce[3], b]),
            tuple([*p3, ce[0] + ce[2], ce[1] + ce[3], b]),
            tuple([*p4, ce[0] + ce[2], ce[1] + ce[3], b]),
        ]
    ]
    ob_vector = np.array(
        [[xs]],
        dtype=[
            ('Ax', 'float32'),
            ('Ay', 'float32'),
            ('Bx', 'float32'),
            ('By', 'float32'),
            ('Cx', 'float32'),
            ('Cy', 'float32'),
            ('bounce', 'float32'),
        ]
    )

    # distance function
    # from: https://gist.github.com/nim65s/5e9902cd67f094ce65b0
    # but slightly refactored and modified to fit the purpose of running it as vectorized
    def dist_f(P, ABCb):
        """ segment line AB, point P, where each one is an array([x, y]) """
        A, B = np.array([ABCb[0], ABCb[1]]), np.array([ABCb[2], ABCb[3]])
        C = np.array([ABCb[4], ABCb[5]])
        bounce = ABCb[6]
        P = np.array([P[0], P[1]])
        if np.allclose(A, P, atol=16) or np.allclose(B, P, atol=16):
            result = 0
        else:
            result = dist_from_line(
                (A[0], A[1]),
                (B[0], B[1]),
                (P[0], P[1]),
            )

        return result, C[0], C[1], bounce

    # vectorize and return calculated results
    line_dist_vec = np.vectorize(dist_f)
    rst = line_dist_vec(b_vector, ob_vector)

    # flatten result
    res = list(
        (d, x, y, b)
        for (dd, xx, yy, bb) in zip(
            rst[0].tolist()[0],
            rst[1].tolist()[0],
            rst[2].tolist()[0],
            rst[3].tolist()[0],
        )
        for (d, x, y, b) in zip(
            dd, xx, yy, bb
        )
    )

    # reshape it back to proper list of lists
    res = [res[i:i+len(xs)] for i in range(0, len(rst[0].tolist()[0]))]
    return res


def vec_matrix(bs):
    xys = [xy(b) for b in bs]
    return [
        [
            (xi - xj, yi - yj)
            for (xj, yj) in xys
        ]
        for (xi, yi) in xys
    ]


def points_to_lines(points):
    return [
        tuple(
            itertools.chain(
                *[
                    xy(p)
                    for p in [points[i], points[(i+1) % len(points)]]
                ]
            )
        ) for i in range(len(points))
    ]


def get_context():
    return {
        'BOIDS': consts.BOIDS,
        'BOID_TYPES': consts.BOID_TYPES,
        'COLOR': consts.COLOR,
        'OBSTACLES': consts.OBSTACLES,
        'POSITIONS': consts.POSITIONS,
        'RULE_TYPES': consts.RULE_TYPES,
        'RULES': consts.RULES,
        'MAP_X': consts.MAP_X,
        'MAP_Y': consts.MAP_Y,
    }
