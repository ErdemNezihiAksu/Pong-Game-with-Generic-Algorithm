This is a generic AI model that learns how to play the famous game **Pong**.

# Pong Main.py
This is the main file that you should run. By default, there are trained model's parameters in the best_ai.txt . So it is going to ask you whether you want to just play against it or train a new AI. If you choose to train, you will watch the training process, how AI models play the game against each other, and their overall score at each game. Running this file is enough to start the project.

## Requirements
- Tkinter

# Pong Game.py
This file sets up the game environment using tkinter library

# Generic Algo.py
This is the file to train an AI model. Algorithm follows these steps:

## - Creating Random AI player:
  The first generation is created with random parameters. Depending on their performance, the best ones are going to be chosen to create the next generations.

  ![Screenshot 2025-01-25 at 09 29 46](https://github.com/user-attachments/assets/d71bb293-8b47-47d7-ba63-a49b08452e49)

## - Simulate Games:
  This is the part where we evaulate each model of the generation. They all play the game against a competatior. We can wacth these games, and keep track of their performance in the meantime.
  
  ![Screenshot 2025-01-25 at 09 30 12](https://github.com/user-attachments/assets/c3f2b854-fa00-41d7-946a-637b711179b9)
  ![Screenshot 2025-01-25 at 09 31 13](https://github.com/user-attachments/assets/b07d4038-7ecf-4a8e-a793-b6309d431284)

## - Breed Next Generation:
  According to their performance, we choose the top k models to breed the next generation.

  ![Screenshot 2025-01-25 at 09 31 23](https://github.com/user-attachments/assets/8ce72862-1405-458c-9471-fd25bb6b3856)

## - Apply Mutation:
  To create variety, we apply random mutations to random models.

## - Repeat the process:
  By default, we run 3 generations, but you can change it as you wish by changing "num_generations" parameter in the main file.

## - Conclusion:
  The best AI is saved and now you can start playing against it.
  
  ![Screenshot 2025-01-25 at 09 34 54](https://github.com/user-attachments/assets/cb30f25e-0622-4af0-a78e-56b9befc9108)
