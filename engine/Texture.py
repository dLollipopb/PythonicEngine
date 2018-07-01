from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
def texture_load(path,mag,min):
	textid=glGenTextures(1)
	glBindTexture(GL_TEXTURE_2D, textid)
	img=pygame.image.load(path)
	glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,mag)
	if min in [GL_LINEAR_MIPMAP_NEAREST,GL_NEAREST_MIPMAP_LINEAR]:
		glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,min)
		gluBuild2DMipmaps(GL_TEXTURE_2D, 3, img.get_width(), img.get_height(),GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(img, "RGBA"))
	else:
		glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,min)
		glTexImage2D(GL_TEXTURE_2D, 0, 3, img.get_width(), img.get_height(), 0,GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(img, "RGBA"))
	return textid
def texture_create(w,h,mag,min):
	textid=glGenTextures(1)
	glBindTexture(GL_TEXTURE_2D, textid)
	img=pygame.Surface((w,h))
	glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,mag)
	if min in [GL_LINEAR_MIPMAP_NEAREST,GL_NEAREST_MIPMAP_LINEAR]:
		glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,min)
		gluBuild2DMipmaps(GL_TEXTURE_2D, 3, img.get_width(), img.get_height(),GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(img, "RGBA"))
	else:
		glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,min)
		glTexImage2D(GL_TEXTURE_2D, 0, 3, img.get_width(), img.get_height(), 0,GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(img, "RGBA"))
	return textid
def pixel(path):
	return texture_load(path,GL_NEAREST,GL_NEAREST)
def smooth(path):
	return texture_load(path,GL_LINEAR,GL_LINEAR_MIPMAP_NEAREST)