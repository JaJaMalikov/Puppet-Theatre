#graphical libraries
import wx
import wx.media
from pygame.locals import *
import pygame

#other built in libraries
import copy
import os
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

class TimelineCtrl(wx.Panel):
	"""
	loads the audio and generates a wave form
	controls the current position in time, uses a slider to sync up the audio with the current frame
	allows switching between multiple framerates
	"""
	def __init__(self, parent, ID, data, window, listener, ViewPortSize=(4000,80)):
		wx.Panel.__init__(self, parent, ID, style=wx.RAISED_BORDER)
		self.ViewPortSize = ViewPortSize
		self.window = window
		self.data = data
		self.listener = listener
		self.wave_data = []
		self.song_length = 1
		self.song_frames = 1
		self.loaded = False
		self.timeset = False
		self.current_pos = 0
		self.time_counter = 0
		self.wavedata = sampler.wavedata()

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

	def onPause(self, event):
		self.mediaPlayer.Pause()

	def onStop(self, event):
		"""
		resets the current frames after stopping
		must seek to 1ms to prevent "phantom frame" effect
		"""
		self.mediaPlayer.Stop()
		self.data["Current Frame"] = 0
		self.mediaPlayer.Seek(1)


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
		self.PP = PygamePanel(self, 1, self.ViewPortSize, self.window, self.listener)
		self.mediaPlayer = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER)

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
		#self.window.PushHistory()

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
		#try:
		if not self.mediaPlayer.Load(pathname):
			wx.MessageBox("Unable to load audio", "ERROR", wx.ICON_ERROR | wx.OK)
		else:
			self.data["Audio"] = pathname
			self.wavedata.gen_wavedata(self.data["Audio"])
			self.gen_waveform()
                        self.loaded = True
                        import os
                        self.window.Set_Forth_Status(os.path.basename(pathname))
		#except:
		#	pass

	def gen_waveform(self):
		"""
		the song is loaded and sampled, then divided into parts equal to
		the number of pixels in the pygame panel, the highest data
		is used to map out the general waveform, giving a visual map
		to sync the audio to

		future update: sampler should be an object which retains the full data
		making it much faster to load a new waveform on resize
		"""
		self.wave_data = self.wavedata.breakdown(self.ViewPortSize[0], self.ViewPortSize[1])
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
		self.mainBox.Add(self.button_panel)

	def Update(self, second):


		if second:
			self.time_counter += 1
		if self.time_counter >= 1 and self.GetClientSize()[0] != self.ViewPortSize[0]:
			"""
			every five seconds it checks if the window was resized
			if so then it resets the pygame panel, sliders, and waveform
			resizing the timeline control panel is too slow to resize constantly, it causes crashes
			could likely be sped up by first making the pygame panel wider than the window can be
			and then only resizing the waveform surface
			as well as storing the waveform data for sampling at all times
			"""
			new_size = (self.GetClientSize()[0], self.ViewPortSize[1])
			#self.PP.set_size(new_size)
			#self.PP.layout()
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
			#self.PP.draw(self.waveform, (0,0))
			#self.PP.Update()

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
				for frame in range(self.song_frames+2):
					self.data["Frames"].append(copy.deepcopy(self.data["Frames"][0]))

			if self.listener.get_mouse_button(1):
				self.data["Current Frame"] = int(self.listener.get_mouse_pos()[0]/self.ViewPortSize[0]*self.song_frames)
				self.current_pos = int(self.data["Current Frame"]/self.song_frames*self.ViewPortSize[0])
				self.mediaPlayer.Seek(self.data["Current Frame"] * self.ms_per_frame)
			else:
				offset = self.mediaPlayer.Tell()
				ratio = offset/self.song_length
				self.current_pos = int(ratio * self.ViewPortSize[0])
				self.data["Current Frame"] = int(self.song_frames * ratio)

			#draws an indicator on the pygame panel according to where the current position is
			self.PP.draw(self.waveform, (0,0))
			pygame.draw.line(self.PP.screen, GREEN, (self.current_pos-2, self.ViewPortSize[1]), (self.current_pos-2, 0), 3)
			pygame.draw.line(self.PP.screen, GREEN, (self.current_pos+2, self.ViewPortSize[1]), (self.current_pos+2, 0), 3)

	def OnClose(self):
		#pygame panel returns errors if attempting to close window without exiting pygame
		self.PP.OnClose()

