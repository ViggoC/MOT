import pygame as pg
from MOT_constants import *

class MOTobj:
    def __init__(self, default_color=WHITE):
        # -- Radius of the circle objects
        self.radius = obj_radius

        # self.shuffle_position()
        # -- Velocity set so that it's random within a range but NOT ZERO
        self.shuffle_speed()
        # -- Set the circle object neutral state color
        self.color = default_color
        self.default_color = default_color

        # -- Timer attributes
        self.timer = 0
        self.flash = True

        # -- State attributes for mouse selection control
        self.state = ""
        self.isClicked = False
        self.isSelected = False

    def change_color(self, color):
        self.color = color

    def in_circle(self, mouse_x, mouse_y):
        # -- Return boolean value depending on mouse position, if it is in circle or not
        if math.sqrt(((mouse_x - self.x) ** 2) + ((mouse_y - self.y) ** 2)) < self.radius:
            return True
        else:
            return False

    def state_control(self, state):
        # -- Neutral or default state with no form of mouse selection
        if state == "neutral":
            self.color = self.default_color
            self.state = "neutral"
            self.isClicked = self.isSelected = False
        # -- Hovered state if mouse is hovering over circle object
        if state == "hovered":
            self.color = hover_col
            self.state = "hovered"
            self.isClicked = self.isSelected = False
        # -- Clicked state if mouse click DOWN while in object
        if state == "clicked":
            self.color = click_col
            self.state = "clicked"
            self.isClicked = True
            self.isSelected = False
        # -- Selected state if mouse click UP on a "clicked" object
        if state == "selected":
            self.color = select_col
            self.state = "selected"
            self.isClicked = False
            self.isSelected = True

    def detect_wall(self, mlist):
        # -- Object positions in x and y coordinates change in velocity value
        self.x += self.dx
        self.y += self.dy
        # -- If the object reaches the window boundary, bounce back
        if self.x < self.radius:
            self.dx = abs(self.dx) 
        if self.x > win_width-self.radius:
            self.dx = -abs(self.dx) 
        if self.y < self.radius:
            self.dy = abs(self.dy) 
        if self.y > win_height-self.radius:
            self.dy = -abs(self.dy)
        # -- If the object bounces off each other, run the Brownian motion physics
        # objects need to be from the same list, otherwise the objects
        # can pass through each other if they're from a different list
        # for a in mlist:
        for b in mlist:
            if self != b:
                if math.sqrt(((self.x - b.x) ** 2) + ((self.y - b.y) ** 2)) <= (self.radius + b.radius):
                    self.brownian_motion(b)

    def draw_circle(self, display):
        # -- Function to draw circle onto display
        pg.draw.circle(display, self.color, (int(self.x), int(self.y)), self.radius)

    def flash_color(self):
        # -- Function to flash color
        if self.timer == FPS:
            self.timer = 0
            self.flash = not self.flash

        # flash frequency
        self.timer += 5

        if self.flash:
            self.color = self.default_color
        else:
            self.color = GREEN

    # def shuffle_position(self):
    #     """Shuffle the position of circles"""
    #     self.x = choice([n for n in range(int(boundary["left"]), int(boundary["right"]), self.radius)])
    #     self.y = choice([n for n in range(int(boundary["up"]), int(boundary["down"]), self.radius)])
    
    def shuffle_speed(self):
        dx_t = random()*2-1
        dy_t = random()*2-1
        spd_t = math.sqrt((dx_t ** 2) + (dy_t ** 2))
        self.dx = dx_t/spd_t*max_spd
        self.dy = dy_t/spd_t*max_spd


    def set_position(self, pos):
        self.x, self.y = pos

    def brownian_motion(self, C2):
        """ ===== FUNCTION TO CALCULATE BROWNIAN MOTION ===== """
        c1_spd = math.sqrt((self.dx ** 2) + (self.dy ** 2))
        diff_x = -(self.x - C2.x)
        diff_y = -(self.y - C2.y)
        vel_x = 0
        vel_y = 0
        if diff_x > 0:
            if diff_y > 0:
                angle = math.degrees(math.atan(diff_y / diff_x))
                vel_x = -c1_spd * math.cos(math.radians(angle))
                vel_y = -c1_spd * math.sin(math.radians(angle))
            elif diff_y < 0:
                angle = math.degrees(math.atan(diff_y / diff_x))
                vel_x = -c1_spd * math.cos(math.radians(angle))
                vel_y = -c1_spd * math.sin(math.radians(angle))
        elif diff_x < 0:
            if diff_y > 0:
                angle = 180 + math.degrees(math.atan(diff_y / diff_x))
                vel_x = -c1_spd * math.cos(math.radians(angle))
                vel_y = -c1_spd * math.sin(math.radians(angle))
            elif diff_y < 0:
                angle = -180 + math.degrees(math.atan(diff_y / diff_x))
                vel_x = -c1_spd * math.cos(math.radians(angle))
                vel_y = -c1_spd * math.sin(math.radians(angle))
        elif diff_x == 0:
            if diff_y > 0:
                angle = -90
            else:
                angle = 90
            vel_x = c1_spd * math.cos(math.radians(angle))
            vel_y = c1_spd * math.sin(math.radians(angle))
        elif diff_y == 0:
            if diff_x < 0:
                angle = 0
            else:
                angle = 180
            vel_x = c1_spd * math.cos(math.radians(angle))
            vel_y = c1_spd * math.sin(math.radians(angle))
        self.dx = vel_x
        self.dy = vel_y