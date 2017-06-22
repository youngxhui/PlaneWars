# 微信打飞机 python 实现

# 用技术和软件

python 2.7

pygame 1.9.3

pyCharm

#  准备工作

1.  安装好 pygame 在第一次使用 pygame 的时候，pyCharm 会自动 install pygame。
2.  下载好使用的素材。



# 技术实现

## 初始化 pygame

首先要初始化 pygame ，之后设定一些基本的要点，比如窗口大小（尽量避免魔法数字），窗口标题以及背景图像。pygame 通过加载图片，最后返回一个 surface 对象，我们不需要关系图片的格式。但是通过 `convert()` 这个函数，会使我们的图片转换效率提高。

```python
# coding=utf8

import pygame

WIDTH = 480
HEIGHT = 800

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('飞机大战')

background = pygame.image.load('resources/image/background.png').convert()

screen.fill(0)
screen.blit(background, (0, 0))
```

所有的图片都已左上角为原点 (0,0)。

## 显示窗口

如果我们这样设定，当我们运行的时候，窗口会一闪而过，并不会出现我们想象的画面。因为窗口只是运行一下就会关闭，所以我们要写一个循环，使窗口一直保持出现。当然如果我们简单的写一个 while True那么我们的程序就出现了死循环，卡死。

![](http://7xt81u.com1.z0.glb.clouddn.com/flyerroe.png)



所以还需要写个退出。

```python
while True:
    screen.fill(0)
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
```



## 显示飞机

首先我们要初始化我们的主角飞机

任就需要加载我们需要的资源，我们的资源文件里已经准备好各种各样的飞机，但是他们都在一张图上。

![](http://7xt81u.com1.z0.glb.clouddn.com/shoot.png)

同时我们的资源文件里还有一个叫做 `shoot.pack` 的文件，里面记录了每个图片所在的位置。

我们通过下面的代码加载资源图片，并且获得我们需要的主角飞机。

```python
plane_img = pygame.image.load('resources/image/shoot.png')

player = plane_img.subsurface(pygame.Rect(0, 99, 102, 126))
```

将 player 显示在屏幕上，并且刷新屏幕

```python
screen.blit(player, [100, 400])

pygame.display.update()
```

效果如下

![](http://7xt81u.com1.z0.glb.clouddn.com/flyplayer.png)

## 让飞机 “飞” 起来

飞机已经出现在我们的屏幕上了，现在需要让飞机动起来让他可以上下左右的移动。

首先要获取键盘事件，获取键盘上什么按键被按下。

```python
key_pressed = pygame.key.get_pressed()
```

通过 `key_pressed` 获取当前的键盘按键。并进行判断，这里写了四个函数进行对 player 移动。

```python
if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
    player.moveUp()
if key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
    player.moveDown()
if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
    player.moveLeft()
if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
    player.moveRight()
```

下一步就是完善这四个方法。

简单的说就是按下方向键的时候(w,a,s,d)飞机向四周移动，但是不能移动离开屏幕。

此时我们就应该把我们的飞机形成一个类，类里面有控制飞机的方法。

这里写类比较麻烦一点



### Player的出现

首先要明确一点，这个类需要什么。

我们之前对 player 有什么操作？定义了他的图片和他出现的位置。所以我们的构造方法就要初始化这些值。



```python
class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, player_position):
        pygame.sprite.Sprite.__init__(self)
        self.img = plane_img.subsurface(player_rect)
        self.rect = player_rect
        self.rect.topleft = player_position
```

简单的说就是获取飞机的图片，初始化飞机的矩形区域。`rect` 该属性会获得四个值。分别是左上角x ,y坐标，矩形的宽度。`topleft` 初始化飞机的左上角坐标，也就是飞机出现的位置。如下图所示。

![](http://7xt81u.com1.z0.glb.clouddn.com/surfaceposition.jpg)



### player的控制

当飞机出现了，我们就应该实现我们在循环里写的方法。我们首先要判断它还在不在屏幕内，不能让飞机飞出屏幕。可以通过 `rect.top`,`rect.bottom`,`rect.left`,`rect.right`四个方法获取飞机图片的上下左右四个边界值。

这样我们就能对飞机进行判断

```python
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
```
这里的 `move` 是我们对飞机的移动的位移定义的产量。

## 让子弹飞
子弹要沿着发射方向射出去。可以在屏幕上一直移动，直到移出屏幕。
我们只要有定义一个子弹对象，让这个对象显示在屏幕上就可以。
先定义飞机子弹类，基本和定义 `player` 一样，获得图片，裁剪图片，设置图片初始位置，在屏幕上显示图片
```python
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_image, bullet_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.midbottom = bullet_position


        
# 省略其他代码

# 加载子弹图片
bullet_rect = pygame.Rect(69, 78, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)

# 省略其他代码

while True:

    # 省略其他代码
    
    screen.blit(bullet.img, bullet.rect)
    
    # 省略其他代码
    
```

运行结果
![](http://7xt81u.com1.z0.glb.clouddn.com/bulletShow.jpg)


下一步就是让飞机的子弹跟随飞机。
我们需要在 Player 类里面添加方法。
首先我们规定，按下空格发射子弹。
```python
    if key_pressed[pygame.K_SPACE]:
        player.shoot()
```
完善shoot方法。子弹类已经有了，我们每次只要在按下空格的时候创建一个对象就好。
首先要每次传入一个子弹的图像，然后还有出现位置，这样子弹才能跟随飞机。
定义一个`pygame.sprite.Group()` 来存放精灵组。这样我们就能把我们的子弹都放进去。
 ``` python
     def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)
 ```

每次按下空格的时候传入一个子弹图片

```python
    if key_pressed[pygame.K_SPACE]:
        player.shoot(bullet_img)
```
最后我们只需要在屏幕上进行子弹的绘制即可。

```python
player.bullets.draw(screen)
```

这样我们的子弹就会跟随飞机出现。

![](http://7xt81u.com1.z0.glb.clouddn.com/bulletShow2.jpg)

下一步就是让子弹在屏幕上移动。

创建移动的方法。

```python
    def move(self):
        self.rect.top -= self.move
```

因为我们的子弹在 bullets 里，所以我们仅需要一个循环，遍历每个子弹，之后移动即可。当子弹移出屏幕的时候我们只要在 `bullets` 中移出就可以。

```python

    for bullet in player.bullets:
        bullet.bulletMove()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

```
结果
![](http://7xt81u.com1.z0.glb.clouddn.com/playerflyshoot.gif)

这个和我们的预期还是有差别的，频率太快了。

关于pygame 的键盘重复事件 官方好像并没有这个设置。那么我们只能在添加一个计数器，通过计算器的数值来判断子弹是否发射。这里的数值是多次测试后，自己感觉一个比较满意的频率。可以自己调整。

```python
# 省略其他代码

# 子弹频率
SHOOT_PC = 0
```
在键盘事件中我们需要判断频率。

```python
    if key_pressed[pygame.K_SPACE]:
        SHOOT_PC = SHOOT_PC + 1
        if SHOOT_PC % 400 == 0:
            player.shoot(bullet_img)

```

player 的飞机就算基本绘制好了

![](http://7xt81u.com1.z0.glb.clouddn.com/playerflyshoot2.gif)
## 绘制敌机

下一步就是绘制敌机。敌机是从屏幕上方移动到屏幕下方。我们任就需要一个类来设置敌机。设置类任就和我们前面的差不多，加载资源，设置 `rect`，设置位置。

```python

# 加载敌机图片

enemy_rect = pygame.Rect(267, 347, 57, 51)
enemy_img = plane_img.subsurface(enemy_rect)
enemy_position = [200, 200]
enemy = Enemy(enemy_img, enemy_position)


# 敌机类

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = enemy_position
```

最后在屏幕显示出来

```python
screen.blit(enemy_img, enemy_rect)
```

![](http://7xt81u.com1.z0.glb.clouddn.com/enemy.jpg)


现在我们就应该想想敌机的特点了，其实他和子弹的特点基本一直，只不过方向不一样而已。还有一点是敌机是随机生成的。

```python
# 敌机计数器
EnEMY_PC = 0
# 省略代码
enemy_position = [random.randint(0, WIDTH - enemy_rect.width), 0]
        enemy = Enemy(enemy_img, enemy_position)
        enemies.add(enemy)
```
我们随机在顶部生成飞机。

![](http://7xt81u.com1.z0.glb.clouddn.com/enemyshow.gif)

这个方式的情况和子弹其实差不多，我们应该给出现敌机确定一个频率。

```
    if EnEMY_PC % 500 == 0:
        enemy_position = [random.randint(0, WIDTH - enemy_rect.width), 0]
        enemy = Enemy(enemy_img, enemy_position)
        enemies.add(enemy)

    EnEMY_PC = EnEMY_PC + 1
```
这样的话出现情况就变得缓慢。下一步实现敌机的移动。敌机的移动原理和子弹的移动其实也是一样的。不多解释

移动方法
```python
    def enemyMove(self):
        self.rect.top += self.move
```

移动实现
```python
 for enemy in enemies:
        enemy.enemyMove()
        if enemy.rect.top > HEIGHT:
            enemies.remove(enemy)

    enemies.draw(screen)
```

![](http://7xt81u.com1.z0.glb.clouddn.com/enemyMove.gif)

## 碰撞检测

飞机和敌机还有子弹都有了，我们现在需要进行完成碰撞检测。有下面几种场景。

1. 敌机和玩家碰撞在一起
2. 子弹和敌机碰撞在一起

无论是那种情况的碰撞，其实就是两张图片有了交集。
如图
![](http://7xt81u.com1.z0.glb.clouddn.com/penz.jpg)
pygame 给我们提供了碰撞检测的方法。首先两个对象必须是 `sprite` 。通过 `pygame.sprite.collide_rect()` 进行碰撞检测。

我们先进行一个测试
```python
    if pygame.sprite.collide_rect(enemy, player):
        print '检测成功'
```

结果

>  检测成功

此时我们就可以完成,当玩家和敌机发生碰撞,游戏结束,当子弹和敌机碰撞,敌机消失.

同样的 pygame 给我们提供了一个 `pygame.sprite.groupcollide()` 用于Group 之间的碰撞检测.当发生碰撞的时候这两个对象都会在 `Group` 中移出.

用于检测敌机和子弹
```
pygame.sprite.groupcollide(enemies, player.bullets, 1, 1)
```

敌机和子弹的关系已经和好的处理.
处理敌机和玩家飞机的关系.

我们需要在 `Player` 里添加一个属性判断当前玩家是否被击中的 `boolean` 值.当集中的时候把属性改为 `True`.当为 `True` 的时候游戏结束.也就是我们一开始设置的循环就会结束.所以我们需要更改之前写的一些代码,使它更加完善.

在 Player 类里面添加是否击中属性.

```python
self.is_hit = False
```

修改循环

```python

RUN = True

while RUN:
    # 省略代码
        if pygame.sprite.collide_rect(enemy, player):
        player.is_hit = True
        RUN = False
    # 省略代码
```

执行结果

![](http://7xt81u.com1.z0.glb.clouddn.com/gameover2.gif)


当玩家被击中的时候,在显示一张 GameOver 图片提示

```
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
```

做到这里基本算是实现了飞机大战.但是还有很多细节处理.

![](http://7xt81u.com1.z0.glb.clouddn.com/finish1.gif)

# 细节处理

Todo
===

## 精细的碰撞检测

## 动画

## 音乐

## 分数

## 等级

## boss

