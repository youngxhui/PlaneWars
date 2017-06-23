# coding=utf8

import pygame
import random
import time
import math

WIDTH = 480
HEIGHT = 800

SHOOT_PC = 0
ENEMY_PC = 0

enemy_add = 300
player_shoot = 0

score = 0
level = 1

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('飞机大战')

background = pygame.image.load('resources/image/background.png').convert()

plane_img = pygame.image.load('resources/image/shoot.png')

shootMusic = pygame.mixer.Sound('resources/sound/bullet.mp3')


# 子弹对象

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_image, bullet_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.midbottom = bullet_position
        self.move = 1.1

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
        shootMusic.play()


# 敌机类

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_shoot_img, enemy_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = enemy_position
        self.shoot_imgs = enemy_shoot_img
        self.move = 1
        self.shoot_index = 0

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

enemy_rect = pygame.Rect(534, 612, 57, 43)
enemy_img = plane_img.subsurface(enemy_rect)
enemies = pygame.sprite.Group()

# 加载敌机被击中图片
enemies_shoot_img = [plane_img.subsurface(pygame.Rect(267, 347, 57, 43)),
                     plane_img.subsurface(pygame.Rect(873, 697, 57, 43)),
                     plane_img.subsurface(pygame.Rect(267, 296, 57, 43)),
                     plane_img.subsurface(pygame.Rect(930, 697, 57, 43))]

enemies_shoot = pygame.sprite.Group()

backgroundMusic = pygame.mixer.music.load('resources/sound/game_music.mp3')
pygame.mixer.music.play(-1, 0.0)

enemy_shoot_sound = pygame.mixer.Sound('resources/sound/enemy3_down.mp3')
enemy_shoot_sound.set_volume(1.0)
RUN = True

while RUN:
    screen.fill(0)
    screen.blit(background, (0, 0))

    if not player.is_hit:
        screen.blit(player.image[player.img_index], player.rect)
        player.img_index = SHOOT_PC / 247
    else:
        player.img_index = player_shoot / 247
        screen.blit(player.image[player.img_index], player.rect)
        player_shoot += 31
        if player_shoot > 495:
            RUN = False
            time.sleep(1)

    if ENEMY_PC % enemy_add == 0:
        enemy_position = [random.randint(0, WIDTH - enemy_rect.width), 0]
        enemy = Enemy(enemy_img, enemies_shoot_img, enemy_position)
        enemies.add(enemy)

    ENEMY_PC = ENEMY_PC + 2
    if ENEMY_PC == 1000:
        ENEMY_PC = 0

    for bullet in player.bullets:
        bullet.bulletMove()
        if bullet.rect.bottom <= 0:
            player.bullets.remove(bullet)

    player.bullets.draw(screen)

    for enemy in enemies:
        enemy.enemyMove()
        if pygame.sprite.collide_circle_ratio(0.6)(player, enemy):
            enemies_shoot.add(enemy)
            enemies.remove(enemy)
            player.is_hit = True
            break
        if enemy.rect.top > HEIGHT:
            enemies.remove(enemy)

    for enemy_shoots in enemies_shoot:
        if enemy_shoots.shoot_index == 0:
            pass
        if enemy_shoots.shoot_index > 70:
            enemies_shoot.remove(enemy_shoots)
            score += 100
            continue
        screen.blit(enemy_shoots.shoot_imgs[enemy_shoots.shoot_index / 20], enemy_shoots.rect)
        enemy_shoots.shoot_index += 1

    enemies.draw(screen)

    # 分数显示
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    screen.blit(score_text, text_rect)

    if score == 100 * (level ** 2 + level):
        level += 1
        enemy_add -= 25

    # 等级显示
    level_font = pygame.font.Font(None, 42)
    level_text = level_font.render('Level ' + str(level), True, (128, 128, 128, 128))
    level_rect = level_text.get_rect()
    level_rect.midtop = [240, 10]
    screen.blit(level_text, level_rect)

    enemies_is_shoot = pygame.sprite.groupcollide(enemies, player.bullets, 0.6, 0.8)

    for enemy_shoot in enemies_is_shoot:
        enemy_shoot_sound.play()
        enemies_shoot.add(enemy_shoot)

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
        SHOOT_PC = SHOOT_PC + 5
        if SHOOT_PC >= 495:
            SHOOT_PC = 0

    pygame.display.update()

    # 退出程序
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

if not RUN:
    pygame.mixer.music.stop()

GAMEOVER = True

# 加载gameOver图片

gameOver_image = pygame.image.load('resources/image/gameover.png')

# 加载GameOVer音乐

gameOver_music = pygame.mixer.music.load('resources/sound/game_over.mp3')
pygame.mixer.music.play(0, 0.0)

while GAMEOVER:
    screen.fill(0)
    screen.blit(gameOver_image, (0, 0))

    pygame.display.update()

    if pygame.mixer.music.get_busy() == 0:
        pygame.quit()
        exit()
