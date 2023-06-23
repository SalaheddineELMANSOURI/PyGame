import pygame
from pygame.locals import *

class robot:
    def __init__(self, nom,line, path, speed, image):
        self.nom = nom #nom du robot
        self.line = line # hauteur de line D'écriture msg
        self.path = path # trajet du robot
        self.speed = speed # vitess du robot
        self.image=image # image du robot
        self.pos_act = path[0] #tableau des paths
        self.rect = pygame.Rect(self.pos_act[0], self.pos_act[1], 25, 25) #dessin des robots
        self.pos_act_index = 0
        self.retour = False
        self.charged = False
        self.j=0 # timer
       
    def deplacement(self):
        if self.pos_act_index < len(self.path) - 1:
            next_pos = self.path[self.pos_act_index + 1]
            if self.rect.topleft == next_pos:
                self.pos_act_index += 1
            else:
                dx = dy = 0
                if self.pos_act[0] < next_pos[0]:
                    dx = self.speed
                elif self.pos_act[0] > next_pos[0]:
                    dx = -self.speed
                elif self.pos_act[1] < next_pos[1]:
                    dy = self.speed
                elif self.pos_act[1] > next_pos[1]:
                    dy = -self.speed
                self.pos_act = (self.pos_act[0] + dx, self.pos_act[1] + dy)
                self.rect.move_ip(dx, dy)

        else:
            if not self.retour:
                self.retour = True
                self.pos_act_index = len(self.path) - 2 # retour -1
                self.path.reverse()
            else:
                self.retour = False
                self.pos_act_index = 0
            self.path.reverse()
           
    def charge(self,screen, space):
            pygame.font.init()
            font = pygame.font.Font(None, 36)
            text = font.render(f"Chargement du {self.nom}", True, (0, 0, 0))#text déchargement
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, (screen.get_height() // 2 - text.get_height() // 2) + space))#affichae des texts 
            self.j+=1    # timer commence
            if (self.j==100): self.pos_act_index=0;self.j=0;self.path.reverse();self.charged = True; # arret lorsque charge = true
      
    def decharge(self, screen, space):  
        pygame.font.init()
        font = pygame.font.Font(None, 36)
        text = font.render(f"Dechargement du {self.nom}", True, (0, 0, 0))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, (screen.get_height() // 2 - text.get_height() // 2) + space))
        self.j+=1    
        if (self.j==100): self.pos_act_index=0;self.j=0;self.path.reverse();self.charged = False; # arret lorsque dcharge = true -> charge=false
        
    def is_colliding(self, robots, screen):
        pygame.font.init()
        font = pygame.font.Font(None, 36)
        
        for i, robot in enumerate(robots):
            robotRect = self.rect
            if robot != self and robotRect.colliderect(robot.rect):
                if i % 2 == 0:
                    robots[i].speed = 0
                    collision_sound = pygame.mixer.Sound("audio/collision.mp3")
                    pygame.mixer.Sound.play(collision_sound)
                    pygame.mixer.music.stop()
                text = font.render(f"Collision du {self.nom}", True, (0, 0, 0))
                screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))
                      
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        