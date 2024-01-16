
import pygame
import sys
import random
import time

pygame.init()

window_width = 720
window_length = 460
playSurface = pygame.display.set_mode((window_width, window_length)) 
pygame.display.set_caption('!!! SNAKE GAME !!!') 


#Colors
# The color method expects three parameters r,g,b combination to give the color
red = pygame.Color(255, 0 ,0) #red color-gameover
snake_color = pygame.Color(0, 255, 0) #green-snake
white = pygame.Color(255, 255, 255) #white-score
black = pygame.Color(0, 0, 0) #black-screen
dark_red = pygame.Color(128, 0, 0) #food color
#brown = pygame.Color(165, 42, 42) #brown-food

# fps controller
fpsController = pygame.time.Clock()

# important varibles for the gameover
snakePos = [100, 50] #initial coordinate of the snake head
snakeBody = [[100, 50], [90, 50], [80, 50]] #snake snakeBody

foodPos = [random.randrange(1, (window_width//10)) * 10, 
           random.randrange(1,(window_length//10)) * 10] #random food positioning

foodSpawn = True
direction = 'RIGHT'
changeTo = direction
score = 0
snake_speed = 10
initscore = 0

# variables for our button
button_rect = pygame.Rect(300, 400, 120, 50)
button_color = (0, 0, 255)
button_text = "RESTART"
button_font = pygame.font.SysFont('monaco', 24)
button_text_surface = button_font.render(button_text, True, white)
button_text_rect = button_text_surface.get_rect(center=button_rect.center)

# drawing the "restart" button
def draw_button():
    pygame.draw.rect(playSurface, button_color, button_rect)
    playSurface.blit(button_text_surface, button_text_rect)

# Game Over function
def gameOver():
    myFont = pygame.font.SysFont('monaco', 72) 
    GOsurf = myFont.render(' GAME OVER !!!', True, red) 
    GOrect = GOsurf.get_rect() 
    GOrect.midtop = (350, 15)
    playSurface.blit(GOsurf, GOrect) 
    showScore(0)
    pygame.display.flip() # to set the fps
           
ocean_color=pygame.Color('mediumaquamarine') 
 #for the backround
def draw_ocean(): 
   for row in range(40) :
       if row %2==0:
        for col in range(40):
            ocean_rect=pygame.Rect(col*60,row*60,60,60)
            pygame.draw.rect(playSurface,ocean_color,ocean_rect)
       else: 
            for col in range(40):
             if col %2 !=0:
              ocean_rect=pygame.Rect(col*60,row*60,60,60)
              pygame.draw.rect(playSurface,ocean_color,ocean_rect)

# Funcție pentru afișarea scorului
game_over_flag = False

def showScore(choice=1):
    sFont = pygame.font.SysFont('monaco', 42) #choose font name and size
    Ssurf = sFont.render('SCORE : {0}'.format(score), True, black) # this is the surface where game over will display having 3 args : the message, antialiasing,and Color
    Srect = Ssurf.get_rect() #to get rect coordinates of the game over text surface
    if choice == 1:
        Srect.midtop = (80, 10)
    else:
        Srect.midtop = (360, 120)

    playSurface.blit(Ssurf, Srect) # bind the gameover text to the main surface
    pygame.display.flip() # to set the fps

def update_score(nscore):
    score = max_score()

    with open('highest_score.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))

def max_score():
    with open('highest_score.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score

# Main Logic Of The GAME
while True:
    for event in pygame.event.get(): # accepts the event
        if event.type == pygame.QUIT: # quit event
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN: # when keyboard key is pressed
            if event.key == pygame.K_RIGHT or event.key == ord('d'): # Right Move
                changeTo = 'RIGHT'
            if event.key == pygame.K_LEFT or event.key == ord('a'): # Left Move
                changeTo = 'LEFT'
            if event.key == pygame.K_UP or event.key == ord('w'): # Up Move
                changeTo = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'): # Down Move
                changeTo = 'DOWN'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))  # post function first creates a event and inside it we emit a quit event

    # validation of direction
    if  game_over_flag==False and not (snakePos[0] > 710 or snakePos[0] < 0) and not (snakePos[1] > 450 or snakePos[1] < 0):            
        if changeTo == 'LEFT' and not direction =='RIGHT':
            direction = 'LEFT'
        if changeTo == 'RIGHT' and not direction =='LEFT':
            direction = 'RIGHT'
        if changeTo == 'UP' and not direction =='DOWN':
            direction = 'UP'
        if changeTo == 'DOWN' and not direction =='UP':
            direction = 'DOWN'

    # Value change after direction change
    if direction == 'RIGHT':
        snakePos[0] += 10
    if direction == 'LEFT':
        snakePos[0] -= 10
    if direction == 'UP':
        snakePos[1] -= 10
    if direction == 'DOWN':
        snakePos[1] += 10

    # Snake Body Mechanism
    snakeBody.insert(0, list(snakePos))
    if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
        score += 1
        foodSpawn = False

    #Change snake color to a random color when it picks up a point
        snake_color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    else:
        snakeBody.pop()
    
    #Food spawn
    if foodSpawn == False:
        foodPos = [random.randrange(1,72)*10,random.randrange(1,46)*10]
    foodSpawn = True

    playSurface.fill(('cadetblue2'))
    draw_ocean()

    for pos in snakeBody:
        pygame.draw.rect(playSurface, snake_color, pygame.Rect(pos[0],pos[1],10,10))
    pygame.draw.rect(playSurface,dark_red,pygame.Rect(foodPos[0],foodPos[1],10,10))

    # Boundary Condition
    if snakePos[0] > 710 or snakePos[0] < 0:
        update_score(score)
        draw_button()
        gameOver()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_x, mouse_y):
                snakePos = [100, 50]
                snakeBody = [[100, 50], [90, 50], [80, 50]]
                foodPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
                foodSpawn = True
                direction = 'RIGHT'
                changeTo = direction
                score = 0
                snake_speed = 10
                initscore = 0
            

    if snakePos[1] > 450 or snakePos[1] < 0:
        update_score(score)
        draw_button()
        gameOver()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_x, mouse_y):
                snakePos = [100, 50]
                snakeBody = [[100, 50], [90, 50], [80, 50]]
                foodPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
                foodSpawn = True
                direction = 'RIGHT'
                changeTo = direction
                score = 0
                snake_speed = 10
                initscore = 0
            

    # Self Body Collision
    for block in snakeBody[1:]:
        if snakePos[0] == block[0] and snakePos[1] == block[1]:
            update_score(score) 
            game_over_flag=True
            break              

    if game_over_flag:
        draw_button()
        gameOver()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_x, mouse_y) and game_over_flag:
                snakePos = [100, 50]
                snakeBody = [[100, 50], [90, 50], [80, 50]]
                foodPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
                foodSpawn = True
                direction = 'RIGHT'
                changeTo = direction
                score = 0
                snake_speed = 10
                initscore = 0
                game_over_flag = False
                              
    showScore()
    # FPS CONTROL
    pygame.display.update()

    if score == initscore+3:
        snake_speed+=5
        initscore = score
    fpsController.tick(snake_speed)
