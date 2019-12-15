import itertools
import json

from flask import Flask, render_template, jsonify, request

from boids import move, calculate_rule
from _profile import profileit
from consts import POSITIONS, BOIDS, OBSTACLES, BOID_SHEEP, RULES, MAP_X, MAP_Y
from utils import sum_vecs, xy, vxy, norm_vec, mul_vec, cummulative_sums, dist_matrix, lines_dist_matrix, \
    ranges, get_context, vec_matrix, points_to_lines

app = Flask(__name__, template_folder='templates')


import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/')
def hello_world():

    img = './static/entity.svg'
    return render_template('base.html', img=img, ctx=get_context())


@app.route('/boids', methods=['POST'])
@profileit
def boids():
    SPEED = 2
    if request.method == 'POST':
        boid_data = json.loads(request.data)
        named_ranges = dict(zip(
            boid_data[BOIDS].keys(),
            ranges(cummulative_sums([len(x[POSITIONS]) for x in boid_data[BOIDS].values()])),
        ))
        all_positions = list(itertools.chain(
            *[
                boid_type[POSITIONS]
                for boid_type in boid_data[BOIDS].values()
            ]
        ))
        d_matrix = dist_matrix(all_positions)
        # obs_d_matrix = lines_dist_matrix(
        #     all_positions,
        #     [
        #         points_to_lines(ob['points'])
        #         for ob in boid_data[OBSTACLES]
        #     ],
        #     [ob['bounce'] for ob in boid_data[OBSTACLES]]
        # )
        obs_d_matrix = [[] for _ in all_positions]
        v_matrix = vec_matrix(all_positions)
        all_data = list(zip(
            all_positions,
            d_matrix,
            obs_d_matrix,
            v_matrix,
        ))
        # for x in all_data:
        #     print('=========')
        #     for a in x:
        #         print(len(a), a)
        #     print('=========')
        for b_type, b_data in boid_data[BOIDS].items():
            # print([
            #     sum_vecs(*list(
            #         calculate_rule(all_data, named_ranges, **r)
            #         for r in b_data[RULES]
            #     ))
            # ])
            sum_matrix = [list() for _ in b_data[POSITIONS]]
            for result_vector in (calculate_rule(all_data, named_ranges, **r) for r in b_data[RULES]):
                for j, result in enumerate(result_vector):
                    sum_matrix[j].append(result)
            # print(sum_matrix)
            # for x in sum_matrix:
            #     print(x)
            move_vectors = [
                norm_vec(
                    sum_vecs(*result_vector)
                )
                for result_vector in sum_matrix
            ]
            boid_data[BOIDS][b_type][POSITIONS] = [
                {'x': x, 'y': y, 'vx': vx, 'vy': vy}
                for ((x, y), (vx, vy))
                in zip(
                    [
                        move(xy(b), mv, SPEED, (MAP_X, MAP_Y), 16)
                        for (b, mv) in zip(b_data[POSITIONS], move_vectors)
                    ],
                    move_vectors
                )
            ]
        # print(separation(50, all_data, named_ranges, max_dist=16, target=BOID_SHEEP))
        # print(alignment(9, all_data, named_ranges, max_dist=80, target=BOID_SHEEP))
        # print(cohesion(3, all_data, named_ranges, max_dist=48, target=BOID_SHEEP))
        # print(obstacle(3, all_data, named_ranges, max_dist=48, target=BOID_SHEEP))
        # print(maintain(50, all_data, named_ranges, target=BOID_SHEEP))
        # move_vectors = [
        #     norm_vec(
        #         sum_vecs(
        #
        #         )
        #     )
        # ]
        # move_vectors = [
        #     norm_vec(
        #         sum_vecs(
        #             mul_vec(norm_vec(cur), 50.),
        #             mul_vec(sep_close, 60.),
        #             mul_vec(sep_far, 1.),
        #             mul_vec(al, 9.),
        #             mul_vec(coh_close, 3),
        #             mul_vec(coh_far, 0.5),
        #             mul_vec(bor_close, 60.),
        #             # mul_vec(bor_far, 2.),
        #         )
        #     ) for (
        #         cur,
        #         sep_close,
        #         sep_far,
        #         al,
        #         coh_close,
        #         coh_far,
        #         bor_close,
        #         bor_far,
        #     ) in zip(
        #         [vxy(b) for b in boid_data['boid']['POSITIONS']],
        #         separation('boid', boid_data, MAX_DIST_SEP,),
        #         separation('boid', boid_data, MIN_DIST_SEP,),
        #         alignment('boid', boid_data, MAX_DIST_AL,),
        #         cohesion('boid', boid_data, MIN_DIST_COH,),
        #         cohesion('boid', boid_data, MAX_DIST_COH,),
        #         obstacle('boid', boid_data, MIN_DIST_BORDER, (850, 850)),
        #         obstacle('boid', boid_data, MAX_DIST_BORDER, (850, 850)),
        #     )
        # ]
        # boid_data['boid'] = {
        #     'color': '#FFFFFF',
        #     'rules': boid_data['boid']['rules'],
        #     'POSITIONS': [
        #         {
        #             'x': x,
        #             'y': y,
        #             'vx': vx,
        #             'vy': vy,
        #         } for (
        #             (x, y),
        #             (vx, vy)
        #         ) in zip(
        #             [
        #                 move(xy(b), mv, SPEED, (850, 850), 16)
        #                 for (b, mv) in zip(boid_data['boid']['POSITIONS'], move_vectors)
        #             ],
        #             move_vectors
        #         )
        #     ]
        # }
        return jsonify(boid_data)
    return jsonify({'xaxa': 'xaxa'})


if __name__ == '__main__':
    app.run()
