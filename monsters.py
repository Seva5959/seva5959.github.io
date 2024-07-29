#!/usr/bin/env python
# -*- coding: utf-8 -*-
#monsters.py
from pygame import *
import pyganim
import os

MONSTER_WIDTH = 32
MONSTER_HEIGHT = 32
MONSTER_COLOR = "#2110FF"

if os.environ.get('WEB_ENV'):
    BASE_DIR = '/'  # для веб-версии
else:
    BASE_DIR = os.path.dirname(__file__)  # для локальной версии

ICON_DIR = os.path.join(BASE_DIR, 'monsters')  # Путь к каталогу с файлами монстров

ANIMATION_MONSTERHORYSONTAL = [
    os.path.join(ICON_DIR, 'fire1.png'),
    os.path.join(ICON_DIR, 'fire2.png')
]

class Monster(sprite.Sprite):
    def __init__(self, x, y, left, up):
        sprite.Sprite.__init__(self)
        self.image = Surface((MONSTER_WIDTH, MONSTER_HEIGHT))
        self.image.fill(Color(MONSTER_COLOR))
        self.rect = Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.image.set_colorkey(Color(MONSTER_COLOR))
        self.startX = x
        self.startY = y
        self.maxLengthLeft = 200
        self.maxLengthUp = 0
        self.xvel = left
        self.yvel = up
        boltAnim = []
        for anim in ANIMATION_MONSTERHORYSONTAL:
            boltAnim.append((anim, 0.3))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self, platforms):
        self.image.fill(Color(MONSTER_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

        self.rect.y += self.yvel
        self.rect.x += self.xvel

        self.collide(platforms)

        if abs(self.startX - self.rect.x) > self.maxLengthLeft:
            self.xvel = -self.xvel
        if abs(self.startY - self.rect.y) > self.maxLengthUp:
            self.yvel = -self.yvel

    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:
                self.xvel = -self.xvel
                self.yvel = -self.yvel