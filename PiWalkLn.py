#!/usr/bin/env python2

from itertools import izip
from math import cos, log, pi, sin, sqrt
from PIL import Image
from PIL.ImageDraw import Draw


# --- Utils. It probably already exists in the standard library,
#     I just don't know where.

phi = (1 + sqrt(5)) / 2


def take(n, seq):
    for _ in xrange(n):
        yield next(seq)


def repeat(x):
    # Shouldn't this exist already?
    while True:
        yield x


# --- Raw generation and handling of sequences

def gen_pi():
    # Stolen and adapted from http://stackoverflow.com/q/9004789/3070326
    # Otherwise I would need to copy/paste a huge chunk of the digits of pi.
    q, r, t, k, m, x = 1, 0, 1, 1, 3, 3
    while True:
        if 4 * q + r - t < m * t:
            yield m
            q, r, t, k, m, x = \
                10*q, 10*(r-m*t), t, k, (10*(3*q+r))//t - 10*m, x
        else:
            q, r, t, k, m, x = \
                q*k, (2*q+r)*x, t*x, k+1, (q*(7*k+2)+r*x)//(t*x), x+2


walk_default_angle = pi / phi


def gen_walk_from_raw(seq, angle=None, step=.5):
    angle = angle if angle != None else walk_default_angle
    def angle2dir(angle):
        return (cos(angle), -sin(angle))
    x, y, lookat = 0.0, 0.0, 0.0
    yield (x, y)
    for l in seq:
        px, py = angle2dir(lookat)
        lookat += angle
        x, y = x + l * step * px, y + l * step * py
        yield (x, y)


# --- Making it more presentable

def compress(x,y):
    d = sqrt(x*x + y*y)
    if d <= 1:
        return (x, y)
    d2 = 1 + log(d)
    return (x * d2 / d, y * d2 / d)


def compress_seq(seq):
    for (x,y) in seq:
        yield compress(x,y)


def intermediate_color(phase):
    if phase < .5:
        phase = phase * 2
        # 0.0 -> (255, 0, 0)
        # 0.5 -> (0, 255, 0)
        return tuple(map(int, (255 - 255*phase, 255*phase, 0)))
    else:
        phase = (phase - 0.5) * 2
        # 0.0 -> (0, 255, 0)
        # 0.5 -> (0, 0, 255)
        return tuple(map(int, (0, 255 - 255*phase, 255*phase)))


# 7 turns out to be a good guess for compressed sequences
def gen_img(scale=80, max_x=7, max_y=7):
    """max_x: assume that the input's x-coordinates will stay in [-max_x ... max_x]
    max_y: assume that the input's y-coordinates will stay in [-max_y ... max_y]
    scale: scale up the input by this factor"""
    img = Image.new("RGB", (max_x * scale * 2, max_y * scale * 2))
    img.scale = scale
    return img

def draw_compiled(img, xyc_it):
    """Draws a sequence of x,y,color tuples onto an image.

    xyc_it: iterator of x,y,color tuples. The color of the first entry is
        discarded, all other colors are used as the respective line's color"""
    center_x, center_y = map(lambda n: n / 2, img.size)
    d = Draw(img)
    (x, y), _ = next(xyc_it)
    x, y = x * img.scale + center_x, y * img.scale + center_y
    for ((x2, y2), c) in xyc_it:
        x2, y2 = x2 * img.scale + center_x, y2 * img.scale + center_y
        d.line((x, y, x2, y2), c)
        x, y = x2, y2


def colorize(xy):
    xyl = list(xy) # the most inefficient step
    l = len(xyl)
    for (i, p) in enumerate(xyl):
        yield (p, intermediate_color((i - 1) / (l - 2.0))) if i != 0 else (p, None)


def gen_box(w=8, h=6, step=1, complete=True):
    return \
        zip(range(0, w + 1, step), repeat(-h)) + \
        zip(repeat(w), range(-h, h + 1, step)) + \
        zip(range(w, -(w + 1), -step), repeat(h)) + \
        zip(repeat(-w), range(h, -(h + 1), -step)) + \
        zip(range(-w, step if complete else 0, step), repeat(-h))


# --- High-level stuff

def gen_boxed_img_from_raw(seq, scale=80):
    img = gen_img(scale=scale)
    draw_compiled(img, colorize(compress_seq(seq)))
    draw_compiled(img, izip(compress_seq(gen_box(200, 100, 5)), repeat((192,) * 3)))
    draw_compiled(img, izip(compress_seq(gen_box(20, 10, 2)), repeat((128,) * 3)))
    draw_compiled(img, izip(compress_seq(gen_box(2, 1)), repeat((64,) * 3)))
    return img


def save_pi_img(n=3000, angle=None, name=None):
    img = gen_boxed_img_from_raw(gen_walk_from_raw(take(n, gen_pi()), angle=angle))
    # Note that images will (often enough) be bitwise identical if run with the
    # same parameters, so overwriting is okay.
    name = name if name != None else \
        "samples/pi_a%1.5f_n%07d.png" % \
        (angle if angle != None else walk_default_angle, n)
    fp = open(name, "w")
    img.save(fp, "png")
    fp.close()
    print "Finished %s" % name


def save_samples():
    [save_pi_img(n, angle * pi if angle != None else None) \
        for angle in [1.0/10, 1.0/6, 1.0/5, 1.0/3, 1.0/2, 2.0/3, None, 179/180.0] \
        for n in [10, 30, 100, 300, 1000, 3000]]
    print "Done saving your samples :)"


def save_samples_expensive():
    [save_pi_img(10000, angle * pi if angle != None else None) \
        for angle in [1.0/10, 1.0/6, 1.0/5, 1.0/3, 1.0/2, 2.0/3, None, 179/180.0]]
    print "Done saving your expensive samples :)"


# --- Be able to run from command line

def main():
    print "Writing lots of images ..."
    save_samples()


if __name__ == '__main__':
    main()
