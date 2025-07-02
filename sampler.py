import sys
import wave
import struct

#loads wav file as array of ints which can be normalized and turned into a visual waveform
#to be restructured later into an object/class for faster resize times

class wavedata:
	def __init__(self):
		self.filename = ""
		self.wavedata = []
		self.wd_len = 0

	def gen_wavedata(self, filename):
		self.filename = filename
		self.to_mono()

	def to_mono(self, channel=0):
		with wave.open(self.filename, 'rb') as wf:
			n_channels = wf.getnchannels()
			n_frames = wf.getnframes()
			sampwidth = wf.getsampwidth()
			frames = wf.readframes(n_frames)

		if sampwidth == 1:
			fmt = "<%dB" % (n_frames * n_channels)
		elif sampwidth == 2:
			fmt = "<%dh" % (n_frames * n_channels)
		elif sampwidth == 4:
			fmt = "<%di" % (n_frames * n_channels)
		else:
			raise ValueError("Unsupported sample width: %d" % sampwidth)

		data = struct.unpack(fmt, frames)

		if n_channels > 1:
			self.wavedata = list(data[channel::n_channels])
		else:
			self.wavedata = list(data)

	def Normalize(self, lst, height):
		return [int(i/max(lst)*height) for i in lst]
		
	def breakdown(self, length, height):
		self.wd_len = int(len(self.wavedata) / length)
		chunks = [ self.wavedata[x:x+ self.wd_len ] for x in range(0, len(self.wavedata), self.wd_len) ]

		final_form = []

		for x in range(length):
			final_form.append( max(chunks[x]))

		return self.Normalize(final_form, height)
