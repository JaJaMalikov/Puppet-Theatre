import wx

class Editor(wx.Frame):
	def __init__(self, parent, id):
		wx.Frame.__init__(self, parent, id, 'Finger Puppet Theatre', size = (1200,800))
		self.initMenu()
		self.initStatusBar()

	def initMenu(self):
		menubar = wx.MenuBar()
		fileMenu = wx.Menu()
		fileItem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
		menubar.Append(fileMenu, '&File')

		self.SetMenuBar(menubar)
		self.Bind(wx.EVT_MENU, self.OnQuit, fileItem)

	def initStatusBar(self):
		self.statusBar = self.CreateStatusBar()
		self.statusBar.SetFieldsCount(3)
		self.statusBar.SetStatusWidths([-1,-4,-2])
		#self.statusBar.SetStatusStyles([wx.SB_FLAT,wx.SB_FLAT,wx.SB_FLAT])
		self.statusBar.SetBackgroundColour('gray')
		self.statusBar.SetStatusText("fps :3", 0)
		self.statusBar.SetStatusText("Recording/Rendering", 1)
		self.statusBar.SetStatusText("time", 2)


	def OnQuit(self, e):
		self.Close()


if __name__ == '__main__':
	app=wx.App()
	frame=Editor(parent=None, id=-1)
	frame.Show()
	app.MainLoop()