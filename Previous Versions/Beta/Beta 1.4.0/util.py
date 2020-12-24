import json
import sys

keyword = sys.argv[1]

loc = 96

if keyword == "vertgen":
	#min 1
	scale = 1
	step = 1

	verts = []
	coords = []

	x = -scale
	y = -scale

	while x != scale:
		verts.append([x/scale,y/scale + 1,0.0])
		coords.append([ (x+scale)/(scale+scale),(y+scale)/(scale+scale) ])
		x += step
		print(x)

	while y != scale:
		verts.append([x/scale,y/scale + 1,0.0])
		coords.append([ (x+scale)/(scale+scale),(y+scale)/(scale+scale) ])
		y += step

	while x > -scale:
		verts.append([x/scale,y/scale + 1,0.0])
		coords.append([ (x+scale)/(scale+scale),(y+scale)/(scale+scale) ])
		x -= step

	while y > -scale-1:
		verts.append([x/scale,y/scale + 1,0.0])
		coords.append([ (x+scale)/(scale+scale),(y+scale)/(scale+scale) ])
		y -= step

	"""
	for x in range(-scale,scale + 1):
		for y in range(-scale,scale+1):
			if x == -scale or x == scale or y == -scale or y == scale:
				verts.append([x/scale,y/scale,0.0])
				coords.append([ (x+scale)/(scale+scale),(y+scale)/(scale+scale) ])
				#coords.append([(x/scale+ 1 )/2,(y/scale+(scale/10))/2])
				#print(x/10)
				#print((x/10+1)/2 )"""

	edges = []
	for x in range(len(verts)-1):
		edges.append([x,x+1])
	edges.append([x+1,0])

	verts_text = "verts = " + json.dumps(verts)
	coords_text = "coords = " + json.dumps(coords)
	edges_text = "edges = " + json.dumps(edges)

	final = "\n".join([verts_text, coords_text, edges_text])

	page = open("verts.py","w")
	page.write(final)
	page.close()

elif keyword == "count":
	import main
	import canvas_base
	import data_default
	import image_list
	import listener
	import OBJ2D
	import object_ctrl
	import object_list
	import pygame_panel
	import render_ctrl
	import render_frames_dialog
	import render_video_dialog
	import sampler
	import timeline_ctrl

	loc += main.loc
	loc += canvas_base.loc
	loc += data_default.loc
	loc += image_list.loc
	loc += listener.loc
	loc += OBJ2D.loc
	loc += object_ctrl.loc
	loc += object_list.loc
	loc += pygame_panel.loc
	loc += render_ctrl.loc
	loc += render_frames_dialog.loc
	loc += render_video_dialog.loc
	loc += sampler.loc
	loc += timeline_ctrl.loc

	print(loc)