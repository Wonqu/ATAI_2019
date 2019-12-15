import consts
from utils import dist, xy, sum_vecs, norm_vec, mul_vec, vxy, overflow, dist_from_line, mul_vec_weight, vec


class Strategy:
    pass


def separation(weight, all_data, named_ranges, **params):
    max_dist = params['max_dist']
    target = params['target']
    result_matrix = [
        mul_vec(
            norm_vec(
                sum_vecs(*list(
                    mul_vec_weight(v, d, max_dist, lambda d, m_d: (d/m_d) if d <= m_d else 0)
                    for (d, v) in zip(d_vec, v_vec)
                ))
            ),
            -weight
        )
        for pos, d_vec, _, v_vec in all_data[slice(*named_ranges[target])]
    ]
    return result_matrix


def alignment(weight, all_data, named_ranges, **params):
    max_dist = params['max_dist']
    target = params['target']
    result_matrix = [
        mul_vec(
            norm_vec(
                sum_vecs(*list(
                    mul_vec_weight(vxy(b_d), d, max_dist, lambda d, m_d: (d / m_d) if d <= m_d else 0)
                    for (d, b_d) in zip(d_vec, [b_d[0] for b_d in all_data])
                ))
            ),
            weight
        )
        for pos, d_vec, _, _ in all_data[slice(*named_ranges[target])]
    ]
    return result_matrix


def cohesion(weight, all_data, named_ranges, **params):
    max_dist = params['max_dist']
    target = params['target']
    result_matrix = [
        mul_vec(
            norm_vec(
                sum_vecs(*list(
                    mul_vec_weight(v, d, max_dist, lambda d, m_d: ((m_d - d) / m_d) if d <= m_d else 0)
                    for (d, v) in zip(d_vec, v_vec)
                ))
            ),
            weight
        )
        for pos, d_vec, _, v_vec in all_data[slice(*named_ranges[target])]
    ]
    return result_matrix


def maintain(weight, all_data, named_ranges, **params):
    target = params['target']
    result_matrix = [
        mul_vec(norm_vec(vxy(pos)), weight)
        for pos, _, _, _ in all_data[slice(*named_ranges[target])]
    ]
    return result_matrix


def obstacles(weight, all_data, named_ranges, **params):
    max_dist = params['max_dist']
    target = params['target']
    result_matrix = []
    for pos, _, o_vec, _ in all_data[slice(*named_ranges[target])]:
        vecs = []
        for (o_d, o_xc, o_yc, bounce) in o_vec:
            vecs.append(
                mul_vec_weight(
                    vec((o_xc, o_yc), xy(pos)),
                    o_d,
                    max_dist,
                    lambda d, m_d: (((m_d - d) / m_d) * bounce) if d <= m_d else 0
                )
            )
        result_matrix.append(mul_vec(norm_vec(sum_vecs(*vecs)), weight))
    return result_matrix


def calculate_rule(all_data, named_ranges, **params):
    params = params.copy()
    rule_name = params.pop('rule')
    rule_weight = params.pop('weight')
    rule_functions = {
        consts.RULE_ALIGNMENT: alignment,
        consts.RULE_COHESION: cohesion,
        consts.RULE_MAINTAIN: maintain,
        consts.RULE_OBSTACLES: obstacles,
        consts.RULE_SEPARATION: separation,
    }
    result_matrix = rule_functions[rule_name](rule_weight, all_data, named_ranges, **params)
    return result_matrix


def move(boid, dir_vec, speed, map_sizes, boid_size):
    # normalize direction vector and multiply it by movement speed, then add it to boid's current position
    return overflow(
        sum_vecs(
            boid,
            mul_vec(norm_vec(dir_vec), speed),
        ),
        map_sizes,
        boid_size,
    )


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
