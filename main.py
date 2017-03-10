import random
import pygame
import sys
import time
import numpy as np
from pprint import pprint

from mqtt import mqtt

width, height = 500, 500
# connecteer met mqtt op host *.101 en poort 1883
mqttclient = mqtt("143.129.39.101", 1883)
screen = pygame.display.set_mode((width, height))

class Person:
    'Common base class for all employees'

    def __init__(self, xgiven, ygiven):
        generatedlikes = np.random.dirichlet(np.ones(3), size=1).transpose()
        self.x = xgiven
        self.y = ygiven
        self.redLike = generatedlikes[0]
        self.greenLike = generatedlikes[1]
        self.blueLike = generatedlikes[2]
        self.rect = pygame.Rect(self.x * 10, self.y * 10, 10, 10)

    def drawperson(self):
        if self.redLike >= self.blueLike and self.redLike >= self.greenLike:
            pygame.draw.rect(screen, (np.floor(255*self.redLike), 0, 0), self.rect)
        elif self.blueLike >= self.redLike and self.blueLike >= self.greenLike:
            pygame.draw.rect(screen, (0, np.floor(255*self.blueLike), 0), self.rect)
        elif self.greenLike >= self.blueLike and self.greenLike >= self.redLike:
            pygame.draw.rect(screen, (0, 0, np.floor(255*self.greenLike)), self.rect)

    def influence(self, neighbour):
        ran = random.uniform(0, 1)
        if neighbour.redLike >= neighbour.blueLike and neighbour.redLike >= neighbour.greenLike:
                influencefactor = (0.5 * neighbour.redLike) + (0.5 * ran)
                print("red dominate! NR:%f ran:%f I:%f R:%f B:%f G:%f" % (neighbour.redLike,ran,influencefactor,self.redLike,self.blueLike,self.greenLike))
                self.redLike = (0.5 * self.redLike) + (0.5 * influencefactor)
                self.blueLike -= (influencefactor / 4)
                self.greenLike -= (influencefactor / 4)
                print("red dominate! R:%f B:%f G:%f" % (self.redLike,self.blueLike,self.greenLike))


        elif neighbour.blueLike >= neighbour.redLike and neighbour.blueLike >= neighbour.greenLike:
                influencefactor = (0.5 * neighbour.blueLike) + (0.5 * ran)
                self.blueLike = (0.5 * self.blueLike) + (0.5 * influencefactor)
                self.redLike -= (influencefactor / 4)
                self.greenLike -= (influencefactor / 4)
        elif neighbour.greenLike >= neighbour.blueLike and neighbour.greenLike >= neighbour.redLike:
                influencefactor = (0.5 * neighbour.greenLike) + (0.5 * ran)
                self.greenLike = (0.5 * self.greenLike) + (0.5 * influencefactor)
                self.redLike -= (influencefactor / 4)
                self.blueLike -= (influencefactor / 4)

# Bereid scherm voor op visualisatie van automata
def visualize_dancefloor():
    pygame.init()
    crowd = [[0 for i in range(50)] for j in range(50)]
    for x in range(0, 50):
        for y in range(0, 50):
            crowd[x][y] = Person(x, y)
            crowd[x][y].drawperson()
    pygame.display.update()
    while 1:
        for x in range(0, 50):
            for y in range(0, 50):
                if x != 0 and y != 0:
                    crowd[x][y].influence(crowd[x - 1][y - 1])
                if x != 49 and y != 49:
                    crowd[x][y].influence(crowd[x + 1][y + 1])
                if x != 0 and y != 49:
                    crowd[x][y].influence(crowd[x - 1][y + 1])
                if x != 49 and y != 0:
                    crowd[x][y].influence(crowd[x + 1][y - 1])
                if y != 49:
                    crowd[x][y].influence(crowd[x][y + 1])
                if y != 0:
                    crowd[x][y].influence(crowd[x][y - 1])
                if x != 0:
                    crowd[x][y].influence(crowd[x - 1][y])
                if x != 49:
                    crowd[x][y].influence(crowd[x + 1][y])
                crowd[x][y].drawperson()
        pygame.display.update()
        time.sleep(0.1)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()


# Connecteer met Mqtt Host
def start_dj_listener():
    mqttclient.connect()
    mqttclient.add_listener_func(on_dj_message)


# Wordt opgeroepen wanneer er een Mqtt bericht binnenkomt
def on_dj_message(msg):
    print(msg)


# start_dj_listener()
visualize_dancefloor()
