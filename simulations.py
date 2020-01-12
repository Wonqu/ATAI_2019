import itertools

import consts
from boid import Dog, Sheep, Wolf, Obstacle

SHEEP_RULES = {
    consts.MAINTENANCE: 7,
    consts.ALIGNMENT: 4,
    consts.COHESION: 20,
    consts.SEPARATION: 3,
    consts.WALLS: 1000,
    consts.CHECKPOINT: 20,
    consts.OBSTACLES: 100,
}

SHEEP_WOLF_RULES = {
    consts.SEPARATION: 100
}

SHEEP_DOG_RULES = {
    consts.COHESION: 5,
    consts.SEPARATION: 3,
}

DOG_RULES = {
    consts.MAINTENANCE: 3,
    consts.SEPARATION: 2,
    consts.WALLS: 1000,
    consts.CHECKPOINT: 10,
    consts.OBSTACLES: 100,
}

DOG_WOLF_RULES = {
    consts.HUNT: 20
}

DOG_SHEEP_RULES = {
    consts.COHESION: 10,
    consts.SEPARATION: 5,
}

WOLF_RULES = {
    consts.MAINTENANCE: 7,
    consts.SEPARATION: 10,
    consts.WALLS: 1000,
    consts.OBSTACLES: 100,
}

WOLF_SHEEP_RULES = {
    consts.HUNT: 15
}

WOLF_DOG_RULES = {
    consts.SEPARATION: 100
}


sim_data_1 = {
    Sheep: {
        Sheep: SHEEP_RULES,
        Wolf: SHEEP_WOLF_RULES,
        Dog: SHEEP_DOG_RULES,
        'start': {
            'points': [
                (100, 4),
                (18, 170),
                (30, 33),
                (22, 110),
                (110, 44),
                (115, 54),
                (112, 24),
                (110, 64),
                (111, 14),
                (12, 34),
                (140, 24),
                (80, 44),
                (99, 122),
                (90, 180),
                (44, 90),
                (36, 80),
                (190, 25),
                (52, 90),
                (54, 43),
                (30, 18),
                (80, 90),
                (12, 100),
            ],
            'checkpoints': [
                (50, 50),
                (250, 50),
                (450, 50),
                (450, 250),
                (800, 700)
            ]
        }
    },
    Dog: {
        Sheep: DOG_SHEEP_RULES,
        Wolf: DOG_WOLF_RULES,
        Dog: DOG_RULES,
        'start': {
            'points': [
                (50, 120),
                (30, 90),
                (40, 10),
            ],
            'checkpoints': [
                (50, 50),
                (250, 50),
                (450, 50),
                (450, 250),
                (800, 700)
            ]
        }
    },
    Wolf: {
        Sheep: WOLF_SHEEP_RULES,
        Wolf: WOLF_RULES,
        Dog: WOLF_DOG_RULES,
        'start': {
            'points': [
                (900, 200),
                (400, 800),
                (520, 540),
                (320, 700),
                (190, 600),
            ],
            'checkpoints': []
        }
    },
    Obstacle: [
        (400, 100),
        (410, 110),
        (420, 120),
        (430, 130),
        (440, 140),
        (450, 150),
        (460, 160),
        (470, 170),
        (480, 180),
        (490, 190),
        (490, 200),
        (490, 210),
        (490, 220),
        (490, 230),
        (490, 240),
        (490, 250),
        (490, 260),
        (490, 270),
        (490, 280),
        (490, 290),
        (490, 300),
        (490, 310),
        (490, 320),
        (490, 330),
        (490, 340),
        (490, 350),
        (490, 360),
        (490, 370),
        (490, 380),
        (490, 390),
        (490, 400),
        (490, 410),
        (490, 420),
        (490, 430),
        (490, 440),
        (490, 450),
        (490, 460),
        (490, 470),
        (490, 480),
        (490, 490),
        (490, 500),
        (490, 510),
        (490, 520),
        (490, 530),
        (490, 540),
        (490, 550),
        (490, 560),
        (490, 570),
        (490, 580),
        (490, 590),
    ]
}

sim_data_2 = {
    Sheep: {
        Sheep: SHEEP_RULES,
        Wolf: SHEEP_WOLF_RULES,
        Dog: SHEEP_DOG_RULES,
    }
}

sim_data_3 = {
    Sheep: {
        Sheep: SHEEP_RULES,
        Wolf: SHEEP_WOLF_RULES,
        Dog: SHEEP_DOG_RULES,
    }
}

