import wx, sys, os, wx.lib.newevent, wx.stc as stc, string

class SyntaxControl(stc.StyledTextCtrl):

	def __init__(self, parent, style=wx.SIMPLE_BORDER):
		stc.StyledTextCtrl.__init__(self, parent, style=style)
		self._styles = [None] * 32
		self._free = 1
		self.SetWrapMode(True)
		self.SetIndent(4)
		self.SetTabIndents(True)
		return
