import json

from flask import Flask, render_template, jsonify, request

import utils
from boids import separation, alignment, cohesion, move, vec_len

app = Flask(__name__, template_folder='templates')


@app.route('/')
def hello_world():

    img = './static/entity.svg'
    return render_template('base.html', img=img)


@app.route('/boids', methods=['POST'])
def boids():
    MAX_DIST_SEP = 100
    MAX_DIST_AL = 200
    MAX_DIST_COH = 300
    SPEED = 0.5
    if request.method == 'POST':
        boid_data = json.loads(request.data)
        # print(separation('boid', boid_data, MAX_DIST_SEP))
        # print(alignment('boid', boid_data, MAX_DIST_AL))
        # print(cohesion('boid', boid_data, MAX_DIST_COH))
        move_vectors = [
            utils.sum_tuples(
                (cur[0] / vec_len(*cur), cur[1] / vec_len(*cur)),
                sep,
                al,
                coh,
            ) for (cur, sep, al, coh) in zip(
                [(b['vx'], b['vy']) for b in boid_data['boid']],
                separation(
                    'boid',
                    boid_data,
                    MAX_DIST_SEP,
                ),
                alignment(
                    'boid',
                    boid_data,
                    MAX_DIST_AL,
                ),
                cohesion(
                    'boid',
                    boid_data,
                    MAX_DIST_COH,
                ),
            )
        ]
        boid_data['boid'] = [
            {
                'x': x,
                'y': y,
                'vx': vx,
                'vy': vy,
            } for (
                (x, y),
                (vx, vy)
            ) in zip(
                [
                    move((b['x'], b['y']), mv, SPEED)
                    for (b, mv) in zip(boid_data['boid'], move_vectors)
                ],
                move_vectors
            )
        ]
        return jsonify(boid_data)
    return jsonify({'xaxa': 'xaxa'})


if __name__ == '__main__':
    app.run()
