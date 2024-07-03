import pygame
import random
import math

# pygame setup
pygame.init()

# images
background = pygame.image.load("./assets/img/background.png")
ufo = pygame.image.load("./assets/img/ufo.png")
ship = pygame.image.load("./assets/img/ship.png")
bullet = pygame.image.load("./assets/img/bullet.png")

# screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

# player
player_x = 370
player_y = 480
player_x_change = 0

# aliens
alien_img = []
alien_x = []
alien_y = []
alien_x_change = []
alien_y_change = []
num_of_aliens = 6

for i in range(num_of_aliens):
    alien_img.append(pygame.image.load("./assets/img/ufo.png"))
    alien_x.append(random.randint(0, 736))
    alien_y.append(random.randint(50, 150))
    alien_x_change.append(2)
    alien_y_change.append(40)

# bullets
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(ship, (x, y))


def alien(x, y, i):
    screen.blit(alien_img[i], (x, y))


def shoot(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 15, y + 10))


def collide(alien_x, alien_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(alien_x - bullet_x, 2) + (math.pow(alien_y - bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:
    screen.blit(background, (0, 0))
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player_x_change = -5
            if event.key == pygame.K_d:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    shoot(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                player_x_change = 0

    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    for i in range(num_of_aliens):
        if alien_y[i] > 440:
            for j in range(num_of_aliens):
                alien_y[j] = 2000
            break

        alien_x[i] += alien_x_change[i]
        if alien_x[i] <= 0:
            alien_x_change[i] = 2
            alien_y[i] += alien_y_change[i]
        elif alien_x[i] >= 735:
            alien_x_change[i] = -2
            alien_y[i] += alien_y_change[i]

        # collision
        collision = collide(alien_x[i], alien_y[i], bullet_x, bullet_y)
        if collision:
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            alien_x[i] = random.randint(0, 736)
            alien_y[i] = random.randint(50, 150)

        alien(alien_x[i], alien_y[i], i)

    # bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        shoot(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
