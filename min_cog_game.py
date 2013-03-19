import pygame
import random
from operator import mul

class Game:
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
        
        self.font_obj = pygame.font.Font('freesansbold.ttf', 32)
        
        
    def visual_frame(self):
        '''Draw a single frame and sync to 3 FPS'''
                
        for x in xrange(Game.board_width):
            for y in xrange(Game.board_height):
                cell = self.board[x][y]
                color = None
                if cell == 0:
                    color = self.black_color
                elif cell == 1:
                    color = self.blue_color
                else:
                    color = self.red_color
                pygame.draw.rect(self.window_surface_obj, color, pygame.Rect(x*Game.block_size, y*Game.block_size, Game.block_size, Game.block_size))
            
        for event in pygame.event.get():
            'DOOOO NOTHIIIIIINGG'
            
        pygame.display.update()
        self.fps_clock.tick(5)
        
 
    def play(self, ctrnn, visual):
        '''Plays a game with the CTRNN argument as the controller.
        
        Object's internal state should NOT change between successive calls.
        If visual is True, a visualization of the gameplay should be shown.'''
        
        score = 0
        
        if visual:
            self.visual_init()
        
        for drop in xrange(self.num_drops):
            object = range(self.object_positions[drop], self.object_positions[drop] + self.object_sizes[drop]+1)
            agent = range(13, 18)
            
            if visual:
                self.board = [[0]*self.board_height for i in xrange(self.board_width)]
                for i in object:
                    self.board[i][0] = 1
                for i in agent:
                    self.board[i][14] = 2
                self.visual_frame()
                
            for step in xrange(self.board_height):
                sensor_input = [i in object for i in agent]
                left_motion, right_motion = ctrnn.timestep(sensor_input)
                motion = int(round(4*right_motion - 4*left_motion))
                agent = [(i + motion)%self.board_width for i in agent]
                object = [(i + self.horizontal_direction)%self.board_width for i in object]
            
                if visual:
                    self.board = [[0]*self.board_height for i in xrange(self.board_width)]
                    for i in object:
                        self.board[i][step] = 1
                    for i in agent:
                        self.board[i][14] = 2
                    self.visual_frame()
                
            if self.object_sizes[drop] < 5:
                score += reduce(mul, (i in agent for i in object), 1)
            else:
                score += 0 if sum((i in object for i in agent)) else 1
                
        pygame.quit()
        
        return score