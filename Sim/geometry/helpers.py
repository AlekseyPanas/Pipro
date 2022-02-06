"""Aleksey's Geometry Package: Helpers

Module Description
==================
This module contains a few geometric helper functions such as collision detection,
a few calculus related helpers, and a few other miscellaneous helpers.

Copyright and Usage Information
===============================

This file may be viewed by anyone for the purpose of learning or inspiration. If
the entire file/package is copied and used in another software, credits to
original creator of this file must be present.

This file is Copyright (c) 2022 Aleksey Panas.
"""
from __future__ import annotations
import math
import geometry.geometry as g
from typing import Union, Callable
import random
import colorsys

SECONDS_IN_YEAR = 31536000


def dist(p: Union[list, tuple, g.Point], q: Union[list, tuple, g.Point]):
    """Return the distance between 2 points"""
    return ((q[1] - p[1]) ** 2 + (q[0] - p[0]) ** 2) ** 0.5


def ccw(a: g.Point, b: g.Point, c: g.Point) -> bool:
    """Return if the points a,b,c are arranged in counterclockwise order"""
    return (c.y - a.y) * (b.x - a.x) > (b.y - a.y) * (c.x - a.x)


def midpoint(vector: g.Vector) -> g.Point:
    """Return midpoint of vector"""
    return vector.start + ((vector.end - vector.start) / 2)


def point_along_vector(vector: g.Vector, dist_ratio: float) -> g.Point:
    """Return midpoint of vector"""
    return vector.start + ((vector.end - vector.start) * dist_ratio)


def intersect_points(a: g.Point, b: g.Point, c: g.Point, d: g.Point) -> bool:
    """Return if segments formed by points AB and CD are intersecting"""
    return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)


def are_vectors_intersecting(vector1: g.Vector, vector2: g.Vector) -> bool:
    """Return whether vectors intersect"""
    # Calling 4 times with shuffled parameters is necessary since the algorithm is
    # inconsistent depending on input order. This ensures that the segments are not
    # considered to be colliding if they touch at endpoints, or if they are collinear and
    # overlapping
    return intersect_points(vector1.start, vector1.end, vector2.start, vector2.end) and \
        intersect_points(vector1.end, vector1.start, vector2.start, vector2.end) and \
        intersect_points(vector1.start, vector1.end, vector2.end, vector2.start) and \
        intersect_points(vector1.end, vector1.start, vector2.end, vector2.start)


def average(values: Union[list[int], tuple[int, ...], set[int]]):
    """Returns average, duh"""
    return sum(values) / len(values)


def generate_integers_with_average(lower_bound: int, upper_bound: int, avg: int, quantity: int) -> list[int]:
    """Generate quantity integers in a list within lower and upper bound inclusive such that
    the average of the integers is close or equal to avg"""
    assert lower_bound <= avg <= upper_bound

    # Generates ages between bounds
    bounds = (lower_bound, upper_bound)
    values = [random.randint(bounds[0], bounds[1]) for _ in range(quantity)]

    # If average is too high or too low, set the lambda while loop condition getter to tweak in appropriate direction
    eval_cond_and_id = ((lambda a: average(a) > avg), "down") \
        if average(values) > avg else \
        ((lambda a: average(a) < avg), "up")

    # Tweak ages in appropriate direction until the average crosses the specified avg value
    while eval_cond_and_id[0](values):
        tweakable_age_indexes = [i for i in range(len(values)) if values[i] not in bounds]
        if eval_cond_and_id[1] == "down":
            values[random.choice(tweakable_age_indexes)] -= 1
        else:
            values[random.choice(tweakable_age_indexes)] += 1

    return values


def trapezoidal_integral_approximation(n: int, a: float, b: float,
                                       f: Callable[[float], float]) -> float:
    """Given n as the number of intervals, estimate the definite integral on the interval a,b
    using the trapezoidal approximation method"""
    interval_width = (b-a) / n
    return (interval_width / 2) * (sum(2 * f(a + i * interval_width) for i in range(1, n)) + f(a) + f(b))


def approximated_function_average_on_interval(n: int, a: float, b: float,
                                              f: Callable[[float], float]) -> float:
    """Using a trapezoidal approximation of the function integral on interval a,b with n intervals of
    estimation, return the average value of the function"""
    return trapezoidal_integral_approximation(n, a, b, f) / (b-a)


def distance_func_between_vectors(v1: g.Vector, v2: g.Vector, delta_time_s: float) -> Callable[[float], float]:
    """Given 2 vectors which represent the motion of 2 objects which occurred over the given
    delta time interval, return the function of their distance as a function of time over that time
    interval"""
    a = v1.start
    b = v1.end
    c = v2.start
    d = v2.end
    r1 = (b.y - a.y - d.y + c.y) / delta_time_s
    r2 = a.y - c.y
    r3 = (b.x - a.x - d.x + c.x) / delta_time_s
    r4 = a.x - c.x
    return lambda time: ((r1*time + r2) ** 2 + (r3*time + r4) ** 2) ** 0.5


def get_shuffled(lst: list) -> list:
    """random.shuffle but returns a copy of the shuffled list"""
    lst = [e for e in lst]
    random.shuffle(lst)
    return lst


def color_brewer(num: int) -> list[tuple[int, ...]]:
    """Returns an equally spaced list of colors with length of num"""
    if num == 0:
        return []
    val = 0.7 / num
    return [tuple(int(c * 255) for c in colorsys.hsv_to_rgb(i * val, 0.8, 0.8)) for i in range(num)]


def roll_probability(prob: float) -> bool:
    """
    Roll the probability and return whether it was successful

    Preconditions:
        - 0 <= prob <= 1
    """
    total = 1
    while prob != int(prob):
        total *= 10
        prob *= 10
    return random.randint(1, total) <= prob


def scale_probability(pc: float, sc: float, sn: float, accuracy=3) -> float:
    """Given a probability of pc, which is the probability of an event occurring
    within a time interval of sc seconds, return the probability of the event
    occurring within a time interval of sn"""
    return round(1-(1-pc)**(sn/sc), accuracy)


def vector_from_magnitude_direction(start: g.Point, direction: float, magnitude: float) -> g.Vector:
    """Given a start pos, direction angle in radians, and magnitude, return a vector"""
    dx = math.cos(direction) * magnitude
    dy = math.sin(direction) * magnitude
    return g.Vector(start, start + g.Point(dx, dy))


def constant_acceleration_position(initial_velocity: float,
                                   acceleration: float, delta_t: float) -> float:
    """Return change in position after constant acceleration over a period of delta_t"""
    return (initial_velocity * delta_t) + (0.5 * acceleration * (delta_t ** 2))
