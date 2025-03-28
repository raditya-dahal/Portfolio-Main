# Import the Turtle Graphics Module
import random
import turtle

# Define program constants
WIDTH = 800
HEIGHT = 600
DELAY = 200  # In Milisecond
FOOD_SIZE = 32
SNAKE_SIZE = 20

offsets = {
    "up": (0, SNAKE_SIZE),
    "down": (0, -SNAKE_SIZE),
    "left": (-SNAKE_SIZE, 0),
    "right": (SNAKE_SIZE, 0),
}

#highscore
high_score = 0

#load the high score if it exits

try:
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    pass

def update_high_score():
    global high_score
    if score > high_score:
        high_score = score
        with open("high_score.txt", "w") as file:
            file.write(str(high_score))

def bind_direction_keys():
    screen.onkey(lambda: set_snake_direction("up"), "Up")
    screen.onkey(lambda: set_snake_direction("down"), "Down")
    screen.onkey(lambda: set_snake_direction("left"), "Left")
    screen.onkey(lambda: set_snake_direction("right"), "Right")


def set_snake_direction(direction):
    global snake_direction
    if direction == "up":
        if snake_direction != "down":  # No self-Collision simply by pressing wrong key
            snake_direction = "up"
    elif direction == "down":
        if snake_direction != "up":  # No self-Collision simply by pressing wrong key
            snake_direction = "down"
    elif direction == "right":
        if snake_direction != "left":  # No self-Collision simply by pressing wrong key
            snake_direction = "right"
    elif direction == "left":
        if snake_direction != "right":  # No self-Collision simply by pressing wrong key
            snake_direction = "left"


def game_loop():
    stamper.clearstamps()

    new_head = snake[-1].copy()
    new_head[0] += offsets[snake_direction][0]
    new_head[1] += offsets[snake_direction][1]

    # Check collisions
    if new_head in snake or new_head[0] < -WIDTH / 2 or new_head[0] > WIDTH / 2 \
            or new_head[1] < -HEIGHT / 2 or new_head[1] > HEIGHT / 2:
        reset()
    else:
        # Add new head to snake body
        snake.append(new_head)

        # Check food collision
        if not food_collision():
            snake.pop(0)  # Remove tail only if food was NOT eaten

        # Draw Snake for the first time
        for segment in snake:
            stamper.goto(segment[0], segment[1])
            stamper.stamp()

        # Refresh Screen
        screen.title(f"Snake Game. Score: {score} High Score: {high_score}")
        screen.update()

        # Continue the game loop
        turtle.ontimer(game_loop, DELAY)


def food_collision():
    global food_pos, score
    if get_distance(snake[-1], food_pos) < 20:
        score += 1  # score = score + 1
        update_high_score()
        food_pos = get_random_food_pos()
        food.goto(food_pos)
        return True
    return False


def get_random_food_pos():
    x = random.randint(int(-WIDTH / 2 + FOOD_SIZE), int(WIDTH / 2 - FOOD_SIZE))
    y = random.randint(int(-HEIGHT / 2 + FOOD_SIZE), int(HEIGHT / 2 - FOOD_SIZE))
    return (x, y)


def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5  # Pythagoras
    return distance


def reset():
    global score, snake, snake_direction, food_pos
    score = 0
    snake = [[0, 0], [SNAKE_SIZE, 0], [SNAKE_SIZE * 2, 0], [SNAKE_SIZE * 3, 0]]
    snake_direction = "up"
    food_pos = get_random_food_pos()
    food.goto(food_pos)
    game_loop()


# Create a window where we will do our drawing.
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)  # Set the dimensions of the Turtle Graphics Window
screen.title("Snake")
screen.bgcolor("#eb7609")
screen.tracer(0)  # Turns of animations.

# Event handlers
screen.listen()
bind_direction_keys()

# Create a turtle to do your bidding
stamper = turtle.Turtle()
stamper.shape("square")
stamper.color("#121211")
stamper.penup()


# Food
food = turtle.Turtle()
food.shape("circle")
food.color("#ffcc00")
food.shapesize(FOOD_SIZE / 20)
food.penup()

# Set animation in motion
reset()

# Finish nicely
turtle.done()
