# coding=utf8

import pygame
import random
import time

WIDTH = 480
HEIGHT = 800

SHOOT_PC = 0
EnEMY_PC = 0

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('飞机大战')

background = pygame.image.load('resources/image/background.png').convert()

plane_img = pygame.image.load('resources/image/shoot.png')


# 子弹对象

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_image, bullet_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.midbottom = bullet_position
        self.move = 1

    def bulletMove(self):
        self.rect.top -= self.move


# player对象

class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, player_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = []
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        self.rect = player_rect[0]
        self.rect.topleft = player_position
        self.img_index = 0
        self.move = 1
        self.bullets = pygame.sprite.Group()
        self.is_hit = False

    # player 移动

    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.move

    def moveDown(self):
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        else:
            self.rect.bottom += self.move

    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.move

    def moveRight(self):
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        else:
            self.rect.right += self.move

    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)


# 敌机类

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = enemy_position
        self.move = 1

    def enemyMove(self):
        self.rect.top += self.move


# 加载player 飞机图片

player_rect = [pygame.Rect(0, 99, 102, 126),
               pygame.Rect(165, 360, 102, 126),
               pygame.Rect(165, 234, 102, 126),
               pygame.Rect(330, 624, 102, 126),
               pygame.Rect(330, 498, 102, 126),
               pygame.Rect(432, 624, 102, 126)]

player_position = [100, 400]
player = Player(plane_img, player_rect, player_position)

# 加载子弹图片
bullet_rect = pygame.Rect(69, 78, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)

# 加载敌机图片

enemy_rect = pygame.Rect(267, 347, 57, 51)
enemy_img = plane_img.subsurface(enemy_rect)
enemies = pygame.sprite.Group()

RUN = True

while RUN:
    screen.fill(0)
    screen.blit(background, (0, 0))

    screen.blit(player.image[player.img_index], player.rect)
    player.img_index = SHOOT_PC / 248

    if EnEMY_PC % 500 == 0:
        enemy_position = [random.randint(0, WIDTH - enemy_rect.width), 0]
        enemy = Enemy(enemy_img, enemy_position)
        enemies.add(enemy)

    EnEMY_PC = EnEMY_PC + 1

    for bullet in player.bullets:
        bullet.bulletMove()
        if bullet.rect.bottom <= 0:
            player.bullets.remove(bullet)

    player.bullets.draw(screen)

    for enemy in enemies:
        enemy.enemyMove()
        if enemy.rect.top > HEIGHT:
            enemies.remove(enemy)

    enemies.draw(screen)

    pygame.sprite.groupcollide(enemies, player.bullets, 0.6, 0.8)

    if pygame.sprite.collide_circle_ratio(0.6)(player, enemy):
        player.is_hit = True
        RUN = False

    # 获取键盘按键
    key_pressed = pygame.key.get_pressed()

    if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
        player.moveUp()
    if key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
        player.moveDown()
    if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
        player.moveLeft()
    if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
        player.moveRight()
    if key_pressed[pygame.K_SPACE]:
        if SHOOT_PC % 495 == 0:
            player.shoot(bullet_img)
        SHOOT_PC = SHOOT_PC + 1
        if SHOOT_PC >= 495:
            SHOOT_PC = 0

    pygame.display.update()

    # 退出程序
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

GAMEOVER = True

# 加载gameOver图片

gameOver = pygame.image.load('resources/image/gameover.png')

while GAMEOVER:
    screen.fill(0)
    screen.blit(gameOver, (0, 0))

    pygame.display.update()

    # 退出程序
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
