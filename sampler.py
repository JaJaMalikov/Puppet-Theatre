import sys
import scipy.io.wavfile as wav

#loads wav file as array of ints which can be normalized and turned into a visual waveform
#to be restructured later into an object/class for faster resize times

loc = 33

class wavedata:
	def __init__(self):
		self.filename = ""
		self.wavedata = []
		self.wd_len = 0

	def gen_wavedata(self, filename):
		self.filename = filename
		self.to_mono()

	def to_mono(self, channel=0):
		(freq, sig) = wav.read(self.filename)
		if sig.ndim == 2:
			self.wavedata = list(sig[:,channel])
		else:
			self.wavedata = list(sig)

	def Normalize(self, lst, height):
		return [int(i/max(lst)*height) for i in lst]
		
	def breakdown(self, length, height):
		self.wd_len = int(len(self.wavedata) / length)
		chunks = [ self.wavedata[x:x+ self.wd_len ] for x in range(0, len(self.wavedata), self.wd_len) ]

		final_form = []

		for x in range(length):
			final_form.append( max(chunks[x]))

		return self.Normalize(final_form, height)
