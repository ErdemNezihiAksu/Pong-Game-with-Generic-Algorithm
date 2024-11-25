from generic_algo import *
import os

def create_window(root, training):
    pong_game = Pong(root,AIPlayer(1,2,1.2),AIPlayer(1,2,1.2),training)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # Calculate x and y position for the game window
    x = (screen_width // 2) - (600 // 2)  # 600 is the width of the game window
    y = (screen_height // 2) - (400 // 2)  # 400 is the height of the game window
    
    # Set the position of the game window
    root.geometry(f"600x400+{x}+{y}")
    return pong_game


def save_ai(best_ai : AIPlayer):
    with open("best_ai.txt", "w") as file:
        file.write(str(best_ai.reaction_speed) + "\n")
        file.write(str(best_ai.prediction_depth) + "\n")
        file.write(str(best_ai.aggression_level) + "\n")

def load_ai():
    params = []
    with open("best_ai.txt" , "r") as file:
        for line in file:
            params.append(float(line.strip()))
    return AIPlayer(params[0],params[1],params[2])

def main():
    pong_game = None
    best_ai = None

    if os.path.getsize("best_ai.txt"):
        while True:
            answer = input("Do you want to load the trained model? (Y/N) : ")
            if answer != 'Y' and answer != 'N':
                print("Invalid option !!")
            else:
                break
        if answer == 'Y':
            best_ai = load_ai()

    root = tk.Tk()
    pong_game = create_window(root, training= True)

    if best_ai == None:
        ga = GenericAlgorithm(root= root, pong_game= pong_game)
        num_generations = 3
        for gen in range(num_generations):
            print(f"Generation : {gen + 1}")
            ga.run_generation()

        best_ai = ga.best_ai
        save_ai(best_ai)
    
        print("\n --> Best AI has been created:")
        print(". reaction speed: ", best_ai.reaction_speed)
        print(". prediction depth: ", best_ai.prediction_depth)
        print(". aggresion level: ", best_ai.aggression_level, "\n")

    pong_game.set_trainig(False)
    pong_game.set_AIs(best_ai,best_ai)
    pong_game.reset_game()
    root.mainloop()

if __name__ == "__main__":
    main()