#graphical libraries
import wx
import wx.media
from pygame.locals import *
import pygame

#other built in libraries
import copy
from datetime import datetime

#pygame rendering panel, designed to layout
from pygame_panel import PygamePanel
#proccesses the audio file sames to generate a waveform
import sampler
#constants to be used throughout the program
from consts import * 
#listens for key inputs, future proofing for key shortcuts
from listener import Key_listener
#internal data structure default implementation
import data_default

loc = 613

version_name = "Monchy PT Timeline Control Panel Beta 1.0.1"

class TimelineCtrl(wx.Panel):
	"""
	loads the audio and generates a wave form
	controls the current position in time, uses a slider to sync up the audio with the current frame
	allows switching between multiple framerates
	"""
	def __init__(self, parent, ID, data, window, ViewPortSize=(4000,50)):
		wx.Panel.__init__(self, parent, ID, style=wx.RAISED_BORDER)
		self.ViewPortSize = ViewPortSize
		self.window = window
		self.data = data
		self.wave_data = []
		self.song_length = 1
		self.song_frames = 1
		self.loaded = False
		self.timeset = False
		self.current_pos = 0
		self.time_counter = 0

		self.framerates =['1', '2', '3', '4', '6', '12', '24', '30', '60']

		self.create_objects()
		self.Set_FPS(1)

		self.waveform = pygame.Surface(self.ViewPortSize)
		self.waveform.fill((100,100,100))

		self.layout()
		self.SetSizer(self.mainBox)
		self.bind_all()

	def bind_all(self):
		self.next_btn.Bind(wx.EVT_BUTTON, self.onNext)
		self.back_btn.Bind(wx.EVT_BUTTON, self.onBack)
		self.play_btn.Bind(wx.EVT_BUTTON, self.onPlay)
		self.stop_btn.Bind(wx.EVT_BUTTON, self.onStop)
		self.pause_btn.Bind(wx.EVT_BUTTON, self.onPause)
		self.VolumeSlider.Bind(wx.EVT_SLIDER, self.onSetVolume)
		self.FPS_btn.Bind(wx.EVT_BUTTON, self.Set_FPS)
		self.PlaybackSlider.Bind(wx.EVT_SLIDER, self.onSliderScroll)


	def create_menus(self):
		"""
		create audio loading menu option in main menu
		"""
		self.loadAudio = wx.MenuItem(self.window.fileMenu, wx.ID_ANY, 
			'&Load Audio\tCtrl+A', 'Load Audio')
		self.window.fileMenu.Append(self.loadAudio)
		self.window.Bind(wx.EVT_MENU, self.LoadAudio, self.loadAudio)

	def onSetVolume(self, event):
		#wx's mediaCtrl sets volume on a scale of 0.0 - 1.0, so the slider's value has to be divided by 100
		self.mediaPlayer.SetVolume(self.VolumeSlider.GetValue() / 100)

	def onNext(self, event):
		#advances the current frame by 1, must use the seek function
		#simply adding to the current frame results in errors
		self.mediaPlayer.Seek(int(self.mediaPlayer.Tell() + self.ms_per_frame))

	def onBack(self, event):
		#advances the current frame by -1, must use the seek function
		#simply adding to the current frame results in errors
		self.mediaPlayer.Seek(int(self.mediaPlayer.Tell() - self.ms_per_frame))

	def isPlaying(self):
		return(self.mediaPlayer.GetState() == wx.media.MEDIASTATE_PLAYING)

	def onPlay(self, event):
		print("playing")
		"""
		mediaCtrl wont return a playlength until it's played for at least a tenth of a second
		sets the playbackslider range once playing
		sets the number of frames based on the length of the audio file
		"""
		if not self.mediaPlayer.Play():
			wx.MessageBox("Music not playing, check if it's loaded", "ERROR", wx.ICON_ERROR | wx.OK)

		else:
			self.mediaPlayer.SetInitialSize()
			self.GetSizer().Layout()

			self.song_length = self.mediaPlayer.Length()
			self.song_frames = int( self.song_length / self.ms_per_frame)
			self.PlaybackSlider.SetRange(0, self.song_frames)
			self.PlaybackSlider.SetSize((self.GetClientSize()[0], 20))

	def onPause(self, event):
		print("pausing")
		self.mediaPlayer.Pause()

	def onStop(self, event):
		"""
		resets the current frames after stopping
		must seek to 1ms to prevent "phantom frame" effect
		"""
		self.mediaPlayer.Stop()
		self.data["Current Frame"] = 0
		self.mediaPlayer.Seek(1)

	def onSliderScroll(self, event):
		"""
		seeks to the equavalent position in the audio using the position to equal the frame * ms_per_frame
		"""
		offset = self.PlaybackSlider.GetValue()
		self.mediaPlayer.Seek(int(offset * self.ms_per_frame))

	def set_data(self, data):
		#loads data and sets frames per second
		self.data = data
		self.Set_FPS(1)
		self.rates.SetValue(str(self.data["FPS"]))

	def create_objects(self):
		"""
		pygame panel is meant to be a directly interactable function to accept
		native pygame functions
		mediactrl is made non-visible in order to be used only for audio
		the slider should be replaced with a new version of the pygamepanel

		future design: clicking should snap indicator to the closest frame, should follow
				click and drag
		"""
		self.PP = PygamePanel(self, 1, self.ViewPortSize, self.window)
		self.mediaPlayer = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER)
		self.PlaybackSlider = wx.Slider(self, value=1, minValue=0,
			maxValue= self.ViewPortSize[0], style=wx.SL_HORIZONTAL)

		play_img = wx.Bitmap("./res/play.png", wx.BITMAP_TYPE_ANY)
		self.play_btn = wx.BitmapButton(self, wx.ID_ANY, play_img, (30,30))

		pause_img = wx.Bitmap("./res/pause.png", wx.BITMAP_TYPE_ANY)
		self.pause_btn = wx.BitmapButton(self, wx.ID_ANY, pause_img, (30,30))

		stop_img = wx.Bitmap("./res/stop.png", wx.BITMAP_TYPE_ANY)
		self.stop_btn = wx.BitmapButton(self, wx.ID_ANY, stop_img, (30,30))

		back_img = wx.Bitmap("./res/back.png", wx.BITMAP_TYPE_ANY)
		self.back_btn = wx.BitmapButton(self, wx.ID_ANY, back_img, (30,30))

		next_img = wx.Bitmap("./res/forward.png", wx.BITMAP_TYPE_ANY)
		self.next_btn = wx.BitmapButton(self, wx.ID_ANY, next_img, (30,30))

		self.VolumeSlider = wx.Slider(self, value=50, minValue = 0, maxValue = 100,
			style=wx.SL_HORIZONTAL)

		#default framerate is 24
		self.rates = wx.ComboBox(self, style=wx.CB_DROPDOWN, choices=self.framerates)
		self.rates.SetValue("24")
		self.FPS_btn = wx.Button(self, 1, "Set FPS")

	def Set_FPS(self, event):
		#attempts to get framerate, sometimes fails for like no reason
		try:
			self.data["FPS"] = int(self.rates.GetStringSelection())
		except:
			pass
		#divides 1000 by the FPS to get miliseconds per frame
		self.ms_per_frame = 1000/self.data["FPS"]
		if self.loaded:
			#once the song has been properly loaded
			#gets the number of frames by dividing the audio length in milliseconds by ms_per_frame
			self.song_frames = int(self.song_length / self.ms_per_frame)
			if len(self.data["Frames"]) < self.song_frames:
				#if the alteration in FPS results in a higher num of frames duplicates the end to fill it up
				for frame in range(self.song_frames - len(self.data["Frames"])):
					self.data["Frames"].append(copy.deepcopy(self.data["Frames"][-1]))
			if len(self.data["Frames"]) > self.song_frames:
				#if the alteration in FPS results in a lower num of frames truncates the frames to the new length
				self.data["Frames"] = self.data["Frames"][:self.song_frames]
			#resets the slider range and size to fit new frame length
			self.PlaybackSlider.SetRange(0, self.song_frames)
			self.PlaybackSlider.SetSize((self.GetClientSize()[0], 20))


	def LoadAudio(self, event):
		#load audio dialog box, bound to menu event gets the name of the audio file and sends it to setAudio
		with wx.FileDialog(self, "Import File", wildcard="WAV files (*.wav)|*.wav",
							style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as FileDialog:
			if (FileDialog.ShowModal() == wx.ID_CANCEL):
				return

			pathname = FileDialog.GetPath()
			self.setAudio(pathname)

	def clear_waveform(self):
		self.waveform = pygame.Surface(self.ViewPortSize)
		self.waveform.fill((100,100,100))


	def setAudio(self, pathname):
		if pathname == "":
			self.mediaPlayer.Load(pathname)
			self.clear_waveform()
			self.loaded = False
			self.window.Set_Forth_Status("")
			#reset all audio, waveform, etc to blank

		#attempts to load audio, called either from window.setdata() or from self.LoadAudio()
		#occasionally fails for unpredictable reasons, rare but results in crash
		try:
			if not self.mediaPlayer.Load(pathname):
				wx.MessageBox("Unable to load audio", "ERROR", wx.ICON_ERROR | wx.OK)
			else:
				self.data["Audio"] = pathname
				self.gen_waveform()
				self.loaded = True
				self.window.Set_Forth_Status(pathname.split("\\")[-1])
		except:
			pass

	def gen_waveform(self):
		"""
		the song is loaded and sampled, then divided into parts equal to
		the number of pixels in the pygame panel, the highest data
		is used to map out the general waveform, giving a visual map
		to sync the audio to

		future update: sampler should be an object which retains the full data
		making it much faster to load a new waveform on resize
		"""
		self.wave_data = sampler.breakdown(self.data["Audio"], self.ViewPortSize[0], self.ViewPortSize[1])
		self.waveform.fill(GREY)
		for x in range(len(self.wave_data)):
			pygame.draw.line(self.waveform, RED, (x,self.waveform.get_height()), 
				(x, self.waveform.get_height()-self.wave_data[x]), 1)

	def layout(self):
		"""
		sets the layout using box sizers
		"""
		self.visBox = wx.BoxSizer(wx.VERTICAL)
		self.visBox.Add(self.PP, 1, wx.EXPAND)

		self.button_panel = wx.BoxSizer(wx.HORIZONTAL)

		self.button_panel.Add(wx.Panel(self), 2, wx.EXPAND)

		self.playback_panel = wx.BoxSizer(wx.HORIZONTAL)
		self.playback_panel.Add(self.back_btn)
		self.playback_panel.Add(self.play_btn)
		self.playback_panel.Add(self.next_btn)
		self.playback_panel.Add(self.stop_btn)
		self.playback_panel.Add(self.pause_btn)
		self.playback_panel.Add(self.VolumeSlider)

		self.button_panel.Add(self.playback_panel, 1, wx.EXPAND)
		self.button_panel.Add(wx.Panel(self), 2, wx.EXPAND)

		self.FPS_panel = wx.BoxSizer(wx.VERTICAL)
		self.FPS_panel.Add(self.FPS_btn)
		self.FPS_panel.Add(self.rates)

		self.button_panel.Add(self.FPS_panel)

		self.mainBox = wx.BoxSizer(wx.VERTICAL)
		self.mainBox.Add(self.visBox,1)
		self.mainBox.Add(self.PlaybackSlider, 1, wx.EXPAND)
		self.mainBox.Add(self.button_panel)

	def get_current_frame(self):
		return int(self.PlaybackSlider.GetValue())

	def Update(self, second):


		if second:
			self.time_counter += 1
		if self.time_counter >= 5 and self.GetClientSize()[0] != self.ViewPortSize[0]:
			"""
			every five seconds it checks if the window was resized
			if so then it resets the pygame panel, sliders, and waveform
			resizing the timeline control panel is too slow to resize constantly, it causes crashes
			could likely be sped up by first making the pygame panel wider than the window can be
			and then only resizing the waveform surface
			as well as storing the waveform data for sampling at all times
			"""
			new_size = (self.GetClientSize()[0], self.ViewPortSize[1])
			self.PlaybackSlider.SetSize((self.GetClientSize()[0], 20))
			self.PP.set_size(new_size)
			self.PP.layout()
			self.ViewPortSize = new_size
			del self.waveform
			self.waveform = pygame.Surface(self.ViewPortSize)
			self.waveform.fill((100,100,100))
			self.time_counter = 0
			if self.loaded:
				self.gen_waveform()

		if not self.window.rendering:
			#tracks and updates the slider and pygame window according to the current play position
			#turns off when rendering in order to prevent the slider from interfereing with the render
			#by changing the current frame

			#update the pygame panel
			self.PP.draw(self.waveform, (0,0))
			self.PP.Update()

			#checks that the audio is loaded but length is still 0 plays audio to force time checking
			if self.loaded and self.song_length <= 1:
				self.onPlay(1)
			#if the audio is loaded and the length is greater than 0 stops playing
			if self.loaded and self.song_length > 1 and not self.timeset:
				self.onStop(1)
				self.timeset = True
			#if audio loaded, stopped, and the length of frames is 1, generates new frames to fill out the length
			if self.loaded and self.timeset and len(self.data["Frames"]) == 1:
				for frame in range(self.song_frames):
					self.data["Frames"].append(copy.deepcopy(self.data["Frames"][0]))

			#resets the playbackslider to the frame according to the time in milliseconds
			offset = self.mediaPlayer.Tell()
			self.PlaybackSlider.SetValue(int(offset / self.ms_per_frame))
			if self.PlaybackSlider.GetMax() > 0:
				self.current_pos = int((self.PlaybackSlider.GetValue() / self.PlaybackSlider.GetMax()) * self.ViewPortSize[0])

			#draws an indicator on the pygame panel according to where the current position is
			self.PP.draw(self.waveform, (0,0))
			pygame.draw.line(self.PP.screen, GREEN, (self.current_pos-1, self.ViewPortSize[1]), (self.current_pos-1, 0), 1)
			pygame.draw.line(self.PP.screen, GREEN, (self.current_pos+1, self.ViewPortSize[1]), (self.current_pos+1, 0), 1)
			self.PP.Update()

			self.data["Current Frame"] = self.get_current_frame()

	def OnClose(self):
		#pygame panel returns errors if attempting to close window without exiting pygame
		self.PP.OnClose()

class testFrame(wx.Frame):
	def __init__(self, parent, title, size):
		wx.Frame.__init__(self,
			parent, wx.ID_ANY, title, pos=(1,1), size=size,
			style = (wx.DEFAULT_FRAME_STYLE|wx.WANTS_CHARS))

		self.listener = Key_listener()

		#sets all data to default position for a new project
		self.new_project()

		#setting up layout
		self.mainBox = wx.BoxSizer(wx.HORIZONTAL)

		#add elements and panels here to allow them to make changes to the window
		self.timelineCtrl = TimelineCtrl(self, wx.ID_ANY, self.data, self, (2000,50))

		#creates menus and tells all control panels to set their menus as well
		self.create_menus()

		self.set_layout()

		self.timer = wx.Timer(self)

		#sets the time the last tick took place
		#tickspeed is useful in determining if the program is running at full speed
		self.lasttick = datetime.now().second

		#####################statusbar
		self.statusbar = self.CreateStatusBar(5)
		
		#####################bindings
		self.bind_all()
		self.timer.Start()
		self.Maximize(True)

	def set_layout(self):
		#organizes layout
		"""
		===================
		| |             | |
		|1|     2       |3|
		| |_____________| |
		|_|______4______|_|

		1- objCtrl
		2- renderCtrl
		3- stateCtrl
		4- timelineCtrl

		"""
		self.center = wx.BoxSizer(wx.VERTICAL)
		self.center.Add(wx.Panel(self, size=(2000,1)))
		self.center.Add(self.timelineCtrl, 0, wx.EXPAND) #4

		self.mainBox.Add(self.center, 1, wx.EXPAND)      #2, 4

		self.SetSizer(self.mainBox)

	def bind_all(self):
		self.Bind(wx.EVT_TIMER, self.tickrate, self.timer)
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.Bind(wx.EVT_MENU, self.OnNew, self.newProj)
		self.Bind(wx.EVT_MENU, self.OnClose, self.closeWin)
		self.Bind(wx.EVT_MENU, self.LoadData, self.loadData)
		self.Bind(wx.EVT_MENU, self.SaveData, self.saveData)
		self.Bind(wx.EVT_MENU, self.SaveAsData, self.saveAsData)

		self.Bind(wx.EVT_MENU, self.On_tutorial1, self.tutorial1)
		self.Bind(wx.EVT_MENU, self.On_tutorial2, self.tutorial2)
		self.Bind(wx.EVT_MENU, self.On_tutorial3, self.tutorial3)
		self.Bind(wx.EVT_MENU, self.On_tutorial4, self.tutorial4)
		self.Bind(wx.EVT_MENU, self.On_tutorial5, self.tutorial5)
		self.Bind(wx.EVT_MENU, self.On_tutorial6, self.tutorial6)

	def create_menus(self):
		self.menubar = wx.MenuBar()
		self.fileMenu = wx.Menu()

		#creates the menu items for saving/loading the current project
		self.newProj = wx.MenuItem(self.fileMenu, wx.ID_ANY, "&New Project\tCtrl+N", 'New Project')
		self.loadData = wx.MenuItem(self.fileMenu, wx.ID_ANY, '&Load Project\tCtrl+O', 'Load Animation')
		self.saveData = wx.MenuItem(self.fileMenu, wx.ID_ANY, '&Save Project\tCtrl+S', 'Save Animation')
		self.saveAsData = wx.MenuItem(self.fileMenu, wx.ID_ANY, '&Save Project As\tShift+Ctrl+S', 'Save Animation As')

		self.fileMenu.Append(self.newProj)
		self.fileMenu.Append(self.loadData)
		self.fileMenu.Append(self.saveData)
		self.fileMenu.Append(self.saveAsData)
		self.fileMenu.AppendSeparator()

		self.closeWin = wx.MenuItem(self.fileMenu, wx.ID_EXIT, '&Quit\tCtrl+X', 'Quit Application')

		self.fileMenu.AppendSeparator()

		self.fileMenu.Append(self.closeWin)

		self.menubar.Append(self.fileMenu, '&File')

		#creates each control panel's menus in order
		#the order these are called determines how the menus are laid out
		self.timelineCtrl.create_menus()

		#help menu links back to youtube tutorials on how to use the program
		self.helpMenu = wx.Menu()

		self.tutorial1 = wx.MenuItem(self.helpMenu, wx.ID_ANY, "&About All")
		self.tutorial2 = wx.MenuItem(self.helpMenu, wx.ID_ANY, "&About Objects")
		self.tutorial3 = wx.MenuItem(self.helpMenu, wx.ID_ANY, "&About Timeline")
		self.tutorial4 = wx.MenuItem(self.helpMenu, wx.ID_ANY, "&About Renderer")
		self.tutorial5 = wx.MenuItem(self.helpMenu, wx.ID_ANY, "&About States")
		self.tutorial6 = wx.MenuItem(self.helpMenu, wx.ID_ANY, "&About Creating Video")

		self.helpMenu.Append(self.tutorial1)
		self.helpMenu.Append(self.tutorial2)
		self.helpMenu.Append(self.tutorial3)
		self.helpMenu.Append(self.tutorial4)
		self.helpMenu.Append(self.tutorial5)
		self.helpMenu.Append(self.tutorial6)

		self.menubar.Append(self.helpMenu, "&Help")

		self.SetMenuBar(self.menubar)


		#opens to a playlist on youtube containing the tutorials for use
		#could probably be turned into a single function
	def On_tutorial1(self, event):
		webbrowser.open("https://www.youtube.com/watch?v=oBAQy1D5r7o&list=PLkVdGBkhsW-WdYoTn-Uf8SouWUh3vGnGO&index=1")

	def On_tutorial2(self, event):
		webbrowser.open("https://www.youtube.com/watch?v=5L98weJKd48&list=PLkVdGBkhsW-WdYoTn-Uf8SouWUh3vGnGO&index=2")

	def On_tutorial3(self, event):
		webbrowser.open("https://www.youtube.com/watch?v=Sm7fqqMC0Ks&list=PLkVdGBkhsW-WdYoTn-Uf8SouWUh3vGnGO&index=3")

	def On_tutorial4(self, event):
		webbrowser.open("https://www.youtube.com/watch?v=ar9PjawB-qs&list=PLkVdGBkhsW-WdYoTn-Uf8SouWUh3vGnGO&index=4")

	def On_tutorial5(self, event):
		webbrowser.open("https://www.youtube.com/watch?v=rqVycueA8Tg&list=PLkVdGBkhsW-WdYoTn-Uf8SouWUh3vGnGO&index=5")

	def On_tutorial6(self, event):
		webbrowser.open("https://www.youtube.com/watch?v=15ymfD67Qbk&list=PLkVdGBkhsW-WdYoTn-Uf8SouWUh3vGnGO&index=6")

	def tickrate(self, event):
		"""
		Controls the tickrate of the software
		allows it to run at max speed, capped by the vsync rate
		every second it sets the current tickrate to monitor the proccessing speed of the program
		sends True signal to the control panels update function once per second
		current time is time since Jan 1, 1970
		"""
		current_time = (datetime.now()-datetime(1970,1,1)).total_seconds()
		if (current_time - self.lasttick) >= 1:
			self.Set_Third_Status(str(self.ticks) )
			self.lasttick = current_time
			self.ticks = 0
			self.timelineCtrl.Update(True)

		else:
			self.ticks += 1
			self.timelineCtrl.Update(False)

		#statusbar set functions, to be compressed into single function "Set_Status"
	def Set_First_Status(self, text):
		self.Set_Status(0, text)

	def Set_Second_Status(self, text):
		self.Set_Status(1, text)

	def Set_Third_Status(self, text):
		self.Set_Status(2, text)

	def Set_Forth_Status(self, text):
		self.Set_Status(3, text)

	def Set_Fifth_Status(self, text):
		self.Set_Status(4, text)

	def Set_Status(self, bar, text):
		self.statusbar.SetStatusText( text, bar)

	def LoadData(self, event):
		"""
		self.data is loaded from a json file named *.ani (short for animate)
		load data selects a file with a file dialog and loads it as self.data
		then it calls self.set_data(), which loads all the images, audio, and settings from the file
		title of the animation is added to the window title

		OnNew offers to save the current project if anything has been added
		after it calls new_project to wipe everything clean
		"""
		with wx.FileDialog(self, "Load Animation", wildcard="ANI files (*.ani)|*.ani",
							style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = fileDialog.GetPath()
			tempData = open(pathname, "r")
			self.data = json.loads(tempData.read())
			tempData.close()
			self.set_data()
			self.timelineCtrl.setAudio(self.data["Audio"])
			self.pathname = pathname
			self.SetTitle("%s (%s)".format(version_name,  self.pathname.split("\\")[-1].split(".")[0]))

	def OnNew(self):
		if len(self.data["Object List"]) > 1 or self.data["Audio"] != "":
			self.SaveAsData(1)
		self.new_project()

	def new_project(self):
		#sets the animation state data into default, for more details see data_default.py
		self.data = copy.deepcopy(data_default.data)

		#dict, holds all images as opengl textures "image name":obj2d
		self.Image_list = {}
		#holds current file path to save and load the animation
		self.pathname = ""
		#signals to certain functions that the video is being rendered to disable audio syncing
		self.rendering = False
		self.ticks = 0
		#clears the project name
		self.SetTitle(version_name)
		try:
			self.set_data()
		except:
			pass

	def set_data(self):
		#calls every control panel to load the new data
		self.timelineCtrl.set_data(self.data)

	def SaveAsData(self, event):
		with wx.FileDialog(self, "Save animation", wildcard="ANI files (*.ani)|*.ani",
			style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = fileDialog.GetPath()
			self.writeData(pathname)

	def SaveData(self, event):
		if self.pathname != "":
			self.writeData(self.pathname)			
		else:
			self.SaveAsData(event)

	def writeData(self, pathname):
		try:
			with open(pathname, 'w') as file:
				file.write(json.dumps(self.data))
		except IOError:
			wx.LogError("Cannot save current data in file %s" % pathname)
		self.pathname = pathname
		self.SetTitle("%s (%s)".format(version_name,  self.pathname.split("\\")[-1].split(".")[0]))

	def OnClose(self, event):
		wx.Exit()
		exit()

if __name__ == "__main__":
	app = wx.App()
	view = testFrame(parent=None, title=version_name, size=(1500,700))
	view.Show()
	app.MainLoop()
