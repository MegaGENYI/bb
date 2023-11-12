#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PyGame

import pygame as pg
from pygame.locals import *

# mine - мои то есть

import phys
import media

# other

import threading
import sys
from time import sleep
from random import randint


def game_exit(): # функция закрытия окна программы
	
	pg.quit()
	sys.exit(0)

def game(): # главная функция (сама игра)
			
	pg.init() # инициализация окна
	clock = pg.time.Clock()
	
	env = media.school_map['road']['obj']
	gamer = phys.Player([741, 650])
	step = 10

	while True:
				
		clock.tick(30)
		
		for event in pg.event.get():
						
			if event.type == QUIT: game_exit()
			
			if pg.key.get_pressed()[K_w]: gamer.walk(0, -1*step, 'road')
			if pg.key.get_pressed()[K_a]: gamer.walk(-1*step, 0, 'road')
			if pg.key.get_pressed()[K_s]: gamer.walk(0, step, 'road')
			if pg.key.get_pressed()[K_d]: gamer.walk(step, 0, 'road')
			
			elif event.type == KEYUP:
				
				if event.key == K_SPACE: game_exit()		
						
		(media.screen).blit(env, (0, 0))
		gamer.draw()
		pg.display.update()
			
	
if __name__ == '__main__':
	
	game() # Андрей - гандон
	# надеюсь код читать никто не будет
	# иначе придется потом это чистить