sim_data_4 = {
    Sheep: {
        Sheep: SHEEP_RULES,
        Wolf: SHEEP_WOLF_RULES,
        Dog: SHEEP_DOG_RULES,
    }
}

sim_data_5 = {
    Sheep: {
        Sheep: SHEEP_RULES,
        Wolf: SHEEP_WOLF_RULES,
        Dog: SHEEP_DOG_RULES,
    }
}


def simulation(sim_data):
    return {
        'boids': {
            Sheep: {
                'objects': [
                    Sheep(
                        idx,
                        sim_data[Sheep]['start']['checkpoints']
                    ) for idx, _ in enumerate(sim_data[Sheep]['start']['points'])
                ],
                'rules': {
                    Sheep: {
                        consts.MAINTENANCE: sim_data[Sheep][Sheep][consts.MAINTENANCE],
                        consts.ALIGNMENT: sim_data[Sheep][Sheep][consts.ALIGNMENT],
                        consts.COHESION: sim_data[Sheep][Sheep][consts.COHESION],
                        consts.SEPARATION: sim_data[Sheep][Sheep][consts.SEPARATION],
                        consts.WALLS: sim_data[Sheep][Sheep][consts.WALLS],
                        consts.CHECKPOINT: sim_data[Sheep][Sheep][consts.CHECKPOINT],
                        consts.OBSTACLES: sim_data[Sheep][Sheep][consts.OBSTACLES],
                    },
                    Wolf: {
                        consts.SEPARATION: sim_data[Sheep][Wolf][consts.SEPARATION]
                    },
                    Dog: {
                        consts.COHESION: sim_data[Sheep][Dog][consts.COHESION],
                        consts.SEPARATION: sim_data[Sheep][Dog][consts.SEPARATION],
                    }
                }
            },
            Dog: {
                'objects': [
                    Dog(
                        idx + len(sim_data[Sheep]['start']['points']),
                        sim_data[Dog]['start']['checkpoints']
                    ) for idx, _ in enumerate(sim_data[Dog]['start']['points'])
                ],
                'rules': {
                    Dog: {
                        consts.MAINTENANCE: sim_data[Dog][Dog][consts.MAINTENANCE],
                        consts.SEPARATION: sim_data[Dog][Dog][consts.SEPARATION],
                        consts.WALLS: sim_data[Dog][Dog][consts.WALLS],
                        consts.CHECKPOINT: sim_data[Dog][Dog][consts.CHECKPOINT],
                        consts.OBSTACLES: sim_data[Dog][Dog][consts.OBSTACLES],
                    },
                    Wolf: {
                        consts.HUNT: sim_data[Dog][Wolf][consts.HUNT]
                    },
                    Sheep: {
                        consts.COHESION: sim_data[Dog][Sheep][consts.COHESION],
                        consts.SEPARATION: sim_data[Dog][Sheep][consts.SEPARATION],
                    }
                }
            },
            Wolf: {
                'objects': [
                    Wolf(
                        idx + len(sim_data[Sheep]['start']['points']) + len(sim_data[Dog]['start']['points']),
                        sim_data[Wolf]['start']['checkpoints']
                    ) for idx, data in enumerate(sim_data[Wolf]['start']['points'])
                ],
                'rules': {
                    Wolf: {
                        consts.MAINTENANCE: sim_data[Wolf][Wolf][consts.MAINTENANCE],
                        consts.SEPARATION: sim_data[Wolf][Wolf][consts.SEPARATION],
                        consts.WALLS: sim_data[Wolf][Wolf][consts.WALLS],
                        consts.OBSTACLES: sim_data[Wolf][Wolf][consts.OBSTACLES],
                    },
                    Sheep: {
                        consts.HUNT: sim_data[Wolf][Sheep][consts.HUNT]
                    },
                    Dog: {
                        consts.SEPARATION: sim_data[Wolf][Dog][consts.SEPARATION]
                    }
                }
            }
        },
        'obstacles': [
            Obstacle(idx, [])
            for idx, _ in enumerate(sim_data[Obstacle])
        ],
        'boids_xy': [
            (x, y)
            for (x, y) in itertools.chain(
                sim_data[Sheep]['start']['points'],
                sim_data[Dog]['start']['points'],
                sim_data[Wolf]['start']['points'],
            )
        ],
        'obstacles_xy': [
            (x, y)
            for (x, y) in sim_data[Obstacle]
        ],
    }
