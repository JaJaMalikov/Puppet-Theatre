#Graphical Libraries
import wx

#other built-in libraries

#vertex default values
import verts

#container class for 2D object texture
from OBJ2D import OBJ2D

loc = 240

class ImageList(wx.Panel ):
	"""
	displays list of current objects images
	allows to create/delete images, select current image with double-click
	"""
	def __init__(self, parent, ID, data, window, frame, Image_list):
		wx.ListBox.__init__(self, parent, ID)
		self.Image_list = Image_list
		self.parent = parent
		self.data = data
		self.window = window
		self.frame = frame
		self.build()
		self.set_layout()
		self.bind_all()

	def create_menus(self):
		self.imgMenu = wx.Menu()

		self.newMultiImg = wx.MenuItem(self.imgMenu, wx.ID_ANY, "&Load Images\tCtrl+I", "Load Images")
		self.delImg = wx.MenuItem(self.imgMenu, wx.ID_ANY, "&Delete Image\tCtrl+J", "Delete Image")
		self.moveImgUp = wx.MenuItem(self.imgMenu, wx.ID_ANY, "&Move Up\tCtrl+G", "Move Image Up")
		self.moveImgDown = wx.MenuItem(self.imgMenu, wx.ID_ANY, "&Move Down\tCtrl+H", "Move Image Down")

		self.imgMenu.Append(self.newMultiImg)
		self.imgMenu.Append(self.delImg)
		self.imgMenu.Append(self.moveImgUp)
		self.imgMenu.Append(self.moveImgDown)

		self.window.menubar.Append(self.imgMenu, "&Images")

		#image loading dialog set in menu
		self.window.Bind(wx.EVT_MENU, self.NewMultiImg , self.newMultiImg)
		self.window.Bind(wx.EVT_MENU, self.removeImg, self.delImg)
		self.window.Bind(wx.EVT_MENU, self.move_up, self.moveImgUp)
		self.window.Bind(wx.EVT_MENU, self.move_down, self.moveImgDown)

	def bind_all(self):
		self.load_btn.Bind(wx.EVT_BUTTON, self.NewMultiImg)
		self.delete_btn.Bind(wx.EVT_BUTTON, self.removeImg)
		self.up_btn.Bind(wx.EVT_BUTTON, self.move_up)
		self.down_btn.Bind(wx.EVT_BUTTON, self.move_down)

		self.overwrite_next.Bind(wx.EVT_BUTTON, self.On_overwrite_next)
		self.overwrite_last.Bind(wx.EVT_BUTTON, self.On_overwrite_last)

		self.overwrite_all.Bind(wx.EVT_BUTTON, self.On_overwrite_all)

		self.overwrite_past.Bind(wx.EVT_BUTTON, self.On_overwrite_past)
		self.overwrite_future.Bind(wx.EVT_BUTTON, self.On_overwrite_future)

	def set_layout(self):
		self.buttonSizer = wx.BoxSizer(wx.VERTICAL)
		self.pageSizer = wx.BoxSizer(wx.VERTICAL)

		self.t_b_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.b_b_sizer = wx.BoxSizer(wx.HORIZONTAL)

		self.t_b_sizer.Add(self.load_btn)
		self.t_b_sizer.Add(self.delete_btn)
		self.b_b_sizer.Add(self.up_btn)
		self.b_b_sizer.Add(self.down_btn)
		self.buttonSizer.Add(self.t_b_sizer)
		self.buttonSizer.Add(self.b_b_sizer)

		self.pageSizer.Add(self.buttonSizer, 0)
		self.pageSizer.Add(self.imgList, -1, wx.EXPAND)

		self.pageSizer.Add(self.overwrite_panel, 0)

		self.SetSizer(self.pageSizer)


	def build(self):
		#loads image(s)
		self.load_btn = wx.Button(self, 1, "Load")
		#deleted image
		self.delete_btn = wx.Button(self, 1, "Delete")
		#moves image up in list, future proof against image cycling
		self.up_btn = wx.Button(self, 1, "Raise")
		#moves image down in list, future proof against image cycling
		self.down_btn = wx.Button(self, 1, "Lower")

		self.imgList = wx.ListBox(self, wx.ID_ANY, style=wx.LB_HSCROLL)

		#holds buttons which are used to overwrite which image is selected
		self.overwrite_panel = wx.Panel(self, size=(167, 90))

		self.overwrite_label = wx.StaticText(self.overwrite_panel, label="Overwrite:", pos=(0,25))
		self.overwrite_all = wx.Button(self.overwrite_panel, label="All", pos=(85, 22))

		self.overwrite_last = wx.Button(self.overwrite_panel, label="Previous", pos=(0, 44))
		self.overwrite_next = wx.Button(self.overwrite_panel, label="Next", pos=(85, 44))

		self.overwrite_future = wx.Button(self.overwrite_panel, label="Subsequent", pos=(0,66))
		self.overwrite_past = wx.Button(self.overwrite_panel, label="Preceeding", pos=(85,66))


	def On_overwrite_future(self, event):
		#overwrites all future images with currently select image
		box = wx.MessageDialog(None, 'Are you sure you want to overwrite all subsequent frames?',
			"Overwrite all future frames", wx.OK | wx.CANCEL | wx.ICON_WARNING)
		if box.ShowModal() == wx.ID_OK:
			ref = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Current Image"]
			for frame in range( self.data["Current Frame"], len(self.data["Frames"])):
				self.data["Frames"][frame][self.data["Current Object"]]["Current Image"] = ref
			self.window.PushHistory()

	def On_overwrite_past(self, event):
		#overwrites all previous images with currently selected image
		box = wx.MessageDialog(None, 'Are you sure you want to overwrite all previous frames?',
			"Overwrite all previous frames", wx.OK | wx.CANCEL | wx.ICON_WARNING)
		if box.ShowModal() == wx.ID_OK:
			ref = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Current Image"]
			for frame in range(0, self.data["Current Frame"]):
				self.data["Frames"][frame][self.data["Current Object"]]["Current Image"] = ref
			self.window.PushHistory()

	def On_overwrite_all(self, event):
		#overwrites all frames with currently selected image
		box = wx.MessageDialog(None, 'Are you sure you want to overwrite all frames?',
			"Overwrite all frames", wx.OK | wx.CANCEL | wx.ICON_WARNING)
		if box.ShowModal() == wx.ID_OK:
			ref = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Current Image"]
			for frame in range(len(self.data["Frames"])):
				self.data["Frames"][frame][self.data["Current Object"]]["Current Image"] = ref
			self.window.PushHistory()

	def On_overwrite_last(self, event):
		#overwrites previous frame with currently selected image

		ref = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Current Image"]
		self.data["Frames"][self.data["Current Frame"]-1][self.data["Current Object"]]["Current Image"] = ref
		self.window.timelineCtrl.onBack(1)
		self.window.PushHistory()

	def On_overwrite_next(self, event):
		#overwrites next frame with currently selected image
		ref = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Current Image"]
		self.data["Frames"][self.data["Current Frame"]+1][self.data["Current Object"]]["Current Image"] = ref
		self.window.timelineCtrl.onNext(1)
		self.window.PushHistory()

	def set_data(self, data):
		self.data = data

	def reload(self):
		#reloads all images from self.data
		for image in self.data["Image List"]:
			self.AddImg(image, False)
		self.set_list(self.data["Current Object"])

	def move_up(self, event):
		"""
		relocates the current image to a higher position on the list
		if the object is at the top of the list then it moves it to the end
		"""
		#gets currently selected image and position
		img = self.get_selection()
		pos = self.data["Object List"][self.data["Current Object"]]["Images"].index(img)

		#checks if position is already top of the list and circles it to the end if so
		if pos != 0:
			self.data["Object List"][self.data["Current Object"]]["Images"].remove(img)
			self.data["Object List"][self.data["Current Object"]]["Images"].insert(pos-1, img)
			new_pos = pos-1
		else:
			self.data["Object List"][self.data["Current Object"]]["Images"].remove(img)
			self.data["Object List"][self.data["Current Object"]]["Images"].append(img)
			new_pos = len(self.data["Object List"][self.data["Current Object"]]["Images"])-1

		#resets the list to view, highlights selected image
		self.set_list(self.data["Current Object"])
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Current Image"] = self.imgList.GetString(new_pos)
		self.imgList.SetSelection(new_pos)
		self.window.PushHistory()

	def move_down(self, event):
		"""
		relocates the current image to a higher position on the list
		if the object is at the top of the list then it moves it to the end
		"""
		#gets currently selected image and position
		img = self.get_selection()
		pos = self.data["Object List"][self.data["Current Object"]]["Images"].index(img)

		#checks if image is at the end and sets the image to the beginning if so
		if pos == len(self.data["Object List"][self.data["Current Object"]]["Images"])-1:
			new_pos = 0
		else:
			new_pos = pos+1

		self.data["Object List"][self.data["Current Object"]]["Images"].remove(img)
		self.data["Object List"][self.data["Current Object"]]["Images"].insert(new_pos , img)

		#resets the list to view, highlights selected image
		self.set_list(self.data["Current Object"])
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Current Image"] = self.imgList.GetString(new_pos )
		self.imgList.SetSelection(new_pos)
		self.window.PushHistory()

	def NewMultiImg(self, event):
		#loads a list of images to append to the object list
		with wx.FileDialog(self, "Import Files", wildcard="PNG files (*.png)|*.png",
							style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) as fileDialog:
			if (fileDialog.ShowModal() == wx.ID_CANCEL):
				return

			pathnames = fileDialog.GetPaths()

			for pathname in pathnames:
				#data image list is used to keep track of the paths of available images
				self.data["Image List"].append(pathname)
				self.AddImg(pathname, True)
			self.window.PushHistory()

	def AddImg(self, pathname, new):
		"""
		creates a new image and adds it to the Image_list dict
		Image_list uses a string:OBJ2D setup to draw the images
		"""
		#removes all but the file name and parent directory to identify it as img_tag
		img_num = pathname.count("\\")
		img_tag = pathname.split("\\", img_num-1)[-1]

		#creates a new OBJ2D from the path and adds it to the Image_List using the img_tag
		#only creates the OBJ2D if one doesn't exist
		#all objects using the same image will draw from the same OBJ2D
		if pathname not in self.Image_list.keys():
			self.Image_list[img_tag ] = OBJ2D(pathname, self.window)

		#new identifies the image as one not currently in the current object
		if new:
			self.data["Object List"][self.data["Current Object"]]["Images"].append(img_tag )

		#loads the image list and sets the first image as the current selection
		#then sets the status for the window
		self.set_current_list()
		if len(self.data["Object List"][self.data["Current Object"]]["Images"]) == 1:
			for x in range(len(self.data["Frames"])):
				self.data["Frames"][x][self.data["Current Object"]]["Current Image"] = self.get_first()
		self.frame.LoadStatus()

	def removeImg(self, event):
		#deletes an image from the current object, resets the list, sets the first image as current selection
		#does NOT delete OBJ2D from image_list in case another object is using it, also results in faster
		#load times when loading the image again
		self.data["Object List"][self.data["Current Object"]]["Images"].remove(self.get_selection())
		self.set_list(self.data["Current Object"])
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Current Image"] = self.get_first()
		self.window.PushHistory()

	def set_list(self, cur_obj):
		#sets the new object list 
		self.imgList.Set(self.data["Object List"][cur_obj]["Images"])

	def set_current_list(self):
		#sets the current image list
		self.imgList.Set(self.data["Object List"][self.data["Current Object"]]["Images"])
		if len(self.data["Object List"][self.data["Current Object"]]["Images"]) == 1:
			self.frame.LoadStatus()

	def get_selection(self):
		return self.imgList.GetString(self.imgList.GetSelection())

	def get_first(self):
		return self.imgList.GetString(0)
