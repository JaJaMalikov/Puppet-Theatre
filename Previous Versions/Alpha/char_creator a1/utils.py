import pygame

def rotate(surface, angle, pivot, offset, scale):
	"""Rotate the surface around the pivot point.

	Args:
		surface (pygame.Surface): The surface that is to be rotated.
		angle (float): Rotate by this angle.
		pivot (tuple, list, pygame.math.Vector2): distance from upper left corner of the destination
		offset (pygame.math.Vector2): distance from center 0,0 being center -1,-1, being just to the upper left.
		scale (float): scale the image being rotated
	"""
	rotated_image = pygame.transform.rotozoom(surface, -angle, scale)  # Rotate the image.
	rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
	# Add the offset vector to the center/pivot point to shift the rect.
	rect = rotated_image.get_rect(center=pivot+rotated_offset)
	return rotated_image, rect  # Return the rotated image and shifted rect.



if __name__ == '__main__':
	pygame.init()
