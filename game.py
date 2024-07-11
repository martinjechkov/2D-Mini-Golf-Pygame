import pygame
import sys
import json
from game_objects import GameLevel, Object, ObjectType, TeleportPad, ShotCounter
from ball import Ball
from level_completed import LevelCompletedScreen
from game_completed import GameCompletedScreen
from main_menu import MainMenuScreen

class Game:
    def __init__(self, level_file, level_number, window_width, window_height):
        pygame.init()
        pygame.display.set_caption("Mini Golf")
        self.level_file = level_file
        self.level_number = level_number
        self.screen = pygame.display.set_mode((window_width, window_height))
        self.level_completed = False
        self.last_level = False
        
        self.main_menu = MainMenuScreen(self.screen)
        
        with open(self.level_file, 'r') as f:
            self.levels = json.load(f)['levels']

        self.run()

    def load_level(self, level_number):
        level_data = self.levels[level_number - 1] # make from 1-based index to 0-based index
        
        if self.level_number == len(self.levels):
            self.last_level = True
        print(f"Current level number: {self.level_number}")
        print(f"Total number of levels: {len(self.levels)}")
        print(self.last_level)

        background_image = pygame.image.load(level_data.get('background')['path_to_background'])

        self.level = GameLevel(background_image)
        for obj_data in level_data['objects']:
            obj_type = obj_data['type']
            position = tuple(obj_data['position'])
            size = obj_data.get('size')
            shape = obj_data['shape']
            color = obj_data['color']
            
            if obj_type == 'TeleportPad':
                destination = tuple(obj_data['destination'])
                obj = TeleportPad(shape, position, size, destination, color)
            elif obj_type == 'Hole':
                obj = Object(shape, position, size, ObjectType.HOLE, color)
            elif obj_type == 'Obstacle':
                obj = Object(shape, position, size, ObjectType.OBSTACLE, color)
            else:
                raise ValueError(f"Unknown object type: {obj_type}")
            
            self.level.add_object(obj)
        
        ball_data = level_data.get('ball')
        if ball_data:
            self.ball = Ball(position=ball_data['position'], radius=ball_data['radius'], color=ball_data['color'])
        else:
            raise ValueError(f"NO BALL DATA FOR LEVEL: {level_number}")


    def handle_event(self, event):
        if self.level_completed:
            result = self.level_completed_screen.handle_event(event)
            if result == "next_level":
                self.level_number += 1
                self.load_level(self.level_number)
                self.level_completed = False
            elif result == "main_menu":
                self.main_menu.active = True
                self.main_menu.draw()
                self.level_completed = False
        else:
            result = self.ball.handle_event(event)
            if result == "ball_shot":
                self.shot_counter.increase_shot_count()

    def update(self):
        self.ball.update()
        self.check_collision()

    def check_collision(self):
        for obj in self.level.objects:
            if isinstance(obj, TeleportPad):
                if self.ball.check_collision(obj):
                    obj.teleport_ball(self.ball)
            elif obj.shape == 'circle':
                if self.ball.check_collision(obj):
                    if obj.object_type == ObjectType.HOLE:
                        self.level_completed = True
                        self.ball.visible = False

                        if not self.last_level:
                            self.level_completed_screen = LevelCompletedScreen(self.screen, self.level_number, self.capture_screen())
                        elif self.last_level:
                            self.game_completed_screen = GameCompletedScreen(self.screen, self.shot_counter.shot_count)
                    else:
                        self.ball.handle_collision(obj)
            elif obj.shape == 'rectangle':
                if self.ball.check_collision(obj):
                    self.ball.handle_collision(obj)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if self.main_menu.active:
                    action = self.main_menu.handle_event(event)
                    if action == "start":
                        self.main_menu.active = False
                        self.shot_counter = ShotCounter()
                        self.last_level = False
                        self.load_level(self.level_number)
                    elif action == "quit":
                        running = False
                if event.type == pygame.QUIT:
                        running = False
                if self.main_menu.active == False:
                    self.handle_event(event)

            if self.main_menu.active:
                self.main_menu.draw()
            elif not self.main_menu.active and not self.level_completed:
                self.level.draw_objects(self.screen)
                self.shot_counter.draw(self.screen)
                self.update()
                self.ball.draw(self.screen)

            if self.level_completed and self.last_level == False:
                self.level_completed_screen.draw(self.screen)
            elif self.level_completed and self.last_level:
                self.game_completed_screen.draw(self.screen)

            pygame.display.flip()
            pygame.time.Clock().tick(60)
        pygame.quit()
        sys.exit()

    def capture_screen(self):
        return self.screen.copy()