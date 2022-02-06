from __future__ import annotations
import math
import random
from geometry.geometry import *
from geometry.helpers import *
import requests
import threading
from dataclasses import dataclass


class Sim:
    """Manages whole sim."""
    drone: Drone
    walls: list[Wall]
    pipes: list[Pipe]

    AIR_DENSITY = 1.2  # kg/m^3  TODO: NOT WORKING, FIX AIR DRAG
    AIR_MULT = 0.995  # Temporary air friction multiplier for speed of drone

    POST_URL = "http://127.0.0.1:5000/ping-add"

    def __init__(self, walls: list[Vector], pipes: list[Vector], drone_start: Point):
        self.drone = Drone(drone_start)
        self.walls = [Wall(v) for v in walls]
        self.pipes = [Pipe(p) for p in pipes]
        self.leaks = []

        self.responses = []
        # Tracks leaks already notified, to prevent spam notification
        self.notified_leaks = []

    def update(self, time_delta: float) -> None:
        # Compute drone physics / logic
        self.drone.update(self, time_delta)

        # Run pipes and gets back leaks, if any
        for pipe in self.pipes:
            self.leaks.extend(pipe.update(self, time_delta))

        # Run leak particle emitter
        for leak in self.leaks:
            leak.update(self, time_delta)

        #print("Res count:", len(self.responses))
        #print("Detect count:", self.count)
        #print("Reqs started:", self.requests_started)

    @staticmethod
    def air_drag(speed: float, drag_coeff: float, cross_section_area: float):
        return 0.5 * Sim.AIR_DENSITY * (speed ** 2) * drag_coeff * cross_section_area

    def apply_force_drone(self, x: float, y: float):
        """Apply an x,y component force in Newtons on the drone"""
        self.drone.forces.append(Point(x, y))

    def detect_gas(self, leak_source: Leak):
        """This function is called as a callback from leak emitters
        when gas is detected and sends a notification request to server"""
        if leak_source not in self.notified_leaks:
            self.notified_leaks.append(leak_source)
            param = [leak_source.emitter_loc.x, leak_source.emitter_loc.y]
            threading.Thread(target=self.notify_server, args=(param,)).start()

    def notify_server(self, leak_pos: list[float]) -> None:
        """Notify server of leak!"""
        print("test thread ran!")
        print("I am the arg:", leak_pos)
        res = requests.post(Sim.POST_URL, json={"location": leak_pos})
        print(res)
        self.responses.append(res)



@dataclass
class Wall:
    """Represents a wall which you cannot pass through"""
    vec: Vector


