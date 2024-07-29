#!/usr/bin/env python
# -*- coding: utf-8 -*-
#player.py
from pygame import *
import pyganim
import os
import blocks
import monsters
from platformerhabrahabr import Menu

MOVE_SPEED = 13
MOVE_EXTRA_SPEED = 2
WIDTH = 22
HEIGHT = 32
COLOR =  "#888888"
JUMP_POWER = 20
JUMP_EXTRA_POWER = 1
GRAVITY = 2
ANIMATION_DELAY = 0.07
ANIMATION_SUPER_SPEED_DELAY = 0.04

if os.environ.get('WEB_ENV'):
    BASE_DIR = '/'  # для веб-версии
else:
    BASE_DIR = os.path.dirname(__file__)  # для локальной версии

ICON_DIR = os.path.join(BASE_DIR, 'mario')  # Путь к каталогу с файлами Mario

ANIMATION_RIGHT = [os.path.join(ICON_DIR, f'r{i}.png') for i in range(1, 6)]
ANIMATION_LEFT = [os.path.join(ICON_DIR, f'l{i}.png') for i in range(1, 6)]
ANIMATION_JUMP_LEFT = [(os.path.join(ICON_DIR, 'jl.png'), 0.1)]
ANIMATION_JUMP_RIGHT = [(os.path.join(ICON_DIR, 'jr.png'), 0.1)]
ANIMATION_JUMP = [(os.path.join(ICON_DIR, 'j.png'), 0.1)]
ANIMATION_STAY = [(os.path.join(ICON_DIR, '0.png'), 0.1)]

class Player(sprite.Sprite):
    def __init__(self, x, y,menu):
        sprite.Sprite.__init__(self)
        self.menu = menu
        self.xvel = 0   #скорость перемещения. 0 - стоять на месте
        self.startX = x # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.yvel = 0 # скорость вертикального перемещения
        self.onGround = False # На земле ли я?
        self.image = Surface((WIDTH,HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT) # прямоугольный объект
        self.image.set_colorkey(Color(COLOR)) # делаем фон прозрачным
#        Анимация движения вправо
        boltAnim = []
        boltAnimSuperSpeed = []
        self.checkpoint = None
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
            boltAnimSuperSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        self.boltAnimRightSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimRightSuperSpeed.play()
#        Анимация движения влево        
        boltAnim = []
        boltAnimSuperSpeed = [] 
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
            boltAnimSuperSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        self.boltAnimLeftSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimLeftSuperSpeed.play()
        
        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0)) # По-умолчанию, стоим
        
        self.boltAnimJumpLeft= pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()
        
        self.boltAnimJumpRight= pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()
        
        self.boltAnimJump= pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()
        self.winner = False

    def update(self, left, right, up, running, platforms):
        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
                if running and (left or right):  # если есть ускорение и мы движемся
                    self.yvel -= JUMP_EXTRA_POWER  # то прыгаем выше
                self.image.fill(Color(COLOR))
                self.boltAnimJump.blit(self.image, (0, 0))

        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n
            self.image.fill(Color(COLOR))
            if running:  # если ускорение
                self.xvel -= MOVE_EXTRA_SPEED  # то передвигаемся быстрее
                if not up:  # и если не прыгаем
                    self.boltAnimLeftSuperSpeed.blit(self.image, (0, 0))  # то отображаем быструю анимацию
            else:  # если не бежим
                if not up:  # и не прыгаем
                    self.boltAnimLeft.blit(self.image, (0, 0))  # отображаем анимацию движения
            if up:  # если же прыгаем
                self.boltAnimJumpLeft.blit(self.image, (0, 0))  # отображаем анимацию прыжка

        if right:
            self.xvel = MOVE_SPEED  # Право = x + n
            self.image.fill(Color(COLOR))
            if running:
                self.xvel += MOVE_EXTRA_SPEED
                if not up:
                    self.boltAnimRightSuperSpeed.blit(self.image, (0, 0))
            else:
                if not up:
                    self.boltAnimRight.blit(self.image, (0, 0))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
            if not up:
                self.image.fill(Color(COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        collision_result = self.collide(0, self.yvel, platforms)
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if isinstance(p, blocks.BlockDie) or isinstance(p, monsters.Monster) or isinstance(p,
                                                                                                   blocks.LavaBlock) or isinstance(
                        p, blocks.InvisibleDeadlyBlock):
                    self.die()
                elif isinstance(p, blocks.BlockTeleport):
                    print("Игрок столкнулся с телепортом")
                    p.teleport(self)
                elif isinstance(p, blocks.Letter):
                    if not p.collected:
                        p.collected = True
                        self.menu.add_image(p.info_image)
                        print(f"Collected letter: {p.letter_number}")
                        return f"show_number_{p.letter_number}"
                elif isinstance(p, blocks.Spring) or isinstance(p, blocks.CloudSpringBlock):
                    if yvel > 0:  # Если игрок падает на пружину или облако-пружину
                        p.boost(self)
                elif isinstance(p, blocks.CloudBlock):
                    if yvel > 0:  # Игрок может стоять на облаке
                        self.rect.bottom = p.rect.top
                        self.onGround = True
                        self.yvel = 0
                else:
                    if xvel > 0:
                        self.rect.right = p.rect.left
                    if xvel < 0:
                        self.rect.left = p.rect.right
                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.onGround = True
                        self.yvel = 0
                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        self.yvel = 0

        return None

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY

    def die(self):
        time.wait(500)
        if self.checkpoint:
            self.teleporting(self.checkpoint.rect.x, self.checkpoint.rect.y)
        else:
            self.teleporting(self.startX, self.startY)