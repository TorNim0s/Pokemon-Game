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
import math

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
    counter = 0
    # game.plot_graph() # debug
    client.start()
    ttl_global = client.time_to_end()
    total_send = ttl_global*10
    saved = getAgentsStart(graphAlgo)
    prev = float(ttl_global)/1000
    print(f"prev = {prev}")
    try:
        while client.is_running() == 'true':
            update(graphAlgo, client)
            for index, agent in enumerate(graphAlgo.get_graph().get_all_a().values()):

                if agent.dest == -1:

                    if agent.onduty:
                        next_node = agent.list.pop()
                        client.choose_next_edge(
                            '{"agent_id":' + str(agent.getID()) + ', "next_node_id":' + str(next_node) + '}')
                        ttl = client.time_to_end()
                        # print(ttl, client.get_info())
                        if len(agent.list) == 0:
                            time_to_pokemon = calc(agent, graphAlgo, next_node)
                            t = threading.Thread(target=calc_Pokemon_To_Agent, args=[graphAlgo, agent, time_to_pokemon, next_node])
                            t.start()


                        if(len(agent.list) == 0):
                            agent.onduty = False

                    else:
                        if agent.pokemon and agent.pokemon.getPos() in graphAlgo.get_graph().get_all_p().keys() and agent.pokemon.occupide:
                            agent.pokemon.occupide = False
                            graphAlgo.get_graph().del_pokemon(agent.pokemon)
                        graphAlgo.GBA3(agent)
            ttl = client.time_to_end()
            game.draw()
            if(prev - float(ttl)/1000 >= 0.1):
                client.move()
                prev = float(ttl)/1000
    except:
        print("GameOver!")
    print("GameOver!")

def calc_Pokemon_To_Agent(graph:GraphAlgo, agent, time, dest):
    pygame.time.wait(math.ceil(time))

    agent.onduty = False
    agent.src = dest
    graph.GBA3(agent)

def calc(agent, graph:GraphAlgo, node):
    src = agent.src
    dst = node
    weight = graph.get_graph().getWeight(src, dst)
    src_pos = graph.get_graph().getNode(src).getPos()
    dst_pos = graph.get_graph().getNode(dst).getPos()
    pok_pos = agent.pokemon.getPos()

    dist_src_dst = math.sqrt(pow(src_pos[0] - dst_pos[0], 2) + pow(src_pos[1] - dst_pos[1], 2))
    dist_src_pok = math.sqrt(pow(src_pos[0] - pok_pos[0], 2) + pow(src_pos[1] - pok_pos[1], 2))

    return ((dist_src_pok/dist_src_dst) * weight)/agent.speed

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

    # algoGraph.PFL()

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