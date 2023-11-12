#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import media

import pygame as pg
from random import randint

def ceil(a):
	
	
	n = int(a)
	if a >= 0:
		if n >= a: return n
		else : return n+1
		
	else: 
		
		if n <= a: return n
		else : return n-1
		
def around(main_pos, round_pos, main_size, round_size, step):

	if main_pos[0]+(main_size[0]//2) in \
		range(round_pos[0]-step, round_pos[0]+round_size[0]+step) \
			   and\
	   main_pos[1]+(main_size[1]//4) in \
		range(round_pos[1]-step, round_pos[1]+round_size[1]+step):
				
			return 1
		
	return 0
		
class Mob():
	
	def __init__(self, 
			     position = [0, 0], 
			     model = randint(0, 1)):
		
		self.position = position
		
		self.role = 'npc'
		self.model = model
		
		self.size = media.mob[self.role]['size']
		
	def get_pos(self): return self.position
	def get_size(self): return self.size
	def get_model(self): return self.model
	
	def draw(self):
		
		(media.screen).blit(
			media.mob[self.role]['obj'][self.model], 
			self.position
		)
		
	def check(self, a, xy, mapp):
		
		ly, lx = \
		self.size[1], self.size[0]
		
		if a == 0: return 0
		
		if xy == 0:
			
			if a > 0 and self.model in (1, 3): self.model -= 1
			if a < 0 and self.model in (0, 2): self.model += 1
			
			if self.position[0]+a+lx > 1600:
				return 0
			
			if self.position[0]+a < 0: return 0
				
			for collision in media.school_map[mapp]['collisions']:
				
				if collision['col_y'][0] > self.position[1]+ly: continue
				if collision['col_y'][1] < self.position[1]: continue

				x1, x2 = collision['col_x']
					
				if self.position[0]+a in range(x1, x2+1) or \
				self.position[0]+a+lx in range(x1, x2+1):
					
					return 0
				
		if xy == 1:
			
			if self.position[1]+a+ly > 900:
				return 0
			
			if self.position[1]+a < 0: return 0
			
			for collision in media.school_map[mapp]['collisions']:
				
				if collision['col_x'][0] > self.position[0]+lx: continue
				if collision['col_x'][1] < self.position[0]: continue

				y1, y2 = collision['col_y']
					
				if self.position[1]+a in range(y1, y2+1) or \
				self.position[1]+a+ly in range(y1, y2+1):
					
					return 0
			
		return 1
		
	def walk(self, x = 0, y = 0, mapp = 'road'):
		
		if x != 0:
			
			if   self.check(x, 0, mapp): self.position[0] += x
			
			elif self.check(x//(abs(x)), 0, mapp): 
				self.position[0] += x//(abs(x))
			
		if y != 0:
			
			if   self.check(y, 1, mapp): self.position[1] += y
			
			elif self.check(y//(abs(y)), 1, mapp): 
				self.position[1] += y//(abs(y))
		
class Teacher(Mob):
	
	def __init__(self,  
				 name = 'teacher'):
		
		self.role = 'teacher'
		self.model = media.mob[self.role]['names'][name]
		self.size = media.mob[self.role]['size']
		
		self.path = media.mob[self.role]['path'][name]
		self.point = 0
		self.position = self.path[0]
		
	def vector(self, pos):
		
		step = 5
		
		if pos[0]-self.position[0] > 0: x = step
		elif self.position[0]-pos[0] == 0: x = 0
		else: x = -1*step
		
		if pos[1]-self.position[1] > 0: y = step
		elif self.position[1]-pos[1] == 0: y = 0
		else: y = -1*step
		
		return x, y	
		
	def teachers_path(self):
		
		if self.position[0] in\
		range(self.path[self.point][0]-10, self.path[self.point][0]+10) and\
		self.position[1] in\
		range(self.path[self.point][1]-10, self.path[self.point][1]+10): 
			
			self.point += 1
		
		if self.point >= len(self.path): self.point = 0
		
		x, y = self.vector(self.path[self.point])
		self.walk(x, y)
		
	def search(self, 
			   pos,
			   size,
			   visib):
		
		if visib == 1: return 0
		
		if pos[0]+(size[0]//2) in \
		range(self.position[0]-200, self.position[0]+self.size[0]+200) \
			   and\
		   pos[1]+(size[1]//4) in \
		range(self.position[1]-200, self.position[1]+self.size[1]+200):
				
			return 1
		
		return 0
		
class Player(Mob):
	
	def __init__(self, position = [0, 0]):
		
		self.position = position
		self.role = 'player'
		self.model = 0
		self.size = media.mob[self.role]['size']

		self.health = 100

	def stealth(self, a):
		
		if self.model >= 2: 
			if a == 0:
				self.model -= 2
		else: 
			if a == 1:
				self.model += 2
				
	def heat(self, hit = 10): self.health -= hit
	def heal(self): self.health += 10
	
	def get_health(self): return self.health
	
	def player_replace(self, new_pos): self.position = new_pos