#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame as pg

screen = \
pg.display.set_mode((1600, 900), 0, 32)

'''
Егорище, такое тз
Ты кароч рисуешь карту в стиле undertale
Кусками, разрешение 1600x900
Затем в этом файле создаешь новый элемент словаря
Дальше будет образец
Заполняешь по инструкции из образца
Понял? ПОНЯЛ? чо не отвечаешь?
'''

# следи за запятыми

'''
Образец:
	# имя локации
	'': {
		
		'path': './media/map/', # дописываешь название файла
		'exit': {
			# имя локации, куда переходит игрок
			'': {
				'col_x': (), # точка перехода на другую локацию
				'col_y': ()
				 }
			
			},      
									   # здесь ставишь имя локации
		'obj': pg.image.load(school_map['']['path']).convert(),
			
		'collisions': [   # здесь массив с коллизиями объектов и стен
			
			{             # блок с отдельным объектом
			 'col_x': (), # коллизия по горизонтали
			 'col_y': ()  # коллизия по вертикали
			 },
			
		]
	
	}

'''

school_map = {

	'road': {

		'obj': pg.image.load('./media/map/road.png').convert(),		

		'exit': {
			
				'hall': {
					 'col_x': (0),
					 'col_y': (0)
					 }
				
			},
		
		'collisions': [

				{
				 'col_x': (0, 200),
				 'col_y': (450, 900)
				 }, 
				
				{
				 'col_x': (1400, 1600),
				 'col_y': (450, 900)
				 }

			]
		
		},
	
	'hall': {
		
		'path': './media/map/',
		'exit': {
			
				'long_corridor_d': {
					'col_x': (),
					'col_y': ()
					}
					
			},
			
		'obj': 0, # pg.image.load(school_map['hall']['path']).convert(),
			
		'collisions': [
			
			{
			 'col_x': (),
			 'col_y': ()
			 }
			
		]
	
	}

}

# У Андрея все попроще

mob = {
	
	'npc': {   
	   
		'obj': 
			[
			pg.image.load('./media/mob/npc/l1.png').convert_alpha(),
			pg.image.load('./media/mob/npc/r1.png').convert_alpha()
			], 
		   
		'size': (117, 200) 
		   
	},

	'player': {
	
		'obj': [                             # тут поменяешь названия
			pg.image.load('./media/mob/player/andrey_right.png').convert_alpha(),
			pg.image.load('./media/mob/player/andrey_left.png').convert_alpha()
		],
	
		'size': (117, 200)
	
	}

}
