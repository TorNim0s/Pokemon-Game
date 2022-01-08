# Pokemon-Game - Python
![](https://cdn.europosters.eu/image/1300/posters/pokemon-eevee-i32673.jpg)

**Created by Eldad Tsemach, Ilan Sirisky and Nir Meir**


# Table of Contents
1. [About the Project](#About)
2. [The Algorithm](#algorithm)
3. [Code Description](#code)
4. [GUI](#gui)
5. [How to Run](#run)
6. [Results](#results)
7. [Dependencies](#dependencies)
8. [UML](#uml)

## About the Project <a name="About"></a>
This is task 4 in our OOP course.

It is based on our Directed Weighted Graph Tasks we did before on the course. So we used our implementation from the tasks before.
[Ex2 - Directed Weighted Graph - Java](https://github.com/TorNim0s/Directed-Weighted-Grapth) , 
[Ex3 - Directed Weighted Graph - Python](https://github.com/TorNim0s/Directed-Weighted-Graph-Python)

Here we recieve a DW Graph, number of agents and pokemons.
With a mission to "catch" as many pokemons as we can within a given time limit for each stage.

[Link to main assignment](https://github.com/benmoshe/OOP_2021/tree/main/Assignments/Ex4)


## he Algorithm <a name="algorithm"></a>
The algorithm goes a follows:
 - We send each agent to a "mission".
 - Each "mission" checks if there any pokemons that don't have any agent assigned to them.
 - Based on the pokemons that are not chosen already by another agent, we choose the best pokemon we can catch.
   - How we choose who's the best pokemon to catch, for each pokemon:
   - We calculate the shortest path to the pokemon using the TSP algorithm from the last task.
   - Calculating the time it takes the agent to reach the pokemon by diving the distance with his speed.
   - Then we divide the the time with the value of the pokemon.
   - And lastly we choose the the pokemon with the lowest "weight" and send the agent towards that pokemon.


## Code Description <a name="code"></a>
- `Node.py` : Implements and represents the vertices of the graph.
- `Edge.py`: Implements and represents the edges of the graph.
- `Pokemon.py` : Implements the pokemons that show up on the graph.
- `Agent.py` : Implements the agents that try to catch the pokemons.
- `DiGraph.py`: Implements the graph itself, contains lists of all vertices, agents and pokemons.
- `GraphAlgo.py`: Implements the algorithm that is listed above.
  - `TSP`, `DijakstraAlgo`, `ShortestPath`, `GBA` - get best agent, `FPL` - find pokemon location.
- `Client.py` : Given to us with the assignment, contains function to move the agents and make/close connection with the server.
- `GameGUI.py` : Creates the GUI for the game.
- `Game.py` : The main class for this project, initializes the graph, starts the game, controls the agents.


## GUI Example <a name="gui"></a>
Example from case 11:

![](https://i.imgur.com/IZG769q.png)

- The agents represent the agents with random names.
- The pokemons represent the various types of pokemons.
- In the top left corner we have:
   - The remaning time for the game.
   - The amount of moves we made.
   - Our grade for the game which is based on the number of pokemons we caught.
   - A stop button, to stop the game gracefully.

## How to Run <a name="run"></a>
Firstly, to run this project, download the files from the github.

Secondly, Open the cmd in the project folder and write `java -jar Ex4_Server_v0.0.jar 0`, where the last 0 is number of the cases, input a numer between [0-15].

Lastly, run the `Game.py` from your IDE with python 3.9 interpeter.

## Results <a name="results"></a>
Results for the cases we got
|Case|Moves|Grade|Numer of Agents|
|---------|---------|---------|---------|
|0|269|147|1|
|1|545|442|1|
|2|273|269|1|
|3|544|644|1|
|4|276|289|1|
|5|551|785|1|
|6|272|79|1|
|7|541|396|1|
|8|273|173|1|
|9|544|479|1|
|10|270|125|1|
|11|555|1648|3|
|12|274|40|1|
|13|542|292|2|
|14|270|208|3|
|15|549|310|1|

## Dependencies <a name="dependencies"></a>
This project is using Python version `3.9`.

We are using Matplotlib version `3.5.1` in order to debug the graph.

The GUI uses Pygame version `2.1.2`.

## UML <a name="uml"></a>
![](https://i.imgur.com/J5GiUSy.png)
