from __future__ import annotations
import math
import pygame
import random
from geometry.geometry import Point, Vector, Rectangle
import time
from Sim import *
from dataclasses import dataclass
from typing import Optional
pygame.init()


class App:
    """In charge of rendering the sim"""
    sim: Sim

    SCROLL_FACTOR = 1.05
    MOVE_FACTOR = 0.01  # Percent of camera's world width to move

    def __init__(self, screen_size_percent: tuple[float, float],
                 walls: list[Vector], pipes: list[Vector], drone_start: Point):
        self.sim = Sim(walls, pipes, drone_start)
        self.running = True

        self.sim_speed = 1.0

        # Pygame / drawing
        monitor_size = pygame.display.Info()
        h_ratio = monitor_size.current_h / monitor_size.current_w
        self.camera = Camera(0, 0, 25, h_ratio)

        self.screen = pygame.display.set_mode(
            (monitor_size.current_w * screen_size_percent[0],
             monitor_size.current_h * screen_size_percent[1])
        )

        self.events = []

    def start(self):
        """Start the app main loop"""
        self.running = True
        self.run()

    def run(self) -> None:
        """Run main app loop"""
        ti = time.time()
        while self.running:
            # Time delta
            tf = time.time()
            t_delta = tf - ti
            ti = tf

            # Refresh screen, handle events
            self.screen.fill((0, 0, 0))
            self.events = pygame.event.get()
            self.handle_events()

            # Update sim
            self.sim.update(t_delta * self.sim_speed)
            # Render sim
            self.render_sim()

            # Refresh screen
            pygame.display.update()

    def render_sim(self) -> None:
        """Render sim components onto screen"""
        for wall in self.sim.walls:
            self.draw_vector(wall.vec, (0, 255, 0), endpt_rad=4)

        for pipe in self.sim.pipes:
            self.draw_vector(pipe.vec, (255, 0, 0), endpt_rad=4)

        for leak in self.sim.leaks:
            self.draw_circle(leak.emitter_loc, (255, 255, 0), 0.1, 2)
            for p in leak.particles:
                self.draw_circle(Point(*p[0]), (255, 255, 0), 0.02)

        self.draw_circle(self.sim.drone.pos, (0, 0, 255), self.sim.drone.radius)

    def draw_vector(self, vec: Vector, color: tuple[int, int, int], endpt_rad: Optional[int] = None) -> None:
        """Given a vector in sim-world coordinates, convert and draw the vector relative
        to App camera"""
        # Start and end points converted into camera world
        conv_st = self.camera.convert_point(vec.start, self.screen.get_width())
        conv_ed = self.camera.convert_point(vec.end, self.screen.get_width())

        pygame.draw.line(self.screen, color, conv_st, conv_ed)

        if endpt_rad is not None:
            rad = endpt_rad #self.camera.scale_quantity(endpt_rad, self.screen.get_width())
            pygame.draw.circle(self.screen, color, conv_st, rad, 1)
            pygame.draw.circle(self.screen, color, conv_ed, rad, 1)

    def draw_circle(self, center: Point, color: tuple[int, int, int], radius: float, width=0) -> None:
        """Given a circle in sim-world coordinates, convert and draw the vector relative
        to App camera"""
        conv_cent = self.camera.convert_point(center, self.screen.get_width())
        rad = self.camera.scale_quantity(radius, self.screen.get_width())
        pygame.draw.circle(self.screen, color, conv_cent, rad, width)

    def handle_events(self):
        """Handle user events and perform actions"""
        for event in self.events:
            if event.type == pygame.QUIT:
                self.stop()
            # Camera zoom
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_WHEELDOWN:
                    self.camera.set_width(self.camera.width() * self.SCROLL_FACTOR)
                elif event.button == pygame.BUTTON_WHEELUP:
                    self.camera.set_width(self.camera.width() / self.SCROLL_FACTOR)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.sim.apply_force_drone(0.0, -10.0)
                elif event.key == pygame.K_DOWN:
                    self.sim.apply_force_drone(0.0, 10.0)
                elif event.key == pygame.K_LEFT:
                    self.sim.apply_force_drone(-10.0, 0.0)
                elif event.key == pygame.K_RIGHT:
                    self.sim.apply_force_drone(10.0, 0.0)

        # Camera pan
        p = pygame.key.get_pressed()
        self.camera.y += (p[pygame.K_s] - p[pygame.K_w]) * App.MOVE_FACTOR * self.camera.width()
        self.camera.x += (p[pygame.K_d] - p[pygame.K_a]) * App.MOVE_FACTOR * self.camera.width()

    def stop(self) -> None:
        """Stop the app from running"""
        self.running = False


class Camera:
    """
    Class to represent a camera view into a 2D world. Represented by
    a rectangle with rotation ability.

    NOTE: ANGLE ROTATION NOT SUPPORTED YET
    """
    x: float  # Center x in sim world
    y: float  # Center y in sim world
    w: float  # Width in sim world coords
    h_ratio: float  # Ratio of height to width
    angle: float  # Radian angle that camera rotates about center

    def __init__(self, x: float, y: float, w: float, h_ratio: float, angle=0.0):
        self.x = x
        self.y = y
        self._w = w
        self._h_ratio = h_ratio
        self.angle = angle

    def set_width(self, new_width: float):
        self._w = new_width

    def width(self) -> float:
        return self._w

    def height(self) -> float:
        return self._w * self._h_ratio

    def center(self) -> Point:
        return Point(self.x, self.y)

    def top_left(self) -> Point:
        return Point(self.x - self._w / 2, self.y - self.height() / 2)

    def convert_point(self, pt: Point, pixel_width: int) -> Point:
        """Given a point, pt, within the 2D world where the camera resides, return
        the coordinates of the point relative to the camera's top left corner and
        scaled into screen render location based on pixel_width"""
        top_left = self.top_left()
        return Point(self.scale_quantity(pt.x - top_left.x, pixel_width),
                     self.scale_quantity(pt.y - top_left.y, pixel_width))

    def scale_quantity(self, value: float, pixel_width: int) -> float:
        """Given a pixel width of screen and an in-world measurement value,
        scale the measurement to be relative to pixel_width"""
        ratio = pixel_width / self._w
        return value * ratio
