import pygame as pg
import random
import math
import os

pg.init()

# Width and height can be edited
max_width = pg.display.Info().current_w
max_height = pg.display.Info().current_h

width = int(max_width / 5)
height = int(max_height / 1.2)

pg.display.set_caption("Asteroidgame")

display = pg.display.set_mode((width, height))

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

robo_image = pg.image.load(os.path.join(img_folder, "robo.png"))
asteroid_image = pg.image.load(os.path.join(img_folder, "asteroid.png"))

fps = 60
clockpace = pg.time.Clock()

red = (255, 0, 0)
black = (0, 0, 0)

# Asteroid class
class Rock:
    def __init__(self, image, start_x: int, start_y: int, speed:int):
        self.__image = image
        self.__start_x = start_x
        self.__start_y = start_y
        self.__speed = speed

    def image(self):
        return self.__image

    def start_x(self):
        return self.__start_x

    def start_x_change(self, change):
        self.__start_x = change

    def start_y_change(self, change):
        self.__start_y = change

    def start_y(self):
        return self.__start_y

    def change_y(self):
        self.__start_y += self.__speed
    
    def speed(self):
        return self.__speed

    def speed_change(self, speed: int):
        self.__speed = speed

# Robotin luokka
class Robot:
    def __init__(self, image, start_x: int, start_y: int, speed: int):
        self.__image = image
        self.__start_x = start_x
        self.__start_y = start_y
        self.__speed = speed

    def image(self):
        return self.__image

    def start_x(self):
        return self.__start_x

    def start_y(self):
        return self.__start_y

    def speed(self):
        return self.__speed 

    def speedup(self):
        self.__speed += 1

    def to_right(self):
        self.__start_x += self.__speed

    def to_left(self):
        self.__start_x -= self.__speed


# Create n number asteroid to game
def create_asteroid(n_asteroid: int, asteroid_speed: int):
    asteroids = []

    for _ in range(n_asteroid):
        start_x = random.randint(0 , (width - asteroid_image.get_width()))
        start_y = random.randint(-height, (0 - asteroid_image.get_height()))
        start_y = int(math.ceil(start_y / asteroid_speed)) * asteroid_speed

        asteroids.append(Rock(asteroid_image, start_x, start_y, asteroid_speed))

    return asteroids

# Display scores
def show_scores(scores: int):
    font = pg.font.SysFont("Arial", 20)
    text = font.render(f"Scores: {scores}", True, (red))
    right_corner = text.get_rect()
    right_corner.right = width - (width / 20)
    display.blit(text, right_corner)

def loss_text():
    font = pg.font.SysFont("Arial", 50)
    text = font.render(f"Game over!", True, (red))
    middle = text.get_rect(center=(width/2, height/3))
    display.blit(text, middle)
    pg.display.flip()

# game function
def game():

    move_left = False
    move_rigth = False

    n_asteroid = 15
    asteroid_speed = 1

    asteroids = create_asteroid(n_asteroid, asteroid_speed)

    robotti = Robot(robo_image, (width/2), (height-robo_image.get_height()), 5)

    scores = 0

    game_over = False
    while not game_over:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                    move_rigth = True
            if event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                move_left = True
                    
            if event.type == pg.KEYUP and event.key == pg.K_RIGHT:
                    move_rigth = False
            if event.type == pg.KEYUP and event.key == pg.K_LEFT:
                move_left = False

            if event.type == pg.QUIT:
                exit()
        
        display.fill(black)

        for i in range(n_asteroid):

            if asteroids[i].start_y() + asteroids[i].image().get_height() >= height:
                game_over = True

            if  (asteroids[i].start_x() + asteroids[i].image().get_width() >= robotti.start_x() + 10) and \
                (asteroids[i].start_x() <= robotti.start_x() + robotti.image().get_width() - 10) and \
                (asteroids[i].start_y() + asteroids[i].image().get_height() >= robotti.start_y() + 10): 
                scores += 1
                start_x = random.randint(0 , (width - asteroid_image.get_width()))
                start_y = random.randint(-height, (0 - asteroid_image.get_height()))
                start_y = int(math.ceil(start_y / asteroid_speed)) * asteroid_speed

                asteroids[i].start_x_change(start_x)
                asteroids[i].start_y_change(start_y)
                
                # if scores are divisible by five, increase asteroid speed by a tenth 
                if scores % 5 == 0 and scores != 0:
                    asteroid_speed += 0.1
                    asteroids[i].speed_change(asteroid_speed)

                # if scores are divisible by 30, increase robot speed by one
                elif scores % 30 == 0 and scores != 0:
                    robotti.speedup()
                else:
                    asteroids[i].speed_change(asteroid_speed)

            if asteroids[i].start_y() + asteroids[i].image().get_height() <= height+1:
                asteroids[i].change_y()

            show_scores(scores)
            
            display.blit(asteroids[i].image(), (asteroids[i].start_x(), asteroids[i].start_y()))

        if move_rigth and  robotti.start_x() <= width-robo_image.get_width():
            robotti.to_right()
        if move_left and robotti.start_x() >= 0:
            robotti.to_left()

        display.blit(robotti.image(), (robotti.start_x(), robotti.start_y()))

        pg.display.flip()
        clockpace.tick(fps)

if __name__ == '__main__':
    
    game()
    loss_text()
    pg.time.wait(3000) 
