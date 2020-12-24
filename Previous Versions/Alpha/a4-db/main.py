import pygame
import time
import sys
import os
import random
from collections import OrderedDict
from collections import deque
import json
import copy
import pygame.font
from pygame.locals import Color

from listener import Key_listener
from timer import Bouncer
from store import Imageset
from record import Record

"""

things to keep in minds for design use:
smaller images rotate faster than larger objects

an object passed into another object's container is passed by reference not value, changing the original object changes the passed object, less calls needed

key listener can be passed to all objects at creation, checked at update time

visible object center is the absolute cordinates of an object on the stage, transformed at runtime to scaled coordinates 

Function keys control current object control
F1 = captions
F2 = cameras
F3 = props
F4 = actors
F5 = Background

Page up = next object in class
Page down = prev object in class

= sets current object as "active" which allows for control of multiple objects
when changing class all objects are set to inactive

key_listner.clear_struck() must be called at the bottom of every loop so that one time keys are not called over and over again

"""


class Background:
	#static objects which can be used both behind and in front of the actors/props


class Actor:
	#takes user input to change image form/position/state to behave as a puppet

class Prop:
	#non-static objects for actors to interact with, may as well be an actor



class Director:
	#holds all objects in a set configuration, passes information and signals to the objects for performance
	#scales to 1/8 during setup and 1/1 during render

class Stage:
	#acts as the main window, shows actor selection framerate and current states using HUD

class Camera:
	#rect container which behaves as a rect and adds filters
	#can track actors/props or run free
