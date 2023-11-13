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

def posled(data): return range(data[0], data[1]+1)

def lesson(): print('OK')

def game(mapp): # главная функция (сама игра)
		
	pg.init() # инициализация окна
	clock = pg.time.Clock() # установка ограничения по кадрам
	
	# настройка мира
	env = media.school_map[mapp]['obj']
	
	# создание игрового аватара
	gamer = phys.Player([741, 650])
	step = 5
	flag = -1
	
	# создание учителя (если есть)
	teacher = phys.Teacher(media.school_map[mapp]['teacher'])
	boss = phys.Boss(media.school_map[mapp]['boss'])
	
	# тупые нпс как же я вас ненавижу
	NPCs = []
	[NPCs.append(phys.Mob(d)) for d in media.school_map[mapp]['NPC']]

	# сверяемся со временем
	time_now, time_check = int(time.time()), int(time.time())

	# запуск игры
	while True:
				
		time_now = int(time.time())
		clock.tick(30)
		
		if time_now-time_check == 5: flag += 1
		
		# обрабатываем нажатия клавиш
		for event in pg.event.get():
						
			if event.type == QUIT: game_exit()
			
			if pg.key.get_pressed()[K_w]: gamer.walk(0, -1*step, mapp)
			if pg.key.get_pressed()[K_a]: gamer.walk(-1*step, 0, mapp)
			if pg.key.get_pressed()[K_s]: gamer.walk(0, step, mapp)
			if pg.key.get_pressed()[K_d]: gamer.walk(step, 0, mapp)
			
			if pg.key.get_pressed()[K_UP]: gamer.walk(0, -1, mapp)
			if pg.key.get_pressed()[K_LEFT]: gamer.walk(-1, 0, mapp)
			if pg.key.get_pressed()[K_DOWN]: gamer.walk(0, 1, mapp)
			if pg.key.get_pressed()[K_RIGHT]: gamer.walk(1, 0, mapp)
			
			if event.type == KEYDOWN:
				
				if event.key == K_e: # взаимодействие (будем расширять)
								
					if boss.get_be(): # если в поле действия босса (учителя)
											
						if gamer.get_pos()[0]+(gamer.get_size()[0]//2) in\
						posled(boss.get_collision()[0]) \
							and\
						   gamer.get_pos()[0]+(gamer.get_size()[0]//2) in\
						posled(boss.get_collision()[1]):
							
							lesson()
			
			if event.type == KEYUP:
				
				if event.key == K_SPACE: game_exit()
				if event.key == K_TAB: gamer.stealth(1); flag += 1
		
		# меняем карту
		for ex in media.school_map[mapp]['exit']:
			
			if (gamer.get_pos()[0] in \
			range(media.school_map[mapp]['exit'][ex]['col_x'][0], 
				  media.school_map[mapp]['exit'][ex]['col_x'][1]+1) or\
				(gamer.get_pos()[0]+gamer.get_size()[0] in \
			range(media.school_map[mapp]['exit'][ex]['col_x'][0], 
				  media.school_map[mapp]['exit'][ex]['col_x'][1]+1))) \
			   and\
			   (gamer.get_pos()[1] in \
			range(media.school_map[mapp]['exit'][ex]['col_y'][0], 
				  media.school_map[mapp]['exit'][ex]['col_y'][1]+1) or\
				(gamer.get_pos()[1]+gamer.get_size()[1] in \
			range(media.school_map[mapp]['exit'][ex]['col_y'][0], 
				  media.school_map[mapp]['exit'][ex]['col_y'][1]+1))):
			
				gamer.player_replace(media.school_map[mapp]['exit'][ex]['spawn'])
				   
				mapp = ex
				env = media.school_map[mapp]['obj']
					   
				NPCs = []
				[NPCs.append(phys.Mob(d)) for d in media.school_map[mapp]['NPC']]
				
				teacher = phys.Teacher(media.school_map[mapp]['teacher'])
				boss = phys.Boss(media.school_map[mapp]['boss'])
				
				break
		
		
		c = 0 # социальный стелс как в ассасине (кустов нет)
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
		
		# прорисовка элементов			
		(media.screen).blit(env, (0, 0)) # прорисовка мира
		[npc.draw() for npc in NPCs] #  прорисовка нпс
		if boss.get_be(): boss.draw() # прорисовка босса
		gamer.draw() # прорисовка игрового перса
		
		# отдельная прорисовка учителя
		if teacher.get_be():
			if teacher.search(gamer.get_pos(), 
					  gamer.get_size(), 
					  gamer.get_model()//2) == 1:
				
				x, y = teacher.vector(gamer.get_pos())
				teacher.walk(x, y)	
			else: teacher.teachers_path()
			teacher.draw()

		# избиение учеников в прямом эфире
		if teacher.get_be():
			
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
	
	game('road')
	# надеюсь код читать никто не будет
	# иначе придется потом это чистить