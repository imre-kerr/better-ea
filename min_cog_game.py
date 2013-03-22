from __future__ import division

import pygame
import random
from operator import mul

class Game:
    agent_size = 5
    max_motion = 4

    board_width = 30
    board_height = 15
    block_size = 30
    horizontal_direction = 0
    num_drops = 40
    

    def __init__(self):
        '''Generate a game instance that can be played by several agents in turn.
        
        Order of blocks should be decided here.'''
        
        self.object_sizes = [random.randint(1, 6) for i in range(self.num_drops)]
        self.object_positions = [random.randint(0, self.board_width - i) for i in self.object_sizes]
        
        
    def visual_init(self):
        '''Initialize some pygame stuff'''
        pygame.init()
        self.fps_clock = pygame.time.Clock()
    
        self.window_surface_obj = pygame.display.set_mode((Game.board_width*Game.block_size, Game.board_height*Game.block_size))
        pygame.display.set_caption("Minimally Cognitive Agent: The Game: The Movie")
        
        self.black_color = pygame.Color(0,0,0)
        self.red_color = pygame.Color(255,0,0)
        self.blue_color = pygame.Color(0,0,255)
        self.white_color = pygame.Color(255,255,255)
        self.purple_color = pygame.Color(255,0,255)
        
        self.font_obj = pygame.font.Font('freesansbold.ttf', 32)
        
        
    def visual_frame(self, score, board):
        '''Draw a single frame and sync to 3 FPS'''
        for x in xrange(Game.board_width):
            for y in xrange(Game.board_height):
                cell = board[x][y]
                color = None
                if cell == 0:
                    color = self.black_color
                elif cell == 1:
                    color = self.blue_color
                elif cell == 2:
                    color = self.red_color
                else:
                    color = self.purple_color
                pygame.draw.rect(self.window_surface_obj, color, pygame.Rect(x*Game.block_size, y*Game.block_size, Game.block_size, Game.block_size))
            
        self.msg_surface = self.font_obj.render("Score: " + str(score), False, self.white_color)
        self.msg_rect = self.msg_surface.get_rect()
        self.msg_rect.topleft = (10,10)
        self.window_surface_obj.blit(self.msg_surface, self.msg_rect)
        0
        for event in pygame.event.get():
            'DOOOO NOTHIIIIIINGG'
            
        pygame.display.update()
        self.fps_clock.tick(10)
        
 
    def play(self, ctrnn, visual):
        '''Plays a game with the CTRNN argument as the controller.
        
        Object's internal state should NOT change between successive calls.
        If visual is True, a visualization of the gameplay should be shown.'''
        
        score = 0
        
        if visual:
            self.visual_init()
        
        for drop in xrange(Game.num_drops):
            object = range(self.object_positions[drop], self.object_positions[drop] + self.object_sizes[drop])
            agent_start = Game.board_width//2 - Game.agent_size//2
            agent = range(agent_start, agent_start+Game.agent_size)
            
            if visual:
                board = [[0]*self.board_height for i in xrange(self.board_width)]
                for i in object:
                    board[i][0] += 1
                for i in agent:
                    board[i][Game.board_height-1] += 2
                self.visual_frame(score, board)
                
            for step in xrange(Game.board_height):
                sensor_input = [i in object for i in agent]
                left_motion, right_motion = ctrnn.timestep(sensor_input)
                motion_sum = left_motion + right_motion
                motion = int(round((motion_sum)*Game.max_motion - Game.max_motion))
                agent = [(i + motion)%Game.board_width for i in agent]
                if Game.horizontal_direction != 0:
                    object = [(i + Game.horizontal_direction)%Game.board_width for i in object]
            
                if visual:
                    board = [[0]*self.board_height for i in xrange(Game.board_width)]
                    for i in object:
                        board[i][step] += 1
                    for i in agent:
                        board[i][Game.board_height-1] += 2
                    self.visual_frame(score, board)
                    
            if self.object_sizes[drop] < Game.agent_size:
                score += reduce(mul, (i in agent for i in object), 1)
            else:
                score += 0 if sum((i in object for i in agent)) else 1.2 
             
            if visual:
                self.visual_frame(score, board)
                self.visual_frame(score, board)
                
            ctrnn.reset()

        if visual:
            pygame.quit()   

        return score
