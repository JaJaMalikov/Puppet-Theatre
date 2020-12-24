#!/usr/bin/env python3

#automatic character creator and body compositor

import random
import pygame
import sys
import os

character = sys.argv[1]

#mkdir()
#listdir()

body = pygame.image.load(os.path.join(character, "body.png" ))
head = pygame.image.load(os.path.join(character,  "head.png" ))
hair = pygame.image.load(os.path.join(character,  "hair.png" ))

mooddirs = ["mouth",  "eyebrows", "pupils"]
mouth_dic = {}
eyebrow_dic = {}
pupil_dic = {}

mouth_states = os.listdir(os.path.join(character,"mouth"))
print(mouth_states)
for state in mouth_states:
	img_list = {}
	for img in os.listdir(os.path.join(character,"mouth",state)):
		print(os.path.join(character,"mouth",state,img))
		img_list[img] = pygame.image.load(os.path.join(character,"mouth",state,img))
	mouth_dic[state] = img_list

eyebrow_states = os.listdir(os.path.join(character,"eyebrows"))
for state in eyebrow_states:
	eyebrow_dic[state.split(".")[0]] = pygame.image.load(os.path.join(character,"eyebrows",state))
	print(state)

pupil_states = os.listdir(os.path.join(character,"pupils"))
for state in pupil_states:
	pupil_dic[state.split(".")[0]] = pygame.image.load(os.path.join(character,"pupils",state))
	print(state)

print(mouth_dic.keys())
print(eyebrow_dic.keys())
print(pupil_dic.keys())

fin = character+"_fin"
os.mkdir(fin)
for m_key in mouth_dic.keys():
	cur_m_fin = os.path.join(fin,m_key)
	os.mkdir(cur_m_fin)
	for e_key in eyebrow_dic.keys():
		cur_e_fin = os.path.join(cur_m_fin, e_key)
		os.mkdir(cur_e_fin)
		for p_key in pupil_dic.keys():
			cur_p_fin = os.path.join(cur_e_fin, p_key)
			os.mkdir(cur_p_fin)
			s_dir = os.path.join(cur_p_fin, "down")
			os.mkdir(s_dir)
			print(mouth_dic[m_key].keys())

			for mouth in mouth_dic[m_key].keys():
				body = pygame.image.load(os.path.join(character, "body.png" ))
				head = pygame.image.load(os.path.join(character,  "head.png" ))
				hair = pygame.image.load(os.path.join(character,  "hair.png" ))

				head.blit(mouth_dic[m_key][mouth],(0,0))
				head.blit(pupil_dic[p_key], (0,0))
				head.blit(eyebrow_dic[e_key], (0,0))
				head.blit(hair, (0,0))

				body.blit(pygame.transform.rotozoom(head, random.randrange(-5,5), 1), (75,0))
				pygame.image.save(body, os.path.join(s_dir, mouth ))

#head.blit(hair,(0,0))
#body.blit(head,(75,0))

#pygame.image.save(body, "test.png")