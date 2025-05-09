# %% [markdown]
# <a href="https://colab.research.google.com/github/yoojinleee/CarGame/blob/main/CarGame.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# %%
import pygame
import random
import sys
import time

# Initializing the game
pygame.init()

# Making the settings for the screen display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game")

# Frame rate for moving car
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

#Car
car_width, car_height = 50, 100
car = pygame.Rect(WIDTH//2, HEIGHT - 120, car_width, car_height)

# Making the car move
car_speed = 5

#Obstacle
obstacle_width, obstacle_height = 50, 100
obstacles = []
obstacle_speed = 5

#Game Activity
running = True
game_active = True
last_math_time = time.time ()
math_interval = 30

#Colors
WHITE = (255, 255, 255)
Black = (0,0,0)
Red = (255, 0, 0)
Blue = (0, 0, 255)

def draw_car():
  pygame.draw.rect(screen, Blue, car)

def draw_obstacles():
  for obs in obstacles:
    x, y, width, height = obs
    # Define the traffic cone shape
    point1 = (x + width // 2, y)
    point2 = (x, y + height)
    point3 = (x + width, y + height)
    points = [point1, point2, point3]
    pygame.draw.polygon(screen, (255, 165, 0), [point1, point2, point3])
    pygame.draw.line(screen, (255, 255, 255), (x + width // 2, y), (x, y + height), 2)
    pygame.draw.line(screen, (255, 255, 255), (x + width // 2, y), (x + width, y + height), 2) 

def spawn_obstacle():
  x = random.randint(0, WIDTH - obstacle_width)
  new_obstacle = pygame.Rect(x, -obstacle_height, obstacle_width, obstacle_height)
  obstacles.append(new_obstacle)

def move_obstacles():
  for obs in obstacles:
    obs.y += obstacle_speed
  #Deleting obstacles off the screen
  obstacles[:] = [obs for obs in obstacles if obs.y < HEIGHT]

def check_collision():
  for obs in obstacles:
    if car.colliderect(obs):
      return True
  return False

def show_message(message):
  text = font.render(message, True, Black)
  rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
  screen.blit(text, rect)
  pygame.display.flip()
  pygame.time.delay(2000)

def start_math_quiz():
  global num1, num2, answer, user_input, game_state
  num1 = random.randint(1,10)
  num2 = random.randint(1,10)
  answer = num1 * num2
  user_input = ""
  game_state = "math_quiz"

# %%
pip install pygame

# %%


# %%
print(pygame.font.get_fonts())

# %%
# Pausing the game every 30 seconds to ask a math question
# Generate two random numbers between 1 and 10

def ask_math_question():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    answer = num1 * num2 # Calculate the correct answer
    user_input = ""
    asking = True


# Begin the math question loop
    while asking:
        screen.fill(WHITE) # Clearing the screen so we can ask the math question
        question = font.render(f"What is {num1} x {num2}?", True, Black)
        input_box = font.render(user_input, True, Red)
        screen.blit(question, (WIDTH // 2 - question.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(input_box, (WIDTH // 2 - input_box.get_width() // 2, HEIGHT // 2 + 10))
        pygame.display.flip()

# Handling different events that could potentially happen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if user_input.isdigit():
                        if int(user_input) == answer:
                            asking = False  # Resume the game
                        else:
                            show_message("Wrong! You died.")
                            return False  # Game is over
                else:
                    user_input += event.unicode
    return True  # Continue the game

game_state = "playing"
user_input = ""
num1, num2 = 0,0
answer = 0

# %%


# %%
while running:
  clock.tick(60)
  screen.fill(WHITE)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    if game_state == "math_quiz" and event.type == pygame.KEYDOWN:
      if event.key == pygame.K_BACKSPACE:
        user_input = user_input[:-1]
      elif event.key == pygame.K_RETURN:
        if user_input.isdigit():
          if int(user_input) == answer:
            game_state = "playing"
            last_math_time = time.time()
          else:
            show_message("Wrong! You died.")
            game_active = False
            game_state = "game_over"
      else:
        user_input += event.unicode

    if game_state == "math_quiz":
      question = font.render(f"What is {num1} x {num2}?", True, Black)
      input_box = font.render(user_input, True, Red)
      screen.blit(question, (WIDTH//2 - question.get_width()//2, HEIGHT//2-50))
      screen.blit(input_box, (WIDTH//2 - input_box.get_width()//2, HEIGHT//2+10))

    elif game_state == "playing" and game_active:
      keys = pygame.key.get_pressed()
      if keys[pygame.K_LEFT] and car.left>0:
        car.x -= car_speed
      if keys[pygame.K_RIGHT] and car.right<WIDTH:
        car.x += car_speed

      if random.randint(1,20)==1:
        spawn_obstacle()

      move_obstacles()
      draw_car()
      draw_obstacles()

      if check_collision():
        show_message("You crashed!")
        game_active = False
        game_state = "game_over"

    #Time-based math challenge
      if time.time() - last_math_time > math_interval:
        start_math_quiz()

    elif game_state == "game_over":
      show_message("Press R to restart")
      keys = pygame.key.get_pressed()
      if keys[pygame.K_r]:
          car.x = WIDTH//2
          car.y = HEIGHT - 120
          obstacles.clear()
          last_math_time = time.time()
          game_active = True
          game_state = "playing"

  pygame.display.flip() % DisplayHandle

pygame.quit()
sys.exit()


