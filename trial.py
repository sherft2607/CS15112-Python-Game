import turtle
import time
import random

# Constants
LEVELS = 3
MAX_SEEDS_PER_LEVEL = 5
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Player settings
jump_height = 40

def draw_bird(size):
    turtle.shape("triangle")
    turtle.shapesize(size)
    turtle.color("blue")

def draw_seed(x, y):
    turtle.penup()
    turtle.goto(x, y)
    turtle.dot(20, "green")

def jump():
    turtle.sety(turtle.ycor() + jump_height)

def collect_seeds():
    seeds_collected = random.randint(1, MAX_SEEDS_PER_LEVEL)
    print(f"You collected {seeds_collected} seeds!")
    return seeds_collected

def play_level(level):
    print(f"\n--- Level {level} ---")
    time.sleep(1)
    print("The baby bird is growing!")

    seeds_collected = 0
    for _ in range(MAX_SEEDS_PER_LEVEL):
        jump()
        seeds_collected += collect_seeds()

    print(f"\nYou completed Level {level}!")
    return seeds_collected

def main():
    turtle.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    turtle.title("Circle of Life Adventure")
    turtle.speed(1)

    draw_bird(1)

    total_seeds_collected = 0
    for level in range(1, LEVELS + 1):
        total_seeds_collected += play_level(level)

    print("\nCongratulations! You completed all levels.")
    print(f"Total seeds collected: {total_seeds_collected}")
    print("The grown bird reaches its nest. The circle of life is complete.")

    turtle.done()

if __name__ == "__main__":
    main()
