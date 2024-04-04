#匯入函式庫
import pygame
import time
import random

pygame.mixer.init()
pygame.init()

#初始化設定
#顏色
white = (255, 255, 255)
gray = (80,80,80)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (50, 153, 213)

#視窗大小
dis_size = 600
dis = pygame.display.set_mode((dis_size, dis_size))
pygame.display.set_caption('Snake Game')

#方塊大小、速度
snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont(None, 30)

#匯入外部資源
intro_image = pygame.image.load("homepage_image.jpg")
intro_image2 = pygame.image.load("homepage_image2.jpg")
restart_image = pygame.image.load("gameover_image.jpg")
die_sound = pygame.mixer.Sound("die.mp3") 
eat_sound = pygame.mixer.Sound("eat.mp3") 
button_sound = pygame.mixer.Sound("button.mp3") 


#構成個要件的函數
#蛇
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, blue, [x[0], x[1], snake_block, snake_block])

#分數顯示
def Your_score(score):
    value = font_style.render("Your Score: " + str(score), True, white)
    dis.blit(value, [0, 0])

#網格背景
def draw_grid():
    for x in range(0, dis_size, snake_block):
        pygame.draw.line(dis, gray, (x, 0), (x, dis_size))
    for y in range(0, dis_size, snake_block):
        pygame.draw.line(dis, gray, (0, y), (dis_size, y))

#遊戲介紹頁面
def game_intro():
    pygame.mixer.music.load("background_music.mp3")  
    pygame.mixer.music.play(-1)  
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    button_sound.play()
                    dis.blit(intro_image2, (0, 0))
                    pygame.display.update()
                    time.sleep(1.5)  
                    intro = False
            if event.type == pygame.QUIT:
                pygame.quit()

        dis.blit(intro_image, (0, 0))

        pygame.display.update()

    gameLoop()

#遊戲主程式
def gameLoop():
    game_over = False

    x1 = dis_size / 2
    y1 = dis_size / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_size - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, dis_size - snake_block) / 20.0) * 20.0

    score = 0

#遊戲進行中的程式
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

#蛇的移動程式
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
        
        #蛇碰到邊界
        if x1 >= dis_size or x1 < 0 or y1 >= dis_size or y1 < 0:
            die_sound.play()
            game_over = True
            pygame.mixer.music.stop()

        x1 += x1_change
        y1 += y1_change
        dis.fill(black)

        draw_grid()

        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_List.append(snake_head)
        
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)
        pygame.display.update()
        
        #吃到食物的程式
        if x1 == foodx and y1 == foody:
            eat_sound.play()

            #用random的函示庫,來隨機生成下一個食物的位置
            foodx = round(random.randrange(0, dis_size - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, dis_size - snake_block) / 20.0) * 20.0
            Length_of_snake += 1
            score += 1

        pygame.time.Clock().tick(snake_speed)
    
#遊戲結束介面
    dis.blit(restart_image, (0, 0))
    pygame.display.update()
    wait_for_space()

#在遊戲介面中偵測空白鍵，等待重新開始
def wait_for_space():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    button_sound.play()
                    game_intro()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

game_intro()