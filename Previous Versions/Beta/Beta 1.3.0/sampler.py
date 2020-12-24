import sys
import scipy.io.wavfile as wav

#loads wav file as array of ints which can be normalized and turned into a visual waveform
#to be restructured later into an object/class for faster resize times

loc = 33

def to_mono(fname, channel=0):
	(freq, sig) = wav.read(fname)
	if sig.ndim == 2:
		return (sig[:,channel], freq)
	return (sig, freq)

def Normalize(lst, height):
	return [int(i/max(lst)*height) for i in lst]
	
def breakdown(filename, length, height):
	array = list(to_mono(filename)[0] )

	ar_len = int(len(array) / length)

	chunks = [ array[x:x+ ar_len ] for x in range(0, len(array), ar_len) ]

	final_form = []

	for x in range(length):
		final_form.append( max(chunks[x]))

	return Normalize(final_form, height)

if __name__ == '__main__':
	print(breakdown(sys.argv[1], 300))

