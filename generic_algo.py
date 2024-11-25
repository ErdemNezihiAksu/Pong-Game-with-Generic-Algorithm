import random
from pong_game import *
    
class GenericAlgorithm:
    def __init__(self, root: tk.Tk, pong_game: Pong, population_size=10, mutation_rate=0.1):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.eval_params = []
        self.pong_game = pong_game
        self.root = root
        self.population = [self.create_random_ai() for _ in range(population_size)]
        self.best_ai = None

    def create_random_ai(self):
        return AIPlayer(
            reaction_speed=random.uniform(1, 2),
            prediction_depth=random.uniform(1, 5),
            aggression_level=random.uniform(0.5, 2)
        )

    def run_generation(self):
        results = []
        print("-- Current Population: ")
        oponent_ai = self.create_oponent_ai()
        self.print_AIs(oponent_ai)
        print("Training Starts...")

        for ai, i in zip(self.population,range(self.population_size)):
            print(f"\n--- AI number {i + 1} ...")
            score = self.simulate_games(ai, oponent_ai)
            results.append((score, ai, i + 1))

        results.sort(reverse=True, key=lambda x: x[0])
        self.best_ai = results[0][1]
        self.breed_next_generation(results[:5])

    def simulate_games(self, ai:AIPlayer, oponent_ai:AIPlayer):
        self.pong_game.set_AIs(ai,oponent_ai)
        self.pong_game.auto_restart()
        self.root.mainloop()
        self.eval_params = self.pong_game.get_eval_params()
        print("...evaluation parameters: ", self.eval_params)
        score_left = self.eval_params[0]* 1.5  + self.eval_params[1] * 0.01
        score_right = self.eval_params[2] * 1.5 + self.eval_params[3] * 0.01
        if score_left == 0 and score_right == 0:
            score_left = ai.reaction_speed * ai.aggression_level * 0.001 + ai.prediction_depth
            score_right = oponent_ai.reaction_speed * oponent_ai.aggression_level * 0.001 + oponent_ai.prediction_depth
        print("...score : " , score_left - score_right)
        return score_left - score_right
       

    def breed_next_generation(self, top_ais):
        print("\n------- Next generetion is being breeded -------\n")
        print(f"AI's used for breeding:", end= ' ')
        for i in range(len(top_ais)):
            print(f" AI{top_ais[i][2]} ", end= ',')
        
        self.population = []
        for _ in range(self.population_size):
            parent1, parent2 = random.sample(top_ais, 2)
            child = self.crossover(parent1[1], parent2[1])
            self.mutate(child)
            self.population.append(child)
        print("## Next generetion is ready")

    def crossover(self, parent1, parent2):
        return AIPlayer(
            reaction_speed=random.choice([parent1.reaction_speed, parent2.reaction_speed]),
            prediction_depth=random.choice([parent1.prediction_depth, parent2.prediction_depth]),
            aggression_level=random.choice([parent1.aggression_level, parent2.aggression_level])
        )

    def mutate(self, ai):
        if random.random() < self.mutation_rate:
            ai.reaction_speed += random.uniform(-0.5, 0.5)
            ai.prediction_depth += random.uniform(-0.5, 0.5)
            ai.aggression_level += random.uniform(-0.2, 0.2)
            ai.reaction_speed = max(1, min(5, ai.reaction_speed))
            ai.prediction_depth = max(1, min(5, ai.prediction_depth))
            ai.aggression_level = max(0.5, min(2, ai.aggression_level))

    def create_oponent_ai(self):
        av_speed = sum(ai.reaction_speed for ai in self.population) / self.population_size
        av_depth = sum(ai.prediction_depth for ai in self.population) / self.population_size
        av_agg = sum(ai.aggression_level for ai in self.population) / self.population_size

        return AIPlayer(av_speed,av_depth,av_agg)

    def print_AIs(self, oponent_ai : AIPlayer):
        for ai,i in zip(self.population, range(self.population_size)):
            print(f". AI{i+1} : ")
            print("---reaction speed: ", ai.reaction_speed)
            print("---prediction depth: ", ai.prediction_depth)
            print("---aggresion level: ", ai.aggression_level, "\n")
        print("--> AI oponent : ")
        print("---reaction speed: ", oponent_ai.reaction_speed)
        print("---prediction depth: ", oponent_ai.prediction_depth)
        print("---aggresion level: ", oponent_ai.aggression_level, "\n")
