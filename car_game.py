import pygame
import random
import time
import math
import winsound

# Initializing the pygame
pygame.init()
rotate = 90
screen = pygame.display.set_mode((840, 650))

# store the image as variable
bg = pygame.image.load("road_image_T.png")
car = pygame.image.load("orange_T.png")
enemy = pygame.image.load("red_T.png")

# Initialize the score related values
score = 0
high_score = 0
score_list = []

# Initalize the font type and size of score
font = pygame.font.SysFont("arial", 40, True)
mes = "SCORE : {}".format(str(score))

# Declare the enemy, x_position 
enemy_s = []
enemy_x = []
enemy_y = []
number= 3

# Append the list of enemy and their positions
for i in range(number):
    enemy_s.append(enemy)
    enemy_x.append(random.choice([190,190, 320, 320, 450, 450,580, 580]))
    enemy_y.append(random.choice([0, 10, 4, -10, 20, -5, -2, 8]))

# Initialize the position of car
car_x = 450; car_y = 540
x_change = 0

# to initalize the speed of enemy movement
enemy_y_change = 10

# To increase the speed of the enemy
speed = 0.0099

# Initalize the life
life = 3

# Set the current time
current_time = str(time.ctime())

# Crush of car by enemy
def Collusion(x, y, a, b):
    distance = math.sqrt(pow(x - a, 2)+pow(y - b, 2))
    if distance < 100:
        return True

# Main Loop
while True:
    
    screen.blit(bg, (0, 0))

    # Open The high Score
    try:
        with open("Score.txt", "r+") as high:
            if high is None:
                s = high.write("")
            s = high.read()
            s = s.split("\n")
            if len(s) > 1:
                for i in range(len(s)-1):
                    l = int(s[i][48::])    
                    score_list.append(l)
                high_score = max(score_list)

    # if no file is detected create file
    except FileNotFoundError:
        with open("Score.txt","w+") as initial:
            initial.write("")

    # Show the High score on the display
    high_score_mes = "HIGH SCORE : {}".format(high_score)
    high_score_text = font.render(high_score_mes, True, (0, 255, 0))
    screen.blit(high_score_text, (5,200))

    # Show the score on the display
    mes = "SCORE : {}".format(str(score))
    text = font.render(mes, True, (255, 0, 0))
    screen.blit(text, (5, 150))

    # After leave the key then asign value to 0 for current place
    x_change = 0

    # User input from the key for X_change
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
            pygame.display.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -130
                # Make sound for the movement
                winsound.Beep(2000, 100)
                
            if event.key == pygame.K_RIGHT:
                x_change = +130
                # Make sound for the movement
                winsound.Beep(2000, 100)
    
    for i in range(len(enemy_s)):
        screen.blit(enemy_s[i], (enemy_x[i], enemy_y[i]))

        # Enemy object moving
        enemy_y[i] += enemy_y_change
        enemy_y_change += speed
        # If enemy object is outoff limit renew it
        if enemy_y[i] > 650:
            score += 1
            enemy_x[i] = random.choice([190,190, 320, 320, 450, 450,580, 580])
            enemy_y[i] = random.choice([0, -40, -20, -10, 10, 15, -2, 8])        

        # font for life
        font = pygame.font.SysFont("arial", 40, True)
        life_mes = "LIFE : {}".format(life)
        text_life = font.render(life_mes, True, (255, 0, 0))
        screen.blit(text_life, (5, 100))
        
        if life <=0:
            
            # font for gameover
            font = pygame.font.SysFont("arial", 100, True)
            game_over = "GAME OVER"
            text_over = font.render(game_over, True, (255, 255, 255))
            screen.fill((0,0,0))
            screen.blit(text_over, (150,300))

            # Font for your score display at the end game
            your_score_font = pygame.font.SysFont("arial", 50)
            your_score_mes = "Your Score : {}".format(score)
            your_score_end_text = your_score_font.render(your_score_mes, True, (40,240,140))
            screen.blit(your_score_end_text, (400,200))

            # Font for high score display at the end game
            high_score_font = pygame.font.SysFont("arial", 50)
            high_score_mes = "High Score : {}".format(high_score)
            high_score_end_text = high_score_font.render(high_score_mes, True, (140,240,40))
            screen.blit(high_score_end_text, (5,200))

            # End the game by pause
            speed = 0
            enemy_y_change = 0

            # if you beat the score make the congratulations message
            if score > high_score:
                # Font for beat the high score
                mess = "This is High Score"
                end_font = pygame.font.SysFont("arial", 40)
                end = end_font.render(mess, True, (50, 255, 200))
                screen.blit(end, (100,0))

                # Font for Congratulation message at the end
                congratulation = "Congratulations !!!"
                con_font = pygame.font.SysFont("arial", 40)
                con = con_font.render(congratulation, True, (50, 255, 200))
                screen.blit(con, (100, 50))
            #time.sleep(10)
            #pygame.display.quit()
            
    
        # If the car and enemy and touch each other
        collusion = Collusion(car_x, car_y, enemy_x[i], enemy_y[i])

        # if True
        if collusion:
            # Make sound for the car crush
            winsound.MessageBeep(2)
            time.sleep(2)
            # if true renew new car
            enemy_x[i] = random.choice([190,190, 320, 320, 450, 450,580, 580])
            enemy_y[i] = random.choice([0, -40, -20, -10, 10, 15, -2, 8])        

            # Reduse one life with respect to one collusion
            life -=1

            # if life is less then 1 print game over
            if life == 0:
                s = str(score)
                with open("Score.txt", "a") as score_file:
                    score_file.write("Current time : {} ".format(current_time))
                    score_file.write("Score : {}\n".format(s))

    # Chnaging X_change with respect to key press
    car_x += x_change

    # To make the game intresting speed up the enemy
    
    # Set limit for car run inside the road
    if car_x < 190:
        car_x = 190
    if car_x > 580:
        car_x = 580

    
    # Place the car on the screen
    screen.blit(car, (car_x, car_y))

    pygame.display.update()
            
