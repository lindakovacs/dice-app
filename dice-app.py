import turtle as tl
import random

class DiceGame:

    def __init__(self):
        # Initialize player name (sandbox-safe default)
        self.player_name = "Player"

        # Score Variables initialization
        self.total_games = 0
        self.total_wins = 0
        self.current_guess = 7

        # Dice values
        self.dice1 = 1
        self.dice2 = 1
        self.dice_sum = 2

        # Dice roll tracking
        self.roll_count = 0
        self.dice_counts = {2: 0, 3: 0, 5: 0}

        # Game state
        self.game_state = "guessing"  # guessing, rolling, result
        self.center_x = -20

        # Variables initialization
        self.create_window()
        self.create_displays()
        self.create_dice()
        self.create_buttons()
        self.keys()
        self.game_loop()

    def create_window(self):
        self.root = tl.Screen()
        if hasattr(self.root, "title"):
            self.root.title("DICE GUESSING GAME")
        if hasattr(self.root, "bgcolor"):
            self.root.bgcolor("#3498db")
        if hasattr(self.root, "setup"):
            self.root.setup(width=520, height=450)
        if hasattr(self.root, "tracer"):
            self.root.tracer(0)

    def create_displays(self):
        # Fallback background fill for sandboxes that ignore Screen.bgcolor
        self.bg_display = tl.Turtle()
        self.bg_display.hideturtle()
        self.bg_display.penup()

        # Stats display at the very top
        self.stats_display = tl.Turtle()
        self.stats_display.hideturtle()
        self.stats_display.penup()
        self.stats_display.color("white")
        self.stats_display.goto(self.center_x, 165)

        # Title display (below stats)
        self.title_display = tl.Turtle()
        self.title_display.hideturtle()
        self.title_display.penup()
        self.title_display.color("white")
        self.title_display.goto(self.center_x, 138)
        self.title_display.write("DICE GUESSING GAME", align="center", font=("Arial", 22, "bold"))

        # Player name display (below title)
        self.name_display = tl.Turtle()
        self.name_display.hideturtle()
        self.name_display.penup()
        self.name_display.color("yellow")
        self.name_display.goto(self.center_x, 114)
        self.name_display.write("Player: {}".format(self.player_name), align="center", font=("Arial", 16, "normal"))

        # Instruction display
        self.instruction_display = tl.Turtle()
        self.instruction_display.hideturtle()
        self.instruction_display.penup()
        self.instruction_display.color("white")

        # Guess display
        self.guess_display = tl.Turtle()
        self.guess_display.hideturtle()
        self.guess_display.penup()
        self.guess_display.color("yellow")

        # Result display
        self.result_display = tl.Turtle()
        self.result_display.hideturtle()
        self.result_display.penup()

    def create_dice(self):
        # Left dice
        self.left_dice = tl.Turtle()
        self.left_dice.hideturtle()
        self.left_dice.penup()
        self.left_dice.speed(0)

        # Right dice
        self.right_dice = tl.Turtle()
        self.right_dice.hideturtle()
        self.right_dice.penup()
        self.right_dice.speed(0)

    def draw_dice(self, turtle_obj, x, y, value):
        """Draw a dice with dots"""
        turtle_obj.clear()
        turtle_obj.goto(x, y)

        # Draw dice square
        turtle_obj.pendown()
        turtle_obj.fillcolor("white")
        turtle_obj.begin_fill()
        for _ in range(4):
            turtle_obj.forward(80)
            turtle_obj.right(90)
        turtle_obj.end_fill()
        turtle_obj.penup()

        # Draw dots
        turtle_obj.color("black")
        dot_positions = {
            1: [(x + 40, y - 40)],
            2: [(x + 20, y - 20), (x + 60, y - 60)],
            3: [(x + 20, y - 20), (x + 40, y - 40), (x + 60, y - 60)],
            4: [(x + 20, y - 20), (x + 60, y - 20), (x + 20, y - 60), (x + 60, y - 60)],
            5: [(x + 20, y - 20), (x + 60, y - 20), (x + 40, y - 40), (x + 20, y - 60), (x + 60, y - 60)],
            6: [(x + 20, y - 20), (x + 60, y - 20), (x + 20, y - 40), (x + 60, y - 40), (x + 20, y - 60), (x + 60, y - 60)]
        }

        for pos in dot_positions[value]:
            turtle_obj.goto(pos[0], pos[1])
            turtle_obj.dot(12)

    def create_buttons(self):
        # Plus button
        self.plus_btn = tl.Turtle()
        self.plus_btn.hideturtle()
        self.plus_btn.penup()
        self.plus_btn.speed(0)

        # Minus button
        self.minus_btn = tl.Turtle()
        self.minus_btn.hideturtle()
        self.minus_btn.penup()
        self.minus_btn.speed(0)

        # Roll button
        self.roll_btn = tl.Turtle()
        self.roll_btn.hideturtle()
        self.roll_btn.penup()
        self.roll_btn.speed(0)

    def draw_button(self, turtle_obj, x, y, width, height, text, color):
        """Draw a button"""
        turtle_obj.clear()
        turtle_obj.goto(x, y)
        turtle_obj.pendown()
        turtle_obj.fillcolor(color)
        turtle_obj.begin_fill()
        for i in range(2):
            turtle_obj.forward(width)
            turtle_obj.right(90)
            turtle_obj.forward(height)
            turtle_obj.right(90)
        turtle_obj.end_fill()
        turtle_obj.penup()

        # Draw text
        turtle_obj.goto(x + width/2, y - height/2 - 10)
        turtle_obj.color("white")
        turtle_obj.write(text, align="center", font=("Arial", 16, "bold"))

    def update_display(self):
        """Update the display based on game state"""
        self.draw_background()

        if self.game_state == "guessing":
            self.instruction_display.clear()
            self.instruction_display.goto(self.center_x, 82)
            self.instruction_display.write("Guess the sum of two dice!", align="center", font=("Arial", 16, "normal"))

            self.guess_display.clear()
            self.guess_display.goto(self.center_x, 45)
            self.guess_display.write("Your Guess: {}".format(self.current_guess), align="center", font=("Arial", 30, "bold"))
            self.guess_display.goto(self.center_x, 20)
            self.guess_display.write("Click + and - to adjust your guess", align="center", font=("Arial", 12, "normal"))

            # Draw plus/minus buttons under guess on same level
            self.draw_button(self.plus_btn, -95, -10, 70, 36, "+", "#2ecc71")
            self.draw_button(self.minus_btn, -5, -10, 70, 36, "-", "#e74c3c")

            # Draw roll button
            self.draw_button(self.roll_btn, -100, -85, 160, 45, "ROLL DICE", "#9b59b6")

            # Clear dice and result
            self.left_dice.clear()
            self.right_dice.clear()
            self.result_display.clear()

        elif self.game_state == "result":
            self.instruction_display.clear()

            # Draw dice
            self.draw_dice(self.left_dice, -150, 0, self.dice1)
            self.draw_dice(self.right_dice, 20, 0, self.dice2)

            # Show result
            self.guess_display.clear()
            self.result_display.clear()

            if self.dice_sum == self.current_guess:
                self.result_display.goto(self.center_x, 80)
                self.result_display.color("green")
                self.result_display.write("YOU WIN!", align="center", font=("Arial", 24, "bold"))
            else:
                self.result_display.goto(self.center_x, 80)
                self.result_display.color("red")
                self.result_display.write("YOU LOSE!", align="center", font=("Arial", 24, "bold"))

            self.result_display.goto(self.center_x, 52)
            self.result_display.color("white")
            self.result_display.write("Sum: {} | Your Guess: {}".format(self.dice_sum, self.current_guess), align="center", font=("Arial", 14, "normal"))

            # Draw play again button
            self.draw_button(self.roll_btn, -120, -145, 200, 45, "PLAY AGAIN", "#3498db")

            # Clear other buttons
            self.plus_btn.clear()
            self.minus_btn.clear()

        # Update stats
        self.update_stats()

    def update_stats(self):
        """Update statistics display"""
        self.stats_display.clear()
        if self.total_games > 0:
            win_rate = (self.total_wins / self.total_games) * 100
            self.stats_display.write("Games: {} | Wins: {} | Win Rate: {:.1f}%".format(self.total_games, self.total_wins, win_rate),
                                    align="center", font=("Arial", 14, "normal"))
        else:
            self.stats_display.write("Games: 0 | Wins: 0 | Win Rate: 0.0%",
                                    align="center", font=("Arial", 14, "normal"))

    def draw_background(self):
        self.bg_display.clear()
        self.bg_display.goto(-260, 190)
        self.bg_display.setheading(0)
        self.bg_display.pendown()
        self.bg_display.fillcolor("#5dade2")
        self.bg_display.begin_fill()
        for _ in range(2):
            self.bg_display.forward(520)
            self.bg_display.right(90)
            self.bg_display.forward(560)
            self.bg_display.right(90)
        self.bg_display.end_fill()
        self.bg_display.penup()


    def on_click(self, x, y):
        """Handle mouse clicks"""
        if self.game_state == "guessing":
            # Plus button (-95 to -25, -46 to -10)
            if -95 <= x <= -25 and -46 <= y <= -10:
                self.current_guess = min(self.current_guess + 1, 12)
                self.update_display()

            # Minus button (-5 to 65, -46 to -10)
            elif -5 <= x <= 65 and -46 <= y <= -10:
                self.current_guess = max(self.current_guess - 1, 2)
                self.update_display()

            # Roll button (-100 to 60, -130 to -85)
            elif -100 <= x <= 60 and -130 <= y <= -85:
                self.roll_dice()

        elif self.game_state == "result":
            # Play again button (-120 to 80, -190 to -145)
            if -120 <= x <= 80 and -190 <= y <= -145:
                self.game_state = "guessing"
                self.update_display()

    def roll_dice(self):
        """Roll the dice and show result"""
        self.game_state = "rolling"

        # Animate rolling
        for _ in range(10):
            temp_dice1 = random.randint(1, 6)
            temp_dice2 = random.randint(1, 6)
            self.draw_dice(self.left_dice, -150, 0, temp_dice1)
            self.draw_dice(self.right_dice, 20, 0, temp_dice2)
            self.root.update()
            self.root.ontimer(lambda: None, 50)

        # Final roll
        self.dice1 = random.randint(1, 6)
        self.dice2 = random.randint(1, 6)
        self.dice_sum = self.dice1 + self.dice2

        # Track and print dice rolls
        self.roll_count += 1
        print("Roll {}: Dice 1 = {}, Dice 2 = {}, Sum = {}".format(self.roll_count, self.dice1, self.dice2, self.dice_sum))

        # Track specific dice values
        if self.dice1 in self.dice_counts:
            self.dice_counts[self.dice1] += 1
        if self.dice2 in self.dice_counts:
            self.dice_counts[self.dice2] += 1

        # Update stats
        self.total_games += 1
        if self.dice_sum == self.current_guess:
            self.total_wins += 1

        # Print summary if reaching 10 rolls
        if self.roll_count % 10 == 0:
            print("\n--- Summary (After {} rolls) ---".format(self.roll_count))
            print("Number 2: Appeared {} times.".format(self.dice_counts[2]))
            print("Number 3: Appeared {} times.".format(self.dice_counts[3]))
            print("Number 5: Appeared {} times.\n".format(self.dice_counts[5]))

        self.game_state = "result"
        self.update_display()

    def keys(self):
        """Set up keyboard controls"""
        self.root.listen()
        self.root.onkey(lambda: self.on_key_space(), "space")
        self.root.onclick(self.on_click)

    def on_key_space(self):
        if self.game_state == "guessing":
            self.roll_dice()
        elif self.game_state == "result":
            self.game_state = "guessing"
            self.update_display()

    def game_loop(self):
        """Main game loop"""
        self.update_display()
        self.root.mainloop()

def main():
    DiceGame()

if __name__ == '__main__':
    main()