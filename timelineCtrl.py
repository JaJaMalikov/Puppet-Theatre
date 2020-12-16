import wx
import os

import wx.media

from pygame.locals import *

import  wx.lib.newevent, wx.stc as stc
import numpy as np

import datetime
from datetime import datetime
import sampler

from consts import * 

import copy
from PygamePanel import PygamePanel
import pygame


class timelineCtrl(wx.Panel):
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

		self.loadAudio = wx.MenuItem(self.window.fileMenu, wx.ID_ANY, 
			'&Load Audio\tCtrl+A', 'Load Audio')
		self.window.fileMenu.Append(self.loadAudio)

		self.create_objects()
		self.Set_FPS(1)

		self.waveform = pygame.Surface(self.ViewPortSize)
		self.waveform.fill((100,100,100))

		self.layout()
		self.SetSizer(self.mainBox)

		self.next_btn.Bind(wx.EVT_BUTTON, self.onNext)
		self.back_btn.Bind(wx.EVT_BUTTON, self.onBack)
		self.play_btn.Bind(wx.EVT_BUTTON, self.onPlay)
		self.stop_btn.Bind(wx.EVT_BUTTON, self.onStop)
		self.pause_btn.Bind(wx.EVT_BUTTON, self.onPause)
		self.VolumeSlider.Bind(wx.EVT_SLIDER, self.onSetVolume)
		self.FPS_btn.Bind(wx.EVT_BUTTON, self.Set_FPS)
		self.window.Bind(wx.EVT_MENU, self.LoadAudio, self.loadAudio)
		self.PlaybackSlider.Bind(wx.EVT_SLIDER, self.onSliderScroll)

	def onSetVolume(self, event):
		self.mediaPlayer.SetVolume(self.VolumeSlider.GetValue() / 100)

	def onNext(self, event):
		self.mediaPlayer.Seek(int(self.mediaPlayer.Tell() + self.ms_per_frame))

	def onBack(self, event):
		self.mediaPlayer.Seek(int(self.mediaPlayer.Tell() - self.ms_per_frame))

	def onPlay(self, event):
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
		self.mediaPlayer.Pause()

	def onStop(self, event):
		self.mediaPlayer.Stop()
		self.data["Current Frame"] = 0
		self.mediaPlayer.Seek(1)

	def onSliderScroll(self, event):
		offset = self.PlaybackSlider.GetValue()
		self.mediaPlayer.Seek(int(offset * self.ms_per_frame))

	def set_data(self, data):
		self.data = data
		self.Set_FPS(1)
		self.rates.SetValue(str(self.data["fps"]))

	def create_objects(self):
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

		self.rates = wx.ComboBox(self, style=wx.CB_DROPDOWN, choices=self.framerates)
		self.rates.SetValue("24")
		self.FPS_btn = wx.Button(self, 1, "Set FPS")

	def Set_FPS(self, event):
		try:
			self.data["fps"] = int(self.rates.GetStringSelection())
		except:
			pass
		self.ms_per_frame = 1000/self.data["fps"]
		if self.loaded:
			self.song_frames = int(self.song_length / self.ms_per_frame)
			if len(self.data["Frames"]) < self.song_frames:
				for frame in range(self.song_frames - len(self.data["Frames"])):
					self.data["Frames"].append(copy.deepcopy(self.data["Frames"][-1]))
			if len(self.data["Frames"]) > self.song_frames:
				self.data["Frames"] = self.data["Frames"][:self.song_frames]
			self.PlaybackSlider.SetRange(0, self.song_frames)
			self.PlaybackSlider.SetSize((self.GetClientSize()[0], 20))


	def LoadAudio(self, event):
		with wx.FileDialog(self, "Import File", wildcard="WAV files (*.wav)|*.wav",
							style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as FileDialog:
			if (FileDialog.ShowModal() == wx.ID_CANCEL):
				return

			pathname = FileDialog.GetPath()
			self.setAudio(pathname)

	def setAudio(self, pathname):
		try:
			if not self.mediaPlayer.Load(pathname):
				wx.MessageBox("Unable to load audio", "ERROR", wx.ICON_ERROR | wx.OK)
			else:
				self.data["audio"] = pathname
				self.gen_waveform()
				self.loaded = True
				self.window.Set_Forth_Status(pathname.split("\\")[-1])
		except:
			pass

	def gen_waveform(self):
		self.wave_data = sampler.breakdown(self.data["audio"], self.ViewPortSize[0], self.ViewPortSize[1])
		self.waveform.fill(GREY)
		for x in range(len(self.wave_data)):
			pygame.draw.line(self.waveform, RED, (x,self.waveform.get_height()), 
				(x, self.waveform.get_height()-self.wave_data[x]), 1)

	def layout(self):
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
			self.PP.draw(self.waveform, (0,0))
			self.PP.Update()
			if self.loaded and self.song_length <= 1:
				self.onPlay(1)
			if self.loaded and self.song_length > 1 and not self.timeset:
				self.onStop(1)
				self.timeset = True
			if self.loaded and self.timeset and len(self.data["Frames"]) == 1:
				for frame in range(self.song_frames):
					self.data["Frames"].append(copy.deepcopy(self.data["Frames"][0]))

			offset = self.mediaPlayer.Tell()
			self.PlaybackSlider.SetValue(int(offset / self.ms_per_frame))
			if self.PlaybackSlider.GetMax() > 0:
				self.current_pos = int((self.PlaybackSlider.GetValue() / self.PlaybackSlider.GetMax()) * self.ViewPortSize[0])

			self.PP.draw(self.waveform, (0,0))
			pygame.draw.line(self.PP.screen, GREEN, (self.current_pos-1, self.ViewPortSize[1]), (self.current_pos-1, 0), 1)
			pygame.draw.line(self.PP.screen, GREEN, (self.current_pos+1, self.ViewPortSize[1]), (self.current_pos+1, 0), 1)
			self.PP.Update()

			self.data["Current Frame"] = self.get_current_frame()

	def OnClose(self):
		self.PP.OnClose()

class testFrame(wx.Frame):
	def __init__(self, parent, title, size):
		wx.Frame.__init__(self,
			parent, wx.ID_ANY, title, pos=(1,1), size=size,
			style=(wx.DEFAULT_FRAME_STYLE|wx.WANTS_CHARS))
		self.data = {}

		self.data["Object List"] = {"Camera":{"Images":["Camera"]}}
		self.data["Background Color"] = [0.0,0.0,0.0,0.0]
		self.data["Current Frame"] = 0
		self.data["Current Object"] = ""
		self.data["imgs"] = []
		self.data["image list"] = []
		self.data["selection"] = 0
		self.data["fps"] = 24
		self.data["audio"] = ""
		self.data["Current State"] = "position"
		self.data["Frames"] = []
		self.data["Frames"].append(
				{
				"Camera":{
					"Current Image": "Camera",
					"pos":[0,0,0],
					"scale":1,
					"angle":0,
					"flipX":1.0,
					"flipY":1.0,
					"visible":True,
					"keyframe":False
					}
				}
			)

		#menu start
		self.menubar = wx.MenuBar()
		self.fileMenu = wx.Menu()

		self.last_time = 0

		self.timelineCtrl = timelineCtrl(self, wx.ID_ANY, self.data, self, (1500,50))

		#menu cont
		self.closewin = self.fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit Application')

		self.menubar.Append(self.fileMenu, '&File')
		self.SetMenuBar(self.menubar)

		#set layout
		self.mainBox = wx.BoxSizer(wx.HORIZONTAL)
		self.mainBox.Add(self.timelineCtrl, 1, wx.EXPAND)
		self.SetSizer(self.mainBox)

		self.timer = wx.Timer(self)

		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.Bind(wx.EVT_TIMER, self.TimerFire, self.timer)

		self.timer.Start()

	def TimerFire(self, event):
		current_time = (datetime.now() - datetime(1970,1,1)).total_seconds()
		if (current_time - self.last_time) >= 1:
			self.last_time = current_time
			self.timelineCtrl.Update(True)
		else:
			self.timelineCtrl.Update(False)

	def OnClose(self, event):
		wx.Exit()
		exit()


if __name__ == "__main__":
	app = wx.App()
	view = testFrame(parent=None, title='Puppet Theatre', size=(1500,700))
	view.Show()
	app.MainLoop()
