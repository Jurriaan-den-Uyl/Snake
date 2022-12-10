import os
import pygame
import random

os.environ['SDL_VIDEO_CENTERED'] = '1'

class GameState():
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.x = 120
        self.y = 120
        self.snake_head = [self.x,self.y]
        self.snake_list = [[self.x,self.y],[self.x-20,self.y],[self.x-40,self.y]]
        self.applex = random.choice(range(0,620, 20))
        self.appley = random.choice(range(0,460, 20))
        self.apple = False
        self.stop = False
        
    def update(self,moveCommandX,moveCommandY):
        self.snake_head[0] += moveCommandX
        self.snake_head[1] += moveCommandY
        self.snake_list.insert(0,[self.snake_head[0],self.snake_head[1]])
        if self.apple == False:
            self.snake_list.pop()
        else:
            self.apple = False
    
    def generateApple(self):
        self.applex = random.choice(range(0,620, 20))
        self.appley = random.choice(range(0,460, 20))
    
    def eating(self):
        if self.snake_head[0] == self.applex and self.snake_head[1] == self.appley:
            self.apple = True
            self.generateApple()
            
    def collision(self):
        if self.snake_head[0] <= -20 or self.snake_head[0] >= 640 or self.snake_head[1] <= -20 or self.snake_head[1] >= 480:
            self.stop = True
        elif self.snake_head in self.snake_list[1:]:
            self.stop = True
        else:
            pass
        
class Game():
    def __init__(self):
        self.reset()
        self.gameState.reset()
    
    def reset(self):
        pygame.init()
        self.window = pygame.display.set_mode((640,480))
        pygame.display.set_caption("Snek")
        pygame.display.set_icon(pygame.image.load("logo32x32.png"))
        self.gameState = GameState()
        self.clock = pygame.time.Clock()
        self.moveCommandX = 20
        self.moveCommandY = 0  
        self.running = True

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                elif event.key == pygame.K_d and self.moveCommandX != -20:
                    self.moveCommandX = 20
                    self.moveCommandY = 0
                elif event.key == pygame.K_a and self.moveCommandX != 20:
                    self.moveCommandX = -20
                    self.moveCommandY = 0
                elif event.key == pygame.K_s and self.moveCommandY != -20:
                    self.moveCommandY = 20
                    self.moveCommandX = 0
                elif event.key == pygame.K_w and self.moveCommandY != 20:
                    self.moveCommandY = -20
                    self.moveCommandX = 0
                elif event.key == pygame.K_SPACE and self.gameState.stop == True:
                    self.reset()
                    self.gameState.stop = False

    def pause(self):
        if self.gameState.stop == False:
            self.clock.tick(10)
        else:
            number_image =  pygame.font.SysFont( None, 32 ).render( f"Your snake was {len(self.gameState.snake_list)} long. Play again? Press SPACE", True, (255,255,255), (0,0,0))
            text_rect_obj = number_image.get_rect()
            text_rect_obj.center = (320, 150)
            self.window.blit(number_image, text_rect_obj)
            pygame.display.update()
            pygame.time.delay(500)
            # pygame.event.wait()
            # while True:
                # event = pygame.event.wait()
                # if event.type == pygame.QUIT:
                    # self.running = False
                    # break
                # elif event.type == pygame.KEYDOWN:
                    # if event.key == pygame.K_SPACE:
                        # print("test")
                        # self.reset()
                        # self.gameState.stop = False

    def update(self):
        self.gameState.update(self.moveCommandX,self.moveCommandY)
        self.gameState.eating()
        self.gameState.collision()

    def render(self):
        self.window.fill((0,0,0))
        for i in range(0, len(self.gameState.snake_list)):
            x = self.gameState.snake_list[i][0]
            y = self.gameState.snake_list[i][1]
            pygame.draw.rect(self.window,(255,255,255),(x,y,20,20))
        applex = self.gameState.applex
        appley = self.gameState.appley
        pygame.draw.rect(self.window,(0,255,0),(applex,appley,20,20))
        pygame.display.update()    

    def run(self):    
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.pause()

game = Game()
game.run()
pygame.quit()