class Drone:
    """Main object in game

    Instance Attributes
        - pos: Center position of drone
        - radius: Size of drone
        - velocity: point relative to drone center indicating velocity x,y (m/s)
        - accel: point relative to drone center indicating acceleration x,y (m/s^2)
        - forces: list of points relative to drone center indicating forces (Newtons)
        - net_force: computed sum of all forces (Newtons)
        - mass: Kilograms
    """
    radius: float
    pos: Point
    velocity: Point
    accel: Point
    forces: list[Point]
    net_force: Point
    mass: float

    DRAG_COEFFICIENT = 0.35

    def __init__(self, pos: Point, radius=0.1):
        self.radius = radius

        self.mass = 0.3

        self.pos = pos
        self.velocity = Point(0.0, 0.0)
        self.accel = Point(0.0, 0.0)

        self.forces = []
        self.net_force = Point(0.0, 0.0)

    def _add_drag(self):
        # TODO: NOT WORKING
        # Velocity Vector
        vel_vec = Vector(Point(0.0, 0.0), self.velocity)
        vel_mag = vel_vec.get_magnitude()

        # Computes drag force
        air_drag_force = Sim.air_drag(vel_mag, Drone.DRAG_COEFFICIENT, self.radius / 4)

        #print("vel", self.velocity)
        #print(vel_vec)
        #print(air_drag_force)
        #print("direction", vel_vec.get_direction())

        i = vector_from_magnitude_direction(
            Point(0.0, 0.0),
            vel_vec.get_direction() + math.pi,
            air_drag_force).end

        #print(i)

        # Add drag as point relative to center pos
        self.forces.append(
            vector_from_magnitude_direction(
                Point(0.0, 0.0),
                vel_vec.get_direction() + math.pi,
                air_drag_force).end)

    def _compute_net_force(self, sim: Sim) -> None:
        """Compute net force"""
        #print("Forces:", self.forces)
        self.net_force = Point(0.0, 0.0)

        # Use point addition to add forces together
        for force in self.forces:
            self.net_force += force

        #print("Net Force:", self.net_force)

    def _perform_motion(self, sim: Sim, time_delta: float) -> None:
        """Perform drone motion and resolve any collisions"""
        # Compute acceleration
        self.accel = Point(self.net_force.x / self.mass,
                           self.net_force.y / self.mass)

        #print("Accel:", self.accel)
        # Find position change at constant acceleration
        delta_pos = Point(
            constant_acceleration_position(self.velocity.x, self.accel.x, time_delta),
            constant_acceleration_position(self.velocity.y, self.accel.y, time_delta)
        )

        #print("Pos delta:", delta_pos)
        # Checks collisions
        collision_wall = None
        for w in sim.walls:
            if are_vectors_intersecting(w.vec, Vector(self.pos, self.pos + delta_pos)):
                collision_wall = w

        # Change velocity based on acceleration
        self.velocity += self.accel * time_delta

        # Apply Air Drag
        self.velocity *= Sim.AIR_MULT

        if collision_wall is None:
            # Shift Position
            self.pos += delta_pos
        else:
            # Resolve collision
            self._resolve_wall_collision(collision_wall)

        #print("New Vel:", self.velocity)

    def _resolve_wall_collision(self, wall: Wall):
        """Apply changes to kinematic quantities post-collision"""
        self.velocity *= 0

    def update(self, sim: Sim, time_delta: float) -> None:
        """Update drone forces and other physical properties. Resolve collisions"""
        #print("\n" * 20)
        #self._add_drag()
        self._compute_net_force(sim)
        self.forces = []

        self._perform_motion(sim, time_delta)


class Pipe:
    """Pipes that can leak"""
    vec: Vector

    LEAK_PROB_PER_HOUR = 0.999

    def __init__(self, vec: Vector):
        self.vec = vec

    def update(self, sim: Sim, time_delta: float) -> list[Leak]:
        """Return leaks that occurred, if any"""
        prob = scale_probability(Pipe.LEAK_PROB_PER_HOUR, 60, time_delta, 10)
        #print("Leak Probability", prob)
        roll_result = roll_probability(prob)
        #print("Roll Result", roll_result)
        if roll_result:
            return [Leak(point_along_vector(self.vec, random.random()))]
        return []


class Leak:
    """Leak emits gas particles from a location and keeps track of particles
    pertaining to that leak

    Instance Attributes:
        - emitter_loc: Point from where emission occurs
        - frequency: Probability that a particle will spawn over a second
        - particles: A list containing [[x, y], (vx, vy), lifetime] of a particle
    """
    emitter_loc: Point
    frequency: float
    particles: list[list[list[float, float], tuple[float, float], float]]

    PARTICLE_DEATH = 20.0

    def __init__(self, emitter_loc: Point):
        self.emitter_loc = emitter_loc

        self.frequency = 0.99
        self.particles = []
        self.speed_multiplier = 0.003

    def update(self, sim: Sim, time_delta: float):
        """Update gas particle motion"""
        prob = scale_probability(self.frequency, 1, time_delta, 10)
        roll = roll_probability(prob)
        while roll:
            roll = roll_probability(prob)

            self.particles.append([[self.emitter_loc.x, self.emitter_loc.y], (
                random.random() * self.speed_multiplier * random.choice([-1, 1]),
                random.random() * self.speed_multiplier * random.choice([-1, 1])
            ), 0.0])
        #print("Particle Prob:", prob)
        #print("Particle Roll:", roll)

        trash = []
        # Move particles
        for p in self.particles:
            # Send callback
            if dist(sim.drone.pos, p[0]) < sim.drone.radius:
                sim.detect_gas(self)

            p[0][0] += p[1][0]
            p[0][1] += p[1][1]
            p[2] += time_delta
            # Particle lifetime
            if p[2] > Leak.PARTICLE_DEATH:
                trash.append(p)
        for p in trash:
            self.particles.remove(p)

