# game-ai-project

This is my first game-ai project. Game is simple, when you face with obstacle you need to jump or slide. With using genetic algorithm, I tried to teach an AI to beat the game. To do this, I used NEAT algorithm.

## In-Game

![ezgif com-gif-maker](https://user-images.githubusercontent.com/76682003/134256883-731051e8-ba89-4a0c-8357-62735248a00f.gif)

### Genetic Algorithm

Genetic Algorithm is a type of Reinforcement Learning method which basically works like evolution in nature. It creates a number of species and for each creation, the algorithm classifies the species to one generation number. After creating a generation of species, the algorithm releases the species to the environment. Each species has its own Neural Network, and each species will be made decisions via this Neural Network. After releasing the species to the environment and waiting for the interaction between the environment and species, the algorithm classifies the species as good or bad in terms of fitting to the environment. The algorithm does this with a pre-defined fitness function which is a function to measure how fitted a species is in the environment. After ranking the species by their fitness score, the algorithm chooses the best species and lets them reproduce. With reproducing the best species, the algorithm creates a second generation with a little bit of variance and mutation. The algorithm repeats this process until it finds the best-fitted species.

### NEAT

NEAT docs : https://neat-python.readthedocs.io/en/latest/

NEAT is a genetic algorithm written in Python. The main difference NEAT has to other genetic algorithms is, the mutations can happen not just weights of connections in the Neural Network, It can happen also like; adding new nodes, new connections, and changing the weights of connections as well.

## In-Game-AI

In game there is 3 levels. In level one, you need to jump over obstacles. In level two, you need to slide under obstacles. And in level three, obstacles created randomly.

* In level one, AI easily learns how to jump in a few generations.

![ezgif com-gif-maker (1)](https://user-images.githubusercontent.com/76682003/134261115-1fa486fb-fe67-4566-a10f-84ced02176df.gif)


* But in level two, AI struggles to learn when to press slide over 100+ generations.

![ezgif com-gif-maker (2)](https://user-images.githubusercontent.com/76682003/134261298-72689c4e-fce7-4c17-a57d-96ee2f319cd9.gif)


* At generation 151, AI finally learns when to jump and when to slide.

![ezgif com-gif-maker (3)](https://user-images.githubusercontent.com/76682003/134261358-f2521d87-3697-420e-b685-5144aa095e3f.gif)

