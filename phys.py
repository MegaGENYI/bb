#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import media

import pygame as pg
from random import randint

class Mob():
	
	def __init__(self, position = [0, 0]):
		
		self.position = position
		
		self.model = 1
		
	def pos(self): return self.position
	
	def draw(self):
		
		(media.screen).blit(
			media.player['obj'][self.model], 
			self.position
		)
		
class Player(Mob):
	
	def __init__(self, position = [0, 0]):
		
		self.position = position
		self.model = 0
		
	def check(self, a, xy, mapp):
		
		ly, lx = media.player['size'][1], media.player['size'][0]
		
		if a == 0: return 0
		
		if xy == 0:
			
			if a > 0: self.model = 0
			if a < 0: self.model = 1
			
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
			elif self.check(x//(abs(x)), 0, mapp): self.position[0] += 1
			
		if y != 0:
			if   self.check(y, 1, mapp): self.position[1] += y
			elif self.check(y//(abs(y)), 1, mapp): self.position[1] += 1