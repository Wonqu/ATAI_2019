import requests

boid_data = {
    'boid': [
        {'x': 1, 'y': 13, 'vx': 12, 'vy': 3},
        {'x': 4, 'y': 1, 'vx': 22, 'vy': 3},
        {'x': 2, 'y': 122, 'vx': 12, 'vy': 13},
        {'x': 11, 'y': 14, 'vx': 2, 'vy': 34},
        {'x': 22, 'y': 10, 'vx': 12, 'vy': 43},
        {'x': 13, 'y': 18, 'vx': 21, 'vy': 223},
    ]
}

response = requests.post(
    url='http://localhost:5000/boids',
    json=boid_data,
)
print(response.content)