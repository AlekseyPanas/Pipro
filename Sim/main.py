import pygame
import time
from geometry.geometry import Point, Vector, Rectangle
from App import App
import json
import os

walls = []
pipes = []
start_pos = Point(0.0, 0.0)

FILENAME = 'test_config.json'

with open(os.path.join(os.path.dirname(__file__), 'configs', FILENAME), 'r') as file:
    loaded_json = json.load(file)

    for w in loaded_json["walls"]:
        walls.append(Vector(
            Point(w["start"]["x"], w["start"]["y"]),
            Point(w["end"]["x"], w["end"]["y"])
        ))

    for p in loaded_json["pipes"]:
        pipes.append(Vector(
            Point(p["start"]["x"], p["start"]["y"]),
            Point(p["end"]["x"], p["end"]["y"])
        ))

    start_pos = Point(loaded_json["drone_start"]["x"], loaded_json["drone_start"]["y"])

App((.6, .6), walls, pipes, start_pos).start()
