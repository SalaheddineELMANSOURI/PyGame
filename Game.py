# 1 - Import packages
import pygame
from pygame.locals import *
import sys
from robot import *

# Definition des Couleurs
Blanc = (255, 255, 255)

# definition des dimmension
Width = 640
Height = 480

# definition des ticks
Tick = 20

# definition des images
robot_img = pygame.image.load('img/Mini-Robot.png')
background = pygame.image.load('img/background.png')
warehouse = pygame.image.load('img/warehouse.png')

# formatage d arriere plan selon dimension du frame
background = pygame.transform.scale(background, (Width, Height))



class Game:
    def __init__(self):
        # Initialisation du jeu
        pygame.init()

        # demarage du fenetre
        self.window = pygame.display.set_mode((Width, Height))
        pygame.display.set_caption('Automatic Robots with collision detection ')
        # Definition des chemin pour les robots
        self.path1 = [(270,15), (270,145), (440,145),(440,330),(210,330),(210,435)] # index0:(270,15) index1:(270,145)...
        self.path2 = [(570,0),(470,0),(470,250),(50,250)]
        self.path3 = [(30,10),(30,100),(350,100),(350,295),(570,300)]

        # liste des robots
        self.robots = [
            robot("robot 1", 0,self.path1,5,robot_img), 
            robot("robot 2",20,self.path2,5,robot_img),
            robot("robot 3",40,self.path3,5,robot_img),    
        ]

    def draw_paths(self):
        pygame.draw.line(self.window,Blanc,[30,30],[30,120],1)
        pygame.draw.line(self.window,Blanc,[30,120],[350,120],1)
        pygame.draw.line(self.window,Blanc,[350,120],[350,315],1)
        pygame.draw.line(self.window,Blanc,[350,315],[580,315],1)
        pygame.draw.line(self.window,Blanc,[280,30],[280,160],1)
        pygame.draw.line(self.window,Blanc,[280,160],[450,160],1)
        pygame.draw.line(self.window,Blanc,[450,160],[450,350],1)
        pygame.draw.line(self.window,Blanc,[450,350],[220,350],1)
        pygame.draw.line(self.window,Blanc,[220,350],[220,450],1)
        pygame.draw.line(self.window,Blanc,[580,15],[480,15],1)
        pygame.draw.line(self.window,Blanc,[480,15],[480,265],1)
        pygame.draw.line(self.window,Blanc,[480,265],[60,265],1)

    def run(self):
        elapsed_time = 0
        clock = pygame.time.Clock()
        # boucle Pygame
        while True:

            # verification des evenement
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # application d image d arriere plan
            self.window.blit(background, (0,0))
            
            # warehouse de depart 
            self.window.blit(warehouse, (0,0))
            self.window.blit(warehouse, (250,0))
            self.window.blit(warehouse, (580,0))
            
            # warehouse d'arrive
            self.window.blit(warehouse, (580,300))
            self.window.blit(warehouse, (200,450))
            self.window.blit(warehouse, (0,250))
            
            # line du robot
            self.draw_paths()

            current_time = pygame.time.get_ticks()
            if current_time - elapsed_time >= 3050:
                elapsed_time = current_time
                for i, _ in enumerate(self.robots):
                    self.robots[i].speed = 5

            
            # affichage des robots
            for robot in self.robots:
                robot.draw(self.window)

            for robot in self.robots:
                robot.is_colliding(self.robots, self.window)#robots qui ont fait collision
                
                if robot.pos_act_index < len(robot.path) - 1:
                                                                    #déplacement
                    robot.deplacement()

                else:
                    if robot.charged:
                        robot.decharge(self.window, robot.line)
                    else:
                        robot.charge(self.window, robot.line)

            # 11 - Update the window
            pygame.display.update()

            # 12 - Slow things down a bit
            clock.tick(Tick)  # make pygame wait
