import json
import random
from types import SimpleNamespace

import matplotlib.pyplot as plt
from pygame import gfxdraw
from pygame import *
import pygame


from src.DiGraph import DiGraph

# init pygame
WIDTH, HEIGHT = 1080, 720

pokeball_path = "..\\imgs\\Pokeball.png"

class GameGUI():
    def __init__(self, graph:DiGraph, client):
        pygame.init()
        self._graph = graph
        self.client = client
        self.screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 20, bold=True)
        self.exit_button = Button((255, 0, 0), 0, 0, 50, 50, 'Stop')

    def update_graph(self, graph):
        self._graph = graph

    def plot_graph(self) -> None: # debug watch
        for src in self._graph.get_all_v().values():
            x, y = random.randint(5, 25), random.randint(5, 25)
            if src.getPos():
                x, y = src.getPos()
            else:
                src.setPos((x, y))

            plt.plot(x, y, markersize=10, marker="o", color="blue")
            plt.text(x, y, str(src.getID()), color="red", fontsize=12)
            for dst in self._graph.all_out_edges_of_node(src.getID()).keys():

                x2, y2 = random.randint(5, 25), random.randint(5, 25)
                if self._graph.getNode(dst).getPos():
                    x2, y2 = src.getPos()
                else:
                    self._graph.getNode(dst).setPos((x2, y2))

                x2, y2 = self._graph.getNode(dst).getPos()
                plt.annotate("", xy=(x, y), xytext=(x2, y2), arrowprops=dict(arrowstyle="<-"))

        for pokemon in self._graph.get_all_p().values():
            x, y = pokemon.getPos()
            plt.plot(x, y, markersize=10, marker="o", color="red")
            plt.text(x, y, pokemon.name, color="black", fontsize=14)

        for agent in self._graph.get_all_a().values():
            x, y = agent.getPos()
            plt.plot(x, y, markersize=12, marker="o", color="black")
            plt.text(x, y, "Agent", color="black", fontsize=14)

        plt.show()

    def draw(self):
        # check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.VIDEORESIZE:
                surface = pygame.display.set_mode((event.w, event.h),
                                                  pygame.RESIZABLE)
            if event.type == pygame.MOUSEBUTTONDOWN:  # If the 'Stop' button was pressed, "gently" stop the program
                pos = pygame.mouse.get_pos()
                if self.exit_button.is_over(pos):
                    self.client.stop_connection()
                    pygame.quit()
                    exit(0)

        self.screen.fill(Color(0, 0, 0))
        self.exit_button.draw(self.screen)
        info = pygame.display.Info()
        bg = pygame.image.load("..\\imgs\\background.png")
        bg = pygame.transform.scale(bg, (info.current_w, info.current_h))
        self.screen.blit(bg, (0, 0))

        for src, node in self._graph.get_all_v().items():
            x = self.my_scale(node.getPos()[0], x=True)
            y = self.my_scale(node.getPos()[1], y=True)

            agentImg = pygame.image.load(pokeball_path)
            agentImg = pygame.transform.scale(agentImg, (30, 30))
            rect = agentImg.get_rect()
            rect = rect.move((x-15, y-15))
            self.screen.blit(agentImg, rect)

            for dst, weight in self._graph.all_in_edges_of_node(src).items():
                dstNode = self._graph.getNode(dst)

                src_x = self.my_scale(node.getPos()[0], x=True)
                src_y = self.my_scale(node.getPos()[1], y=True)
                dest_x = self.my_scale(dstNode.getPos()[0], x=True)
                dest_y = self.my_scale(dstNode.getPos()[1], y=True)

                pygame.draw.line(self.screen, Color(61, 72, 126),
                                 (src_x, src_y), (dest_x, dest_y))

        for pokemon in self._graph.get_all_p().values():
            x = self.my_scale(pokemon.getPos()[0], x=True)
            y = self.my_scale(pokemon.getPos()[1], y=True)
            pokImg = pygame.image.load(pokemon.path)
            pokImg = pygame.transform.scale(pokImg, (30, 30))
            rect = pokImg.get_rect()
            rect = rect.move((x-15, y-15))
            self.screen.blit(pokImg, rect)

            id_srf = self.font.render(pokemon.name, True, Color(255, 255, 255))
            rect = id_srf.get_rect(center=(x+15, y-20))
            self.screen.blit(id_srf, rect)

        for agent in self._graph.get_all_a().values():
            x = self.my_scale(agent.getPos()[0], x=True)
            y = self.my_scale(agent.getPos()[1], y=True)

            agentImg = pygame.image.load(agent.path)
            agentImg = pygame.transform.scale(agentImg, (50, 50))
            rect = agentImg.get_rect()
            rect = rect.move((x-25, y-25))
            self.screen.blit(agentImg, rect)

            name_header = f"Name: {agent.name}"
            speed_header = f"Speed: {agent.speed}"

            id_srf = self.font.render(name_header, True, Color(255, 255, 255))
            rect = id_srf.get_rect(center=(x, y-55))
            self.screen.blit(id_srf, rect)
            id_srf2 = self.font.render(speed_header, True, Color(255, 255, 255))
            rect = id_srf2.get_rect(center=(x, y -35))
            self.screen.blit(id_srf2, rect)

        self.header_display()

        # update screen changes
        display.update()

        # refresh rate
        self.clock.tick(60)

    def header_display(self):
        # draw the node id
        ttl = float(self.client.time_to_end())/1000
        info = json.loads(self.client.get_info(),
                          object_hook=lambda d: SimpleNamespace(**d)).GameServer
        headerTime = f"Time left: {(str(ttl))}"
        headerMoves = f"Moves: {info.moves}"
        headerGrade = f"Grade: {info.grade}"

        id_srf = self.font.render(headerTime, True, Color(255, 255, 255))
        id_srf2 = self.font.render(headerMoves, True, Color(255, 255, 255))
        id_srf3 = self.font.render(headerGrade, True, Color(255, 255, 255))
        x = self.screen.get_width() / 20
        y = self.screen.get_height() / 20
        self.screen.blit(id_srf, (x,y))
        self.screen.blit(id_srf2, (x, y+25))
        self.screen.blit(id_srf3, (x, y+50))


    def scale(self, data, min_screen, max_screen, min_data, max_data):
        """
        get the scaled data with proportions min_data, max_data
        relative to min and max screen dimentions
        """
        return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen

    def my_scale(self, data, x=False, y=False):
        if x:
            return self.scale(data, 50, self.screen.get_width() - 50, self._graph.bound["min_x"], self._graph.bound["max_x"])
        if y:
            return self.scale(data, 50, self.screen.get_height() - 50, self._graph.bound["min_y"], self._graph.bound["max_y"])

class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 20)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False