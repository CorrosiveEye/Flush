                         import pygame
                         import sys
                         import random

from pygame              import Surface, font
 
from state               import State
from data                import *
from constants           import *
from utils               import Timer
from drawables           import *

from retrogamelib.camera import Camera, ParallaxCamera
from retrogamelib.dialog import DialogBox, Menu

class MenuState(State):
    def __init__(self):
        super(MenuState, self).__init__()

        self.debug = False
        self.scale = 8

        self.elapsed = 0
        self.sinspeed = random.uniform(.1, .2)


    def on_resume(self):
        super(MenuState, self).on_resume()
        for snow in snowbg_sprites_list:
            snow.set_pos(self.cam.rect)
        self.cam.follow(self.menu)

    def on_reset(self):
        for group in all_groups_list:
            for thing in group:
                thing.kill()


    def on_load(self, camera=None, font=None, fps=None):
        super(MenuState, self).on_load(camera, font, fps)

        self.menu = Menu(self.font, ["Play", "Options", "Quit"],
                (self.surf_main.get_width() / 2) / 2, (self.surf_main.get_height() / 2) / 2)


    def on_event(self, e):
        for event in e:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.switch_state("playstate")

                elif event.key == pygame.K_RETURN:
                    option = self.menu.get_option()
                    if option[0] == 0:
                        self.switch_state("playstate")
                    elif option[0] == 1:
                        print("Make me do something...")
                    elif option[0] == 2:
                        pygame.quit()
                        sys.exit()

                elif event.key == pygame.K_r:
                    self.on_reset()
                    self.on_load()

                elif event.key == pygame.K_UP:
                    self.menu.move_cursor(-1)

                elif event.key == pygame.K_DOWN:
                    self.menu.move_cursor(1)

    def on_update(self):
        self.cam.on_update(self.fps.speed_factor)
        self.menu.on_update()
        for snow in snowbg_sprites_list:
            snow.on_update(self.fps.speed_factor)
            snow.check_collision(self.cam.rect)
        self.cam.translate(snowbg_sprites_list)
        self.cam.translate([self.menu])

    def on_render(self):
        self.surf_main.fill((5, 10, 20))
        
        for snow in snowbg_sprites_list:
            snow.on_render(self.surf_main)

        self.menu.draw(self.surf_main,
                self.menu.rect)

        for sprite in fog_sprites_list:
            sprite.on_render(self.surf_main)
