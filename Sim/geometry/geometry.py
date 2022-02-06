"""Aleksey's Geometry Package: Geometry

Module Description
==================
This module contains classes representing various geometric objects useful
for the simulation, namely, Points, Vectors, Paths, Rectangles, and Circles

Copyright and Usage Information
===============================

This file may be viewed by anyone for the purpose of learning or inspiration. If
the entire file/package is copied and used in another software, credits to
original creator of this file must be present.

This file is Copyright (c) 2022 Aleksey Panas.
"""
from __future__ import annotations
import math
from geometry.helpers import *
from typing import Any, Callable, Union
import pygame


class Point:
    """
    Representation of a 2D point
    """
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    def _perform_operation(self, other: Any,
                           operation: Callable[[float, Union[int, float]], float]):
        if isinstance(other, (float, int)):
            return Point(operation(self.x, other), operation(self.y, other))
        elif isinstance(other, (list, Point, tuple)) and len(other) == 2:
            return Point(operation(self.x, other[0]), operation(self.y, other[1]))
        else:
            raise TypeError("Can only add numerical values to points")

    def __add__(self, other: Any) -> Point:
        return self._perform_operation(other, lambda a, b: a + b)

    def __sub__(self, other: Any) -> Point:
        return self._perform_operation(other, lambda a, b: a - b)

    def __truediv__(self, other) -> Point:
        return self._perform_operation(other, lambda a, b: a / b)

    def __mul__(self, other) -> Point:
        return self._perform_operation(other, lambda a, b: a * b)

    def __eq__(self, other: Point):
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise TypeError("Indexing into a point must be done with integers, not " + str(type(item).__name__))
        elif item not in (0, 1):
            raise IndexError("A point can only be indexed at 0 or 1")
        return self.x if item == 0 else self.y

    def __iter__(self):
        return (self.x, self.y).__iter__()

    def __str__(self):
        return "Point" + str(tuple(self))

    def __len__(self):
        return 2

    def __repr__(self):
        return self.__str__()


class Vector:
    """
    Representation of a 2D vector
    """
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def __iter__(self):
        return iter((self.start, self.end))

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise TypeError("Indexing into a point must be done with integers, not " + str(type(item).__name__))
        elif item not in (0, 1):
            raise IndexError("A vector can only be indexed at 0 or 1")
        return self.start if item == 0 else self.end

    def __str__(self):
        return "Vector" + str(tuple(self))

    def __repr__(self):
        return self.__str__()

    def get_bounding_box(self) -> Rectangle:
        """Get the vector's bounding box"""
        left = min(self.start, self.end, key=lambda p: p[0])[0]
        width = max(self.start, self.end, key=lambda p: p[0])[0] - left

        top = min(self.start, self.end, key=lambda p: p[1])[1]
        height = max(self.start, self.end, key=lambda p: p[1])[1] - top

        return Rectangle(
            left=left,
            top=top,
            width=width,
            height=height
        )

    def get_direction(self) -> float:
        """Return angle in radians where the vector is facing"""
        return math.atan2(self.end[1] - self.start[1],
                          self.end[0] - self.start[0])

    def get_magnitude(self) -> float:
        """Return the length of the vector"""
        return dist(self.start, self.end)


class Path:
    """
    Representation of a path as a list of sequential points
    """
    def __init__(self, points: list[Point]):
        self.points = points

    def get_vectors(self) -> list[Vector]:
        """Return the path as a list of connected vectors. Point references are maintained
        in the resulting vector list!"""
        return [Vector(self.points[i], self.points[i + 1]) for i in range(len(self.points) - 1)]

    def __iter__(self):
        return iter(self.points)

    def __str__(self):
        return "Path" + str(tuple(self))

    def __repr__(self):
        return self.__str__()


