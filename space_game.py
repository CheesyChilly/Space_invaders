import pygame
import math
from pygame import mixer
import random

mixer.init()
mixer.music.load("Github/Space_invaders/assets/highbgm.mp3")
mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops=-1)

# variables
game_over = False
run = True
no_enemies = 10
x_res = 720
y_res = 720
game_pause = False

clock = pygame.time.Clock()

pygame.init()  # initializing the pygame
screen = pygame.display.set_mode((x_res, y_res))  # create a screen

pygame.display.set_caption("space invaders")  # Naming the window

background = pygame.image.load("Github/Space_invaders/assets/bg.jpeg")
cursorImg = pygame.image.load("Github/Space_invaders/assets/cursor.png").convert_alpha()
cursor = pygame.cursors.Cursor((9, 0), cursorImg)

icon = pygame.image.load("Github/Space_invaders/assets/mushroom 32x32.png")
pygame.display.set_icon(icon)  # applying the icon to the window


# creaing player
playerImg = pygame.image.load("Github/Space_invaders/assets/spaceship.png")
playerx = (x_res / 2) - 32
playery = y_res - 128
p_changex = 0

# creating enemy
enemyImg = []
enemyx = []
enemyy = []
e_changex = []
e_changey = []
enemy_speed = 4
left = no_enemies

for i in range(1, no_enemies + 1):
    enemyImg.append(pygame.image.load("Github/Space_invaders/assets/ufo.png"))
    enemyx.append(random.randint(32, (x_res - 96)))
    enemyy.append(random.randrange(32, (64 * 5), 64))
    e_changey.append(64)
    e_changex.append(enemy_speed)

# creating bullet
Bullet = pygame.image.load("Github/Space_invaders/assets/bullet.png")
bulletImg = pygame.transform.scale(Bullet, (32, 32))
bulletx = playerx + 32
bullety = y_res - 128
b_changey = 1
b_state = "ready"

# Score
score_value = 0
font = pygame.font.Font("Github/Space_invaders/assets/Mario-Kart-DS.ttf", 32)
scorex = 10
scorey = 10


def show_score(x, y):
    score = font.render("SCORE -    " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def restart(x, y):
    score = font.render("press R to restart.", True, (255, 255, 255))
    screen.blit(score, (x, y))


def final_score(x, y):
    score = font.render("TOTAL SCORE -    " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def number_e(x, y, n):
    score = font.render("Enemies -  " + str(n), True, (255, 255, 255))
    screen.blit(score, (x, y))


def bullet_fire(x, y):
    global b_state
    b_state = "fire"
    screen.blit(bulletImg, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def isCollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(
        (math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2))
    )
    if distance < 32:
        return True
    else:
        return False


def playerCollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(
        (math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2))
    )
    if distance < 64:
        return True
    else:
        return False


gameover_font = pygame.font.Font("Github/Space_invaders/assets/Mario-Kart-DS.ttf", 64)


def gameover_text():
    over_text = gameover_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (195, 300))


while run:
    # setting background color
    # screen.fill((20, 20, 20))
    clock.tick(60)
    pygame.mouse.set_cursor(cursor)
    if game_over:
        screen.fill((5, 5, 5))
        gameover_text()

    else:
        screen.blit(background, (0, 0))

    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        # looking for close action
        if event.type == pygame.QUIT:
            run = False
            mixer.music.stop()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                p_changex = 6

            if event.key == pygame.K_LEFT:
                p_changex = -6

            if event.key == pygame.K_w:
                if b_state == "ready":
                    bulletx = playerx + 16
                    bullet_fire(bulletx, bullety)
                    mixer.Channel(1).play(
                        pygame.mixer.Sound("Github/Space_invaders/assets/shoot.mp3")
                    )
                    mixer.Channel(1).set_volume(0.2)

            if event.key == pygame.K_r and game_over:
                # Restart the game
                b_state = "ready"
                game_over = False
                playerx = (x_res / 2) - 32
                playery = y_res - 128
                score_value = 0

                # Reset enemy positions and other necessary variables
                for i in range(no_enemies):
                    enemyx[i] = random.randint(32, (x_res - 96))
                    enemyy[i] = random.randrange(32, (64 * 5), 64)
                mixer.music.rewind()
                mixer.music.set_volume(0.4)

            if event.key == pygame.K_ESCAPE:
                game_pause = True
                screen.fill((45, 22, 5))

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                p_changex = 0

    playerx += p_changex

    for i in range(no_enemies):
        # enemy movement
        enemyx[i] += e_changex[i]
        if enemyx[i] < 0 + 32:
            # for i in range(no_enemies):
            e_changex[i] = enemy_speed
            enemyy[i] += e_changey[i]
        if enemyx[i] > x_res - 96:
            # for i in range(no_enemies):
            e_changex[i] = -enemy_speed
            enemyy[i] += e_changey[i]

        collision = isCollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            mixer.Channel(2).play(
                pygame.mixer.Sound("Github/Space_invaders/assets/enemy_death.mp3")
            )
            mixer.Channel(2).set_volume(0.2)
            # no_enemies -= 1
            bullety = y_res - 128
            b_state = "ready"
            score_value += 100
            enemyy[i] = random.randrange(32, (64 * 5), 64)
            enemyx[i] = random.randint(32, (x_res - 96))
            # enemyy[i] = 2000
            # left -= 1

        enemy(enemyx[i], enemyy[i], i)

        p_collision = playerCollision(enemyx[i], enemyy[i], playerx, playery)
        if p_collision:
            game_over = True
            for j in range(no_enemies):
                enemyy[j] = 2000
            mixer.music.set_volume(0)
            mixer.Channel(1).set_volume(0)
            b_state = "fi"
            mixer.Channel(0).play(
                pygame.mixer.Sound("Github/Space_invaders/assets/gameover.mp3")
            )
            mixer.Channel(0).set_volume(1)

            print("Gameover")

        # player movement
        if playerx < 0 + 32:
            playerx = 0 + 32
        if playerx >= x_res - 96:
            playerx = x_res - 96

        if bullety < 0:
            b_state = "ready"
            bullety = y_res - 128

        # bullet movement
        if b_state == "fire":
            bullet_fire(bulletx, bullety)
            bullety -= b_changey

        if game_over:
            player(playerx, 2000)
            final_score(218, 370)
            number_e(720 - 200, 2000, no_enemies)
            restart(218, 500)

        if game_over == False:
            player(playerx, playery)
            show_score(scorex, scorey)
            number_e(720 - 200, 720 - 32, no_enemies)

    pygame.display.update()

pygame.quit()
