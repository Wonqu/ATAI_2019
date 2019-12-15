from rewrite import consts
from rewrite.consts import WALL_DISTANCE, WIDTH, HEIGHT


def alignment(b1, boids, w):
    dx, dy = 0, 0
    i = 0
    for b2 in boids:
        if b1 != b2:
            bx = (b2.x - b1.x)
            by = (b2.y - b1.y)
            d = (bx ** 2 + by ** 2) ** 0.5
            if d < 50:
                i += 1
                dx += b2.dx
                dy += b2.dy
    if i:
        dx = dx / i
        dy = dy / i
        d = (dx**2 + dy**2)**0.5
        return w * dx / d, w * dy / d
    return 0, 0


def cohesion(b1, boids, w):
    ax, ay = 0, 0
    vx, vy = 0, 0
    i = 0
    for b2 in boids:
        if b1 != b2:
            bx = (b2.x - b1.x)
            by = (b2.y - b1.y)
            d = (bx**2 + by**2)**0.5
            if d < 50:
                i += 1
                ax += b2.x
                ay += b2.y

    if i:
        ax /= i
        ay /= i
        vx = ax - b1.x
        vy = ay - b1.y

        d = (vx**2 + vy**2) ** 0.5
        vx = vx / d * w
        vy = vy / d * w

    return vx, vy


def maintenance(b1, boids, w):
    return w * b1.dx, w * b1.dy


def obstacles(b1, boids, w):
    return b1.x * w, b1.y * w


def separation(b1, boids, w):
    dx, dy = 0, 0
    i = 0
    for b2 in boids:
        if b1 != b2:
            bx = (b2.x - b1.x)
            by = (b2.y - b1.y)
            d = (bx**2 + by**2)**0.5
            min_dist, max_dist = b1.SEPARATION_DISTANCES.get(b2.__class__, (b1.SIZE, b1.SIZE))
            if d <= max_dist:
                i += 1
                d = d / max_dist if d > min_dist else 1
                dx += bx / d
                dy += by / d

    if i:
        d = (dx**2 + dy**2)**0.5
        dx /= d
        dy /= d

    return -w * dx, -w * dy


def hunt(b1, boids, w):
    dx, dy = 0, 0
    sx, sy = 0, 0
    i = 0
    for b2 in boids:
        min_d = float('inf')
        if b1 != b2:
            bx = (b2.x - b1.x)
            by = (b2.y - b1.y)
            d = (bx ** 2 + by ** 2) ** 0.5
            if d <= b1.HUNT_DISTANCES[b2.__class__]:
                i += 1
                sx += bx / d
                sy += by / d
                if d <= min_d:
                    min_d = d
                    dx = bx
                    dy = by
                if min_d <= b1.SIZE:
                    boids.remove(b2)

    if i:
        sd = (sx ** 2 + sy ** 2) ** 0.5
        sx /= sd * i
        sy /= sd * i

        d = (dx ** 2 + dy ** 2) ** 0.5
        dx /= d
        dy /= d

    return w * (dx * i + 0), w * (dy * i + 0)


def center(b1, boids, w):
    cx = consts.WIDTH / 2
    cy = consts.HEIGHT / 2

    bx = (cx - b1.x)
    by = (cy - b1.y)

    d = (bx ** 2 + by ** 2) ** 0.5

    return bx / d, by / d


def walls(b1, boids, w):
    dx = 0
    dy = 0

    # x component
    if b1.x + WALL_DISTANCE >= WIDTH:
        dx = -w
    elif b1.x - WALL_DISTANCE <= 0:
        dx = w

    # y component
    if b1.y + WALL_DISTANCE >= HEIGHT:
        dy = -w
    elif b1.y - WALL_DISTANCE <= 0:
        dy = w

    return dx, dy


rule_functions = {
    consts.ALIGNMENT: alignment,
    consts.CENTER: center,
    consts.COHESION: cohesion,
    consts.HUNT: hunt,
    consts.MAINTENANCE: maintenance,
    consts.OBSTACLES: obstacles,
    consts.SEPARATION: separation,
    consts.WALLS: walls,
}

