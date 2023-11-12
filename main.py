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
import time
from random import randint


def game_exit(): # функция закрытия окна программы
	
	pg.quit()
	sys.exit(0)

def game(): # главная функция (сама игра)
			
	pg.init() # инициализация окна
	clock = pg.time.Clock()
	
	env = media.school_map['road']['obj']
	gamer = phys.Player([741, 650])
	step = 5
	flag = -1
	
	teacher = phys.Teacher('teacher')
	
	NPCs = []
	NPCs.append(phys.Mob([250, 600]))

	time_now, time_check = int(time.time()), int(time.time())

	while True:
				
		time_now = int(time.time())
		clock.tick(30)
		
		if time_now-time_check == 5: flag += 1
		
		for event in pg.event.get():
						
			if event.type == QUIT: game_exit()
			
			if pg.key.get_pressed()[K_w]: gamer.walk(0, -1*step, 'road')
			if pg.key.get_pressed()[K_a]: gamer.walk(-1*step, 0, 'road')
			if pg.key.get_pressed()[K_s]: gamer.walk(0, step, 'road')
			if pg.key.get_pressed()[K_d]: gamer.walk(step, 0, 'road')
			
			if pg.key.get_pressed()[K_UP]: gamer.walk(0, -1, 'road')
			if pg.key.get_pressed()[K_LEFT]: gamer.walk(-1, 0, 'road')
			if pg.key.get_pressed()[K_DOWN]: gamer.walk(0, 1, 'road')
			if pg.key.get_pressed()[K_RIGHT]: gamer.walk(1, 0, 'road')
			
			elif event.type == KEYUP:
				
				if event.key == K_SPACE: game_exit()
				if event.key == K_TAB: gamer.stealth(1); flag += 1
		
		c = 0
		for npc in NPCs:
			
			if gamer.get_pos()[0]+(gamer.get_size()[0]//2) in \
			range(npc.get_pos()[0]-20, npc.get_pos()[0]+npc.get_size()[0]+20) \
			   and\
			   gamer.get_pos()[1]+(gamer.get_size()[1]//4) in \
			range(npc.get_pos()[1]-20, npc.get_pos()[1]+npc.get_size()[1]//2+50):
			
				gamer.stealth(1)
				break
			
			else: c += 1
			
		if c == len(NPCs) and flag%2 == 1: gamer.stealth(0)
							
		(media.screen).blit(env, (0, 0))
		[npc.draw() for npc in NPCs]
		gamer.draw()
		
		if teacher.search(gamer.get_pos(), 
				  gamer.get_size(), 
				  gamer.get_model()//2) == 1:
			
			x, y = teacher.vector(gamer.get_pos())
			teacher.walk(x, y)	
		else: teacher.teachers_path()
		teacher.draw()

		if gamer.get_pos()[0]+(gamer.get_size()[0]//2) in \
		range(teacher.get_pos()[0]-20, teacher.get_pos()[0]+teacher.get_size()[0]+20) \
			   and\
		   gamer.get_pos()[1]+(gamer.get_size()[1]//4) in \
		range(teacher.get_pos()[1]-20, teacher.get_pos()[1]+teacher.get_size()[1]//2+50) \
			   and\
		   gamer.get_model() < 2:
			
			gamer.heat()
			gamer.stealth(1)
			flag += 1
			time_check = int(time.time())

		pg.display.update()
			
	
if __name__ == '__main__':
	
	game() # Андрей - гандон
	# надеюсь код читать никто не будет
	# иначе придется потом это чистить