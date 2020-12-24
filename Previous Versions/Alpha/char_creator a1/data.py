#!/usr/bin/env python3


class data:
	def __init__(self, angle, pivot, offset):
		self.angle = angle
		self.pivot = pivot
		self.offset = offset

if __name__ == '__main__':
	herp = data(1,2,3)
	print(herp.angle)
	print(herp.pivot)
	print(herp.offset)