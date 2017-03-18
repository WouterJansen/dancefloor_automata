import random
import pygame
import sys
import numpy as np

from mqtt import mqtt

width, height = 500, 500
mqttclient = mqtt("broker.hivemq.com", 1883)
crowd = [[0 for i in range(width // 10)] for j in range(height // 10)]


class Person:

    def __init__(self, xgiven, ygiven):
        generatedlikes = np.random.dirichlet(np.ones(3), size=1).transpose()
        self.x = xgiven
        self.y = ygiven
        self.redLike = generatedlikes[0]
        self.greenLike = generatedlikes[1]
        self.blueLike = generatedlikes[2]
        self.rect = pygame.Rect(self.x * 10, self.y * 10, 10, 10)

    def drawperson(self, screen):
        if self.redLike >= self.blueLike and self.redLike >= self.greenLike:
            pygame.draw.rect(screen, (np.floor(255 * self.redLike), 0, 0), self.rect)
        elif self.blueLike >= self.redLike and self.blueLike >= self.greenLike:
            pygame.draw.rect(screen, (0, np.floor(255 * self.blueLike), 0), self.rect)
        elif self.greenLike >= self.blueLike and self.greenLike >= self.redLike:
            pygame.draw.rect(screen, (0, 0, np.floor(255 * self.greenLike)), self.rect)

    def influence(self, neighbour):
        #print("1 r %f b %f g %f", (self.redLike, self.blueLike, self.greenLike))
        if neighbour.redLike >= neighbour.blueLike and neighbour.redLike >= neighbour.greenLike:
            #print("1")
            influencefactor = (0.5 * neighbour.redLike) + (0.5 * random.uniform(0, 1))
            self.redLike = (0.5 * self.redLike) + (0.5 * influencefactor)
            self.blueLike -= (influencefactor / 4)
            self.greenLike -= (influencefactor / 4)
            self.blueLike = np.abs(self.blueLike)
            self.greenLike = np.abs(self.greenLike)
            # if self.blueLike < 0:
            #     self.greenLike += self.blueLike
            #     if self.greenLike < 0:
            #         self.greenLike = 0
            #     self.blueLike = 0
            # elif self.greenLike < 0:
            #     self.blueLike += self.greenLike
            #     if self.blueLike < 0:
            #         self.blueLike = 0
            #     self.greenLike = 0
        elif neighbour.blueLike >= neighbour.redLike and neighbour.blueLike >= neighbour.greenLike:
            #print("2")
            influencefactor = (0.5 * neighbour.blueLike) + (0.5 * random.uniform(0, 1))
            self.blueLike = (0.5 * self.blueLike) + (0.5 * influencefactor)
            self.redLike -= (influencefactor / 4)
            self.greenLike -= (influencefactor / 4)
            self.redLike = np.abs(self.redLike)
            self.greenLike = np.abs(self.greenLike)
            # if self.redLike < 0:
            #     self.greenLike += self.redLike
            #     if self.greenLike < 0:
            #         self.greenLike = 0
            #     self.redLike = 0
            # elif self.greenLike < 0:
            #     self.redLike += self.greenLike
            #     if self.redLike < 0:
            #         self.redLike = 0
            #     self.greenLike = 0
        elif neighbour.greenLike >= neighbour.blueLike and neighbour.greenLike >= neighbour.redLike:
            #print("3")
            influencefactor = (0.5 * neighbour.greenLike) + (0.5 * random.uniform(0, 1))
            self.greenLike = (0.5 * self.greenLike) + (0.5 * influencefactor)
            self.redLike -= (influencefactor / 4)
            self.blueLike -= (influencefactor / 4)
            self.redLike = np.abs(self.redLike)
            self.blueLike = np.abs(self.blueLike)
            # if self.redLike < 0:
            #     self.blueLike += self.redLike
            #     if self.blueLike < 0:
            #         self.blueLike = 0
            #     self.redLike = 0
            # elif self.blueLike < 0:
            #     self.redLike += self.blueLike
            #     if self.redLike < 0:
            #         self.redLike = 0
            #     self.blueLike = 0
        #print("2 r %f b %f g %f", (self.redLike, self.blueLike, self.greenLike))

    def sendOpinion(self, msg):
        if msg == "Rock":
            if self.redLike >= self.blueLike and self.redLike >= self.greenLike:
                mqttclient.publish("dancefloor/vote/", "Like")
            else:
                mqttclient.publish("dancefloor/vote/", "Dislike")
        elif msg == "Pop":
            if self.greenLike >= self.redLike and self.greenLike >= self.blueLike:
                mqttclient.publish("dancefloor/vote/", "Like")
            else:
                mqttclient.publish("dancefloor/vote/", "Dislike")
        elif msg == "Techno":
            if self.blueLike >= self.redLike and self.blueLike >= self.greenLike:
                mqttclient.publish("dancefloor/vote/", "Like")
            else:
                mqttclient.publish("dancefloor/vote/", "Dislike")


def visualize_dancefloor():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    for x in range(0, width // 10):
        for y in range(0, height // 10):
            crowd[x][y] = Person(x, y)
            crowd[x][y].drawperson(screen)
    pygame.display.update()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        for x in range(0, width // 10):
            for y in range(0, height // 10):
                # if x != 0 and y != 0:
                #     crowd[x][y].influence(crowd[x - 1][y - 1])
                # if x != width // 10 - 1 and y != height // 10 - 1:
                #     crowd[x][y].influence(crowd[x + 1][y + 1])
                # if x != 0 and y != height // 10 - 1:
                #     crowd[x][y].influence(crowd[x - 1][y + 1])
                # if x != width // 10 - 1 and y != 0:
                #     crowd[x][y].influence(crowd[x + 1][y - 1])
                if x != width // 10 - 1:
                    crowd[x][y].influence(crowd[x + 1][y])
                if y != height // 10 - 1:
                    crowd[x][y].influence(crowd[x][y + 1])
                if x != 0:
                    crowd[x][y].influence(crowd[x - 1][y])
                if y != 0:
                    crowd[x][y].influence(crowd[x][y - 1])
                crowd[x][y].drawperson(screen)
        pygame.display.update()


def start_dj_listener():
    mqttclient.connect()
    mqttclient.add_listener_func(on_dj_message)


def on_dj_message(msg):
    if msg == "Rock":
        print("DJ koos Rock muziek")
    elif msg == "Pop":
        print("DJ koos Pop muziek")
    elif msg == "Techno":
        print("Dj koos Techno muziek")
    for x in range(0, width // 10):
        for y in range(0, height // 10):
            crowd[x][y].sendOpinion(msg)


start_dj_listener()
visualize_dancefloor()