class Rectangle:
    """
    Rect shape for path finding
    """
    def __init__(self, left: float, top: float, width: float, height: float):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def is_vector_intersect(self, vector: Vector) -> bool:
        """Return if vector intersects rectangle, false if vector only touches edges or vertices"""
        sides = self.get_sides()

        # Checks if any side intersects vector, or if vector's start, end, or midpoint is inside the rect
        return any(are_vectors_intersecting(side, vector) for side in sides) or \
            self.is_point_inside(vector.start) or \
            self.is_point_inside(vector.end) or self.is_point_inside(midpoint(vector))

    def get_vertices(self) -> list[Point]:
        """Return all 4 corners of the rectangle"""
        return [
            Point(self.left, self.top),
            Point(self.left + self.width, self.top),
            Point(self.left + self.width, self.top + self.height),
            Point(self.left, self.top + self.height)
        ]

    def get_inflated(self, radius: float):
        """Return new rectangle with all sides expanded in every direction by radius, preserving center"""
        return Rectangle(
            left=self.left - radius,
            top=self.top - radius,
            width=self.width + radius * 2,
            height=self.height + radius * 2,
        )

    def get_area(self) -> float:
        """Do the width times the height yknow? skrrt skrrt"""
        return self.width * self.height

    def is_point_inside(self, point: Point):
        """Return if point is inside the shape. If point is on edges, does not count"""
        return self.left < point.x < self.left + self.width and \
            self.top < point.y < self.top + self.height

    def is_point_inside_inclusive(self, point: Point):
        """Return if point is inside the rectangle, or on its edges"""
        return self.left <= point.x <= self.left + self.width and \
            self.top <= point.y <= self.top + self.height

    def is_point_between_edges(self, point: Point, only_vertical=False, only_horizontal=False) -> bool:
        """Return if the point's x coordinate is between the left and right side or if the point's
        y coordinate is between the top and bottom sides (open interval, excluding the edges themselves)"""
        if only_vertical:
            return self.left < point.x < self.left + self.width
        elif only_horizontal:
            return self.top < point.y < self.top + self.height
        return self.left < point.x < self.left + self.width or \
            self.top < point.y < self.top + self.height

    def get_sides(self) -> list[Vector]:
        """Return all sides of the rectangle as vectors (start and end hold no significance for these)"""
        bot = Vector(Point(self.left, self.top + self.height),
                     Point(self.left + self.width, self.top + self.height))

        top = Vector(Point(self.left, self.top),
                     Point(self.left + self.width, self.top))

        left = Vector(Point(self.left, self.top),
                      Point(self.left, self.top + self.height))

        right = Vector(Point(self.left + self.width, self.top),
                       Point(self.left + self.width, self.top + self.height))
        return [bot, top, left, right]

    def get_pygame_rectangle(self):
        """Pygame Rect objects only accept integers, hence we have our own Rectangle class. This method returns
        a pygame rectangle instance of this rectangle"""
        return pygame.Rect((self.left, self.top), (self.width, self.height))


class Circle:
    """
    Circle shape for path finding
    """
    def __init__(self, center_x: float, center_y: float, radius: float):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius

    def is_vector_intersect(self, vector: Vector) -> bool:
        """Return if vector intersects the circle, tangent line should be false"""
        # TODO: This algorithm is not done. Review projection approach on iPad
        return False

    def get_inflated(self, radius: float) -> Circle:
        """
        Return new circle with its radius increased by radius
        """
        return Circle(
            center_x=self.center_x,
            center_y=self.center_y,
            radius=self.radius + radius
        )

    def get_bounding_box(self) -> Rectangle:
        """Return rectangle representing this circle's bounding box"""
        return Rectangle(left=self.center_x - self.radius,
                         top=self.center_y - self.radius,
                         width=self.radius * 2,
                         height=self.radius * 2)

    def is_point_inside(self, point: Point):
        """Return if point is inside the circle, but not on edge"""
        return dist((self.center_x, self.center_y), (point.x, point.y)) < self.radius
