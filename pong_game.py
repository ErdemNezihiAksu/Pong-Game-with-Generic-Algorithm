import tkinter as tk
import random
import time

PADDLE_HEIGHT = 100
PADDLE_WIDTH = 20
GAME_END_SCORE = 3

class AIPlayer:
    def __init__(self, reaction_speed, prediction_depth, aggression_level):
        self.reaction_speed = reaction_speed
        self.prediction_depth = prediction_depth
        self.aggression_level = aggression_level

    def move_paddle(self, paddle_y, ball_y, ball_dy):
        predicted_ball_y = ball_y + ball_dy * self.prediction_depth
        if predicted_ball_y < paddle_y + 50 and paddle_y > 0:
            return -self.reaction_speed * self.aggression_level
        elif predicted_ball_y > paddle_y + 50 and paddle_y < 300:
            return self.reaction_speed * self.aggression_level
        return 0

class Pong:
    def __init__(self, master, left_ai, right_ai , training = False):
        self.eval_params = []
        self.training = training
        self.ai_left = left_ai
        self.ai_right = right_ai
        self.master = master
        self.master.title("Pong")
        self.canvas = tk.Canvas(master, width=600, height=400, bg="black")
        self.canvas.pack()
        self.canvas.focus_set()

        self.ball = self.canvas.create_oval(290, 190, 310, 210, fill="white")
        self.paddle_left = self.canvas.create_rectangle(10, 150, 10 + PADDLE_WIDTH, 150 + PADDLE_HEIGHT, fill="white")
        self.paddle_right = self.canvas.create_rectangle(570, 150, 570 + PADDLE_WIDTH, 150 + PADDLE_HEIGHT, fill="white")
        
        self.score_left = 0
        self.score_right = 0
        self.hit_left = 0
        self.hit_right = 0
        
        self.score_left_text = self.canvas.create_text(150, 20, text="Left: 0", fill="white", font=("Arial", 14))
        self.score_right_text = self.canvas.create_text(450, 20, text="Right: 0", fill="white", font=("Arial", 14))

        self.ball_dx = random.choice([-3, 3])
        self.ball_dy = random.choice([-3, 3])
        self.paddle_speed = 2

        self.start_button = tk.Button(master, text="Start Game", bg="orange", command=self.__start_game)
        self.start_button.place(x=260, y=130, width=80, height=40)

        self.restart_button = tk.Button(master, text="Restart Game", bg="orange", command=self.auto_restart)

        self.winner_text = None
        self.start_time = None

        self.left_delay = 0
        self.right_delay = 0
        self.max_delay = None

        self.key_up_right_pressed = False
        self.key_down_right_pressed = False

    def set_AIs(self,left_ai, right_ai): #This function is used to change the AI's during training.
        self.ai_left = left_ai
        self.ai_right = right_ai

    def set_trainig(self,training: bool):
        self.training = training

    def auto_start(self):
        self.__start_game()

    def auto_restart(self):
        self.reset_game()
        self.__start_game()

    def get_time(self):
        stop = time.time()
        return stop - self.start_time
    
    def get_eval_params(self):
        print("gettting eval params...")
        return self.eval_params

    def __start_game(self):
        self.start_time = time.time()
        self.start_button.place_forget()
        self.restart_button.place_forget()
        if self.training is False:
            self.canvas.bind("<KeyPress-Up>", self.start_move_up_right)
            self.canvas.bind("<KeyRelease-Up>", self.stop_move_up_right)
            self.canvas.bind("<KeyPress-Down>", self.start_move_down_right)
            self.canvas.bind("<KeyRelease-Down>", self.stop_move_down_right)
            self.max_delay = 190
        else:
            self.max_delay = 100
        self.__game_loop()

    def reset_game(self):
        self.left_delay = 0
        self.right_delay = 0
        self.score_left = 0
        self.score_right = 0
        self.hit_left = 0
        self.hit_right = 0
        self.canvas.itemconfig(self.score_left_text, text="Left: 0")
        self.canvas.itemconfig(self.score_right_text, text="Right: 0")

        self.canvas.coords(self.paddle_left, 10, 150, 10 + PADDLE_WIDTH, 150 + PADDLE_HEIGHT)
        self.canvas.coords(self.paddle_right, 570, 150, 570 + PADDLE_WIDTH, 150 + PADDLE_HEIGHT)

        if self.winner_text:
            self.canvas.delete(self.winner_text)
            self.winner_text = None
        
        self.canvas.itemconfig(self.ball, state="normal")
        self.__reset_ball()
        self.restart_button.place_forget()
        self.start_button.place(x=260, y=130, width=80, height=40)

    def start_move_up_right(self, event):
        self.key_up_right_pressed = True

    def stop_move_up_right(self, event):
        self.key_up_right_pressed = False

    def start_move_down_right(self, event):
        self.key_down_right_pressed = True

    def stop_move_down_right(self, event):
        self.key_down_right_pressed = False

    def move_paddle_up_right(self):
        if self.canvas.coords(self.paddle_right)[1] > 0 and self.key_up_right_pressed:
            self.canvas.move(self.paddle_right, 0, -self.paddle_speed)

    def move_paddle_down_right(self):
        if self.canvas.coords(self.paddle_right)[3] < 400 and self.key_down_right_pressed:
            self.canvas.move(self.paddle_right, 0, self.paddle_speed)

    def move_ai_paddles(self):
        paddle_left_coords = self.canvas.coords(self.paddle_left)
        paddle_right_coords = self.canvas.coords(self.paddle_right)
        ball_coords = self.canvas.coords(self.ball)
        if self.left_delay == 0:
            move_left = self.ai_left.move_paddle(paddle_left_coords[1], ball_coords[1], self.ball_dy)
            self.canvas.move(self.paddle_left, 0, move_left)
        if self.training and self.right_delay == 0:
            move_right = self.ai_right.move_paddle(paddle_right_coords[1], ball_coords[1], self.ball_dy)
            self.canvas.move(self.paddle_right, 0, move_right)

    def __game_loop(self):
        self.move_ai_paddles()
        if self.training is False:
            self.move_paddle_up_right()
            self.move_paddle_down_right()
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        ball_pos = self.canvas.coords(self.ball)
        left_paddle_pos = self.canvas.coords(self.paddle_left)
        right_paddle_pos = self.canvas.coords(self.paddle_right)

        if self.right_delay > 0:
            self.right_delay -= 1
        elif self.left_delay > 0:
            self.left_delay -= 1

        if ball_pos[1] <= 0 or ball_pos[3] >= 400:
            self.ball_dy *= -1

        if ball_pos[0] <= left_paddle_pos[2] and ball_pos[1] >= left_paddle_pos[1] and ball_pos[3] <= left_paddle_pos[3]:
            self.ball_dx *= -1
            self.hit_left += 1
            self.left_delay = random.randint(0,self.max_delay)

        if ball_pos[2] >= right_paddle_pos[0] and ball_pos[1] >= right_paddle_pos[1] and ball_pos[3] <= right_paddle_pos[3]:
            self.ball_dx *= -1
            self.hit_right += 1
            self.right_delay = random.randint(0,self.max_delay)

        if ball_pos[0] <= 0:
            self.score_right += 1
            self.__reset_ball()

        if ball_pos[2] >= 600:
            self.score_left += 1
            self.__reset_ball()

        self.canvas.itemconfig(self.score_left_text, text="Left: " + str(self.score_left))
        self.canvas.itemconfig(self.score_right_text, text="Right: " + str(self.score_right))

        if self.score_left == GAME_END_SCORE or self.score_right == GAME_END_SCORE:
            self.__end_game()
            if self.training:
                self.master.quit()
            return
        else:
            if self.training and self.get_time() >= 40:
                self.eval_params = [self.score_left, self.hit_left, self.score_right, self.hit_right]
                print("time limit exceeded...")
                if self.training:
                    self.master.quit()
                return
            self.master.after(10, self.__game_loop)

    def __reset_ball(self):
        self.canvas.coords(self.ball, 290, 190, 310, 210)
        self.ball_dx = random.choice([-3, 3])
        self.ball_dy = random.choice([-3, 3])

    def __end_game(self):
        winner = "Left" if self.score_left == GAME_END_SCORE else "Right"
        self.winner_text = self.canvas.create_text(300, 200, text=f"{winner} player wins!", fill="white", font=("Arial", 20))
        self.canvas.itemconfig(self.ball, state="hidden")
        self.restart_button.place(x=260, y=130, width=80, height=40)
        if self.training:
            self.eval_params = [self.score_left, self.hit_left, self.score_right, self.hit_right]

