loc = 64
data = {}

"""
the data structure of the currently selected animation; dictionary
keys:
"Object List" - dict, "Object name":dict - "Images":[list]
"Background Color", tuple, normalized RGBA values for the background color
"Current Frame" - int, currently rendered frame
"Current Object" - string, currently selected object, corrisponds to a key from "Object List"
"Render Dir" - string, current directory to save frames to
"Video Name" - string, location and name of the output video file
"Image List" - (formerly 'imgs') list, image names, added to list when new image is created, used to load all images from .ani file
"FPS" - int, frames per second of the current animation
"Audio" - string, path of the current audio file
"Frames" - list, 0-n, each frame is a dict; "Object name":{"state":value}
				"Current Image" - string, image name, is the one that is 
				"Pos" - tuple, x,y,z values controling the position of the object in 3D space
				"ScaleX" - float, controls the reletive scale of the objects width
				"ScaleY" - float, controls the relative scale of the object's height
				"Angle" - int, controls the angle in degrees of the object, point of origin is bottom center of object
				"FlipX" - float,(1.0 or -1.0) multiplied by the ScaleX to result in a flip on the horizontal axis if negative
				"FlipY" - float, (1.0, or -1.0) multiplied by the ScaleY to result in a flip on the vertical axis if positive
				"Keyframes" - list, if state is listed marks current frame as keyframe for the state
				"Aspect" - bool, if true the aspect ratio of the selected object is maintained
"""

data["Object List"] = {"Camera":{"Images":["Camera"],"Parent":None, "Children":[]}}
data["Background Color"] = [0.0,0.0,0.0,0.0]
data["Current Frame"] = 0

"""
free objects
if object is made child it is removed from free object list
	and added to the children of a free object
free objects are selected from a list 
object list draw order must be calculated for every frame
draw order calc must be done 
"""
data["Current Object"] = "Camera"
data["Render Dir"] = ""
data["Video Name"] = ""
data["Image List"] = []
data["FPS"] = 24
data["Audio"] = ""
data["Frames"] = []
data["Frames"].append(
		{
		"Camera":{
			"Current Image": "Camera",
			"Pos":[0.0,0.0,0.0],
			"Dist":0.0,
			"ScaleX":1,
			"ScaleY":1,
			"Angle":0,
			"FlipX":1.0,
			"FlipY":1.0,
			"Keyframes":[],
			"Aspect":False,
			"Parent":None
			}
		}
	)

default = {
	"Current Image": "none",
	"Pos":[0.0,0.0,0.0],
	"Dist":0.0,
	"ScaleX":1,
	"ScaleY":1,
	"Angle":0,
	"FlipX":1.0,
	"FlipY":1.0,
	"Keyframes":[],
	"Aspect":False,
	"Parent":None
}