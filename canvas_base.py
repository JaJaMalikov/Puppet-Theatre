#Graphical Libraries
import wx
from wx import glcanvas
from OpenGL.GL import *
from OpenGL.GLU import *


#other built-in libraries

#designated constants for program-wide use
from consts import *

loc = 74

class CanvasBase(glcanvas.GLCanvas):
	"""
	basis for the canvas object in the render control panel
	currently uses the fixe function pipeline, will be updated to modern opengl
	3.3+ in Beta 2
	"""
	def __init__(self, parent, ViewPortSize, data):
		glcanvas.GLCanvas.__init__(self, parent, -1, size=(ViewPortSize))
		self.init = False
		self.context = glcanvas.GLContext(self)
		self.data = data
		self.resized = True
		self.box_width = 1
		self.box_height = 1
		self.ViewPortSize = ViewPortSize
		self.resolution = [1,1]
		self.SetCurrent(self.context)
		self.distance = 50.0
		self.view_angle = 45

		#self.data["Background Color"] is a 4 float list of RGBA values
		#using the * before unpacks it because clear color takes 4 inputs
		glClearColor(*self.data["Background Color"])
		self.Bind(wx.EVT_SIZE, self.OnResize)
		glEnable(GL_BLEND)
		#glEnable(GL_DEPTH_TEST)
		#glDepthFunc(GL_LESS)
		#glAlphaFunc(GL_GREATER, 0.5)
		#glEnable(GL_ALPHA_TEST)

	def set_distance(self, dist):
		self.distance = dist

	def set_view_angle(self, angle):
		self.view_angle = angle

	def set_resolution(self, size):
		self.resolution = size

	def prepTexture(self, texture):
		glBindTexture(GL_TEXTURE_2D, texture)

		self.begin()
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glEnable(GL_BLEND)

	def loadTexture(self, textureData, width, height):
		glEnable(GL_TEXTURE_2D)
		texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, texture)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height,
					0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

		glGenerateMipmap(GL_TEXTURE_2D)
		return texture

	def drawTexture(self, verts, coords):
		glBegin(GL_POLYGON)

		for x in range(len(verts)):
			glTexCoord2f(*coords[x])
			glVertex3f(*verts[x])

		glEnd()
		glDisable(GL_BLEND)
		self.end()

	def draw_cam(self, texture, verts, coords):
		#glDisable(GL_DEPTH_TEST )

		glBindTexture(GL_TEXTURE_2D, texture)
		glPushMatrix()
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

		self.Purge(self.ViewPortSize)

		glTranslatef(0.0 , -self.box_height ,0.0)
		glScalef(self.box_width ,self.box_height , 1.0)


		glBegin(GL_POLYGON)

		for x in range(len(verts)):
			glTexCoord2f(*coords[x])
			glVertex3f(*verts[x])

		glEnd()
		glDisable(GL_BLEND)

		glColor4f(1.0,1.0,1.0,1.0)
		glPopMatrix()
		#glEnable(GL_DEPTH_TEST)
		#glDepthFunc(GL_LESS)
		#glAlphaFunc(GL_GREATER, 0.5)
		#glEnable(GL_ALPHA_TEST)

	def draw_wire(self, inData, texture, verts, edges, coords ):
		"""
		wire drawing for possible debug mode
		"""
		glBindTexture(GL_TEXTURE_2D, 0)
		glColor4f(0.0,1.0,0.0,1.0)

		glPushMatrix()

		self.transform(inDate, None)

		#glTranslatef(inData["Pos"][0], inData["Pos"][1], inData["Pos"][2] )
		#glRotatef(inData["Angle"], 0, 0, 1)
		#glScalef(inData["FlipX"] * inData["ScaleX"], inData["FlipY"] * inData["ScaleY"], 1.0)

		glBegin(GL_LINES)

		for Edge in edges:
			for Vertex in Edge:
				glVertex3fv(verts[Vertex])

		glEnd()
		glPopMatrix()
		glColor4f(1.0,1.0,1.0,1.0)

	def draw_origin(self, inData, texture, verts, edges ):
		"""
		wire drawing for possible debug mode
		"""
		glBindTexture(GL_TEXTURE_2D, 0)
		glColor4f(0.0,1.0,0.0,1.0)

		glPushMatrix()

		glTranslatef(inData["Pos"][0], inData["Pos"][1], inData["Pos"][2] )
		glRotatef(inData["Angle"], 0, 0, 1)
		glScalef(inData["FlipX"] * inData["ScaleX"], inData["FlipY"] * inData["ScaleY"], 1.0)

		glBegin(GL_LINES)

		glVertex3f(0.1 , 0.1, 0.1)
		glVertex3f(-0.1 , -0.1, 0.1)

		glVertex3f(0.1 , -0.1, 0.1)
		glVertex3f(-0.1 , 0.1, 0.1)

		glEnd()
		glPopMatrix()
		glColor4f(1.0,1.0,1.0,1.0)


	def begin(self):
		glPushMatrix()

	def end(self):
		glPopMatrix()

	def GetImgData(self, offset):
		return glReadPixels(offset[0],offset[1],self.resolution[0], self.resolution[1], GL_RGBA, GL_UNSIGNED_BYTE)

	def FrameBufferOn(self):
		glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)

	def FrameBufferOff(self):
		glBindFramebuffer(GL_FRAMEBUFFER, 0)

	def translate(self, x, y, z):
		glTranslatef(x,y,z)

	def transformFlat(self, cam, child):
		#sets the canvas to the camera on the current frame's pos, scale, rot
		#giving the user full control over the camera from frame to frame

		glTranslatef(cam["Pos"][0],
					cam["Pos"][1],
					0.0 )

		glRotatef(cam["Angle"], 0, 0, 1)

		glTranslatef(cam["Origin"][0],
					cam["Origin"][1],
					0.0)

		glScalef(cam["FlipX"] * cam["ScaleX"],
				cam["FlipY"] * cam["ScaleY"], 1.0)

	def transform(self, cam, parent =False):
		#sets the canvas to the camera on the current frame's pos, scale, rot
		#giving the user full control over the camera from frame to frame

		if not parent:
			glTranslatef(cam["Pos"][0],
						cam["Pos"][1],
						cam["Pos"][2])

			glRotatef(cam["Angle"], 0, 0, 1)

			glTranslatef(cam["Origin"][0],
						cam["Origin"][1],
						0.0)

			glScalef(cam["FlipX"] * cam["ScaleX"],
					cam["FlipY"] * cam["ScaleY"], 1.0)
		else:
			glTranslatef(cam["Pos"][0],
						cam["Pos"][1],
						0.0)

			glRotatef(cam["Angle"], 0, 0, 1)

			glTranslatef(cam["Origin"][0],
						cam["Origin"][1],
						0.0)

			glScalef(cam["FlipX"] * cam["ScaleX"],
					cam["FlipY"] * cam["ScaleY"], 1.0)

	def transformStraight(self, cam, child):
		#sets the canvas to the camera on the current frame's pos, scale, rot
		#giving the user full control over the camera from frame to frame

		glTranslatef(cam["Pos"][0],
					cam["Pos"][1],
					cam["Pos"][2])

		glRotatef(cam["Angle"], 0, 0, 1)

		glScalef(cam["FlipX"] * cam["ScaleX"],
				cam["FlipY"] * cam["ScaleY"], 1.0)

	def draw_box(self):
		#print(self.box_width, self.box_height)
		#glDisable(GL_DEPTH_TEST )

		glBindTexture(GL_TEXTURE_2D, 0)
		glPushMatrix()
		glLineWidth(4)
		glColor4f(0.0,1.0,0.0,1.0)

		self.Purge(self.ViewPortSize)

		glBegin(GL_LINE_LOOP)

		glVertex3f(-self.box_width, 
			self.box_height, 0.0)
		glVertex3f(self.box_width, 
			self.box_height, 0.0)
		glVertex3f(self.box_width, 
			-self.box_height, 0.0)
		glVertex3f(-self.box_width, 
			-self.box_height, 0.0)

		glEnd()

		glLineWidth(2)
		glColor4f(1.0,0.0,1.0,1.0)
		glBegin(GL_LINE_LOOP)

		glVertex3f(-self.box_width, 
			self.box_height, 0.0)
		glVertex3f(self.box_width, 
			self.box_height, 0.0)
		glVertex3f(self.box_width, 
			-self.box_height, 0.0)
		glVertex3f(-self.box_width, 
			-self.box_height, 0.0)


		glEnd()

		glColor4f(1.0,1.0,1.0,1.0)
		glPopMatrix()
		#glEnable(GL_DEPTH_TEST)
		#glDepthFunc(GL_LESS)
		#glAlphaFunc(GL_GREATER, 0.5)
		#glEnable(GL_ALPHA_TEST)

	def gen_fbo(self, px_width, px_height):
		plane_texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, plane_texture)

		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, px_width, px_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
		glBindTexture(GL_TEXTURE_2D, 0)

		self.FBO = glGenFramebuffers(1)
		glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)
		glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, plane_texture, 0)

		plane_buffer = glGenRenderbuffers(1)
		glBindRenderbuffer(GL_RENDERBUFFER, plane_buffer)
		glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, px_width, px_height)
		glBindRenderbuffer(GL_RENDERBUFFER, 0)

		glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, plane_buffer)

		#glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, px_width, px_height, 0,GL_DEPTH_COMPONENT, GL_UNSIGNED_INT, None)
		#glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_TEXTURE_2D, plane_texture, 0)


		glBindFramebuffer(GL_FRAMEBUFFER, 0)

	def is_resized(self):
		resized = self.resized
		self.resized = False
		return resized

	def set_data(self, data):
		#loads the current project data in order to get the background color
		self.data = data

	def Purge(self, size):
		if 0 in size:
			print("size 0")
			size = [1,1]
		#resets the convas identity, perspective, and position
		glViewport(0,0, size[0], size[1])
		glLoadIdentity()
		gluPerspective(self.view_angle, (size[0]/ size[1]), 0.1, self.distance)
		glTranslatef(0.0,0.0,-10)
		#glEnable(GL_DEPTH_TEST)
		#glDepthFunc(GL_LEQUAL)

	def clear(self):
		#clears the canvas with the color set in self.data["Background Color"]
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

	def OnResize(self, event):
		#sets the viewportsize and readjusts the glViewport to match
		#purges the canvas to match
		size = self.GetClientSize()
		self.ViewPortSize = size
		glViewport(0, 0, size.width, size.height)
		self.Purge(self.ViewPortSize)
		self.resized = True

	def set_bg(self, color):
		#self.data["Background Color"] = color
		
		glClearColor(*color)

	def Update(self):


		#only purges at the moment but future proofing in case updates should do more later
		self.Purge(self.ViewPortSize)

	def Draw(self):
		self.SwapBuffers()
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
