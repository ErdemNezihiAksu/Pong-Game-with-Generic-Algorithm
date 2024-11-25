#Pong Main.py
This is the main file that you should run. By default, there are trained model's parameters in the best_ai.txt . So it is going to ask you whether you want to just play against it or train a new AI.

#Pong Game.py
This file sets up the game environment using tkinter library

#Generic Algo.py
This is the file to train an AI model. Algorithm follows these steps:

##- Creating Random AI player:
  The first generation is created with random parameters. Depending on their performance, the best ones are going to be chosen to create the next generations.

##- Simulate Games:
  This is the part where we evaulate each model of the generation. They all play the game against a competatior. We can wacth these games, and keep track of their performance in the meantime.

##- Breed Next Generation:
  According to their performance, we choose the top 5 models to breed the next generation.

##- Apply Mutation:
  To create variety, we apply random mutations to random models.

##- Repeat the process:
  By default, we run 3 generations, but you can change it as you wish by changing "num_generations" parameter in the main file.
