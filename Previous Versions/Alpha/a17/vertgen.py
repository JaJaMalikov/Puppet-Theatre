import json

#min 1
scale = 3
step = 1

verts = []
coords = []

x = -scale
y = -scale

verts.append([0.0,0.0,0.0])
coords.append([.5,.5])

while x != scale:
	verts.append([x/scale,y/scale,0.0])
	coords.append([ (x+scale)/(scale+scale),(y+scale)/(scale+scale) ])
	x += step
	print(x)

while y != scale:
	verts.append([x/scale,y/scale,0.0])
	coords.append([ (x+scale)/(scale+scale),(y+scale)/(scale+scale) ])
	y += step

while x > -scale:
	verts.append([x/scale,y/scale,0.0])
	coords.append([ (x+scale)/(scale+scale),(y+scale)/(scale+scale) ])
	x -= step

while y > -scale-1:
	verts.append([x/scale,y/scale,0.0])
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
