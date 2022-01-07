import threading

from src.DiGraph import DiGraph

from types import SimpleNamespace

from src.GameGUI import GameGUI
from src.GraphAlgo import GraphAlgo
from src.Node import Node
from src.client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *
import time

def main():
    # default port
    PORT = 6666
    # server host (default localhost 127.0.0.1)
    HOST = '127.0.0.1'

    client = Client()
    client.start_connection(HOST, PORT)

    diGraph = DiGraph()
    algoDiGraph = GraphAlgo(diGraph)
    startGame(algoDiGraph, client)

def getAgentsStart(graphAlgo) -> list:
    lst = []
    for agent in graphAlgo.get_graph().get_all_a().values():
        lst.append(agent.getPos())

    return lst

def startGame(graphAlgo:GraphAlgo, client):
    init_graph(graphAlgo.get_graph(), client)
    game = GameGUI(graphAlgo.get_graph(), client)
    # game.plot_graph() # debug
    client.start()
    saved = getAgentsStart(graphAlgo)
    # try:

    # try:
    while client.is_running() == 'true':
        update(graphAlgo, client)
        # game.update_graph(graphAlgo.get_graph())
        # choose next edge
        for index, agent in enumerate(graphAlgo.get_graph().get_all_a().values()):

            if agent.dest == -1:
                graphAlgo.PFL()

                if agent.onduty:
                    next_node = agent.list.pop()
                    client.choose_next_edge(
                        '{"agent_id":' + str(agent.getID()) + ', "next_node_id":' + str(next_node) + '}')
                    ttl = client.time_to_end()
                    print(ttl, client.get_info())


                    if(len(agent.list) == 0):
                        agent.onduty = False

                else:
                    # graphAlgo.get_graph().del_pokemon(agent)
                    if agent.pokemon and agent.pokemon.getPos() in graphAlgo.get_graph().get_all_p().keys():
                        graphAlgo.get_graph().del_pokemon(agent.pokemon)
                    graphAlgo.GBA3(agent)
            # if(saved[index] == agent.getPos()):
        client.move()
        game.draw()

            # saved[index] = agent.getPos()
    # except:
    #     print("Game over!")




def get_pokemons(graph, client):
    pokemons = json.loads(client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]
    # for p in pokemons:
    #     x, y, _ = p.pos.split(',')

    lst = []

    for id,p in enumerate(pokemons):
        x, y, _ = p.pos.split(',')
        p.pos = (float(x), float(y))
        lst.append(p.pos)

    delete = []

    for pok in graph.get_all_p().keys():
        if pok not in lst:
            pokemon = graph.get_pokemon(pok)
            delete.append(pokemon)

    for pok in delete:
        graph.del_pokemon(pok)

    for id, p in enumerate(pokemons):
        graph.add_pokemon(id, p.pos, p.value, p.type)

def update(algoGraph, client):
    diGraph = algoGraph.get_graph()
    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = (float(x), float(y))

    # draw agents
    for agent in agents:
        diGraph.getAgent(agent.id).setPos(agent.pos)
        (diGraph._agents[agent.id]).value = agent.value
        (diGraph._agents[agent.id]).src = agent.src
        (diGraph._agents[agent.id]).dest = agent.dest
        (diGraph._agents[agent.id]).speed = agent.speed

    diGraph.calc_bound()

    algoGraph.PFL()

    # diGraph.clearPokemons()
    get_pokemons(diGraph, client)
    algoGraph.PFL()

def init_graph(diGraph, client):
    graph_json = client.get_graph()

    graph = json.loads(
        graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))

    for n in graph.Nodes:
        x, y, _ = n.pos.split(',')
        n.pos = SimpleNamespace(x=float(x), y=float(y))

    info = json.loads(client.get_info(),
                        object_hook=lambda d: SimpleNamespace(**d)).GameServer
    agents = info.agents

    for i in range(agents):
        client.add_agent("{\"id\":%d}" % (i))

    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = (float(x), float(y))

    for id,n in enumerate(graph.Nodes):
        x = n.pos.x
        y = n.pos.y

        diGraph.add_node(id, (x, y))

    # draw edges
    for e in graph.Edges:

        diGraph.add_edge(e.src,e.dest,e.w)

    # draw agents
    for agent in agents:
        diGraph.add_agent(agent.id, agent.pos, agent.value, agent.src, agent.dest, agent.speed)

    diGraph.calc_bound()

    get_pokemons(diGraph, client)

if __name__ == '__main__':
    main()