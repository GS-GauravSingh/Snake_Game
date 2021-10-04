# Pygame Version: 2.0.1
import pygame
from pygame.locals import *
import pygame.display
import pygame.event
import pygame.draw
import pygame.time
import pygame.image
import pygame.transform
import pygame.font
import pygame.mixer
import random
import os.path

pygame.mixer.init()
pygame.init()

# Defining colors with RGB values
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
dark_green = (12, 87, 3)

Screen_Width = 800
Screen_Height = 600
Game_Window = pygame.display.set_mode([Screen_Width, Screen_Height])
pygame.display.set_caption("Snakes by VishuCool")

def welcome_screen():
    exit_game = False
    while not exit_game:
        img = pygame.image.load("welcome.png")
        Game_Window.blit(img, [0, 0])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    pygame.mixer.music.load("background.mp3")
                    pygame.mixer.music.play()
                    mainGame_loop()

            pygame.display.update()
            clock.tick(60)


clock = pygame.time.Clock()
font = pygame.font.SysFont('footlight', 30)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    Game_Window.blit(screen_text, [x, y])


def plot_snake(gamewindow, color, snk_list, snk_size):
    for x,y in snk_list:
        pygame.draw.rect(gamewindow, color, (x, y, snk_size, snk_size))



   
def mainGame_loop():
    file_path = "hiscore.txt" 

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            highscore = f.read()

    else: 
        with open(file_path, "w") as f:
            f.write("0")

    snk_list = []
    snk_length = 1
    Exit_game = False
    Game_over = False
    Snake_x = 50 # snake head 'x' coordinate
    Snake_y = 50 # snake head 'y' coordinate
    snake_size = 30
    init_velocity = 5
    snakevel_x = 0
    snakevel_y = 0
    fps = 60
    food_x = random.randint(40, Screen_Width/2)
    food_y = random.randint(40, Screen_Height/2)
    score = 0
    
    

    while not Exit_game:
        
        if Game_over:
            with open(file_path, "w") as f:
                f.write(str(highscore))
            img = pygame.image.load("overimg.png")
            Game_Window.blit(img, [0, 0])
            if score<int(highscore):
                text_screen(f"Your Score is: {score}", black, 280, 20)
            else: 
                text_screen(f"Congrats!! You created a new High Score: {highscore}", black, 120, 20)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == K_RETURN:
                        welcome_screen()



        else:
            # Handeling events
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # creating Exit game functionality
                    Exit_game = True

                
                if event.type == pygame.KEYDOWN:
                    if event.key == K_LEFT:
                        snakevel_x -= init_velocity
                        snakevel_y = 0

                    if event.key == K_RIGHT:              
                        snakevel_x += init_velocity
                        snakevel_y = 0

                    if event.key == K_UP:
                        snakevel_y -= init_velocity
                        snakevel_x = 0

                    if event.key == K_DOWN:
                        snakevel_y += init_velocity
                        snakevel_x = 0
                
            Snake_x = Snake_x + snakevel_x
            Snake_y = Snake_y + snakevel_y

            if abs(Snake_x - food_x)< 10 and abs(Snake_y - food_y)< 10:
                point = pygame.mixer.Sound("beep.mp3")
                pygame.mixer.Sound.play(point)
                score += 10
                food_x = random.randint(20, Screen_Width/2)
                food_y = random.randint(20, Screen_Height/2)
                snk_length += 5

                if score>int(highscore):
                    highscore = int(highscore) + 10


            if Snake_x>Screen_Width or Snake_x<0 or Snake_y<0 or Snake_y>Screen_Height:
                pygame.mixer.music.load("gameover.mp3")
                pygame.mixer.music.play()
                Game_over = True

            
                
            # Blitting background image and printing score on screen
            bg = pygame.image.load("background.png")
            Game_Window.blit(bg, [0,0])

            if score<int(highscore):
                text_screen(f"Score:{str(score)}", black, 5,5)
                text_screen(f"High Score: {str(highscore)}", black, 580,5)
            else:
                text_screen(f"High Score: {str(highscore)}", black, 5,5)


            # Blitting Snake head on screen
            plot_snake(Game_Window, dark_green, snk_list, snake_size)
            snk_head = pygame.image.load("snk_head.png")
            snk_head.convert()
            rect = snk_head.get_rect()
            Game_Window.blit(snk_head, [Snake_x, Snake_y])
            
            # Blitting Snake food on screen
            snk_food = pygame.image.load("food.png")
            Game_Window.blit(snk_food, (food_x, food_y))

            head = []
            head.append(Snake_x)
            head.append(Snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]
                             

            if head in snk_list[:-1]:
                pygame.mixer.music.load("gameover.mp3")
                pygame.mixer.music.play()
                Game_over = True

        
        
        pygame.display.update()
        clock.tick(fps)
        
    pygame.quit()
    quit()


welcome_screen()


