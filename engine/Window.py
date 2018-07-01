import pygame,os
from threading import Thread
from OpenGL.GL import *
from OpenGL.GLU import *
from Matrix import Quaternion,Vector
from ctypes import windll
GetSystemMetrics = ctypes.windll.user32.GetSystemMetrics
class Window:
	def __init__(self,w=-1,h=-1,fullscreen=False,noframe=False,resize=False):
		pygame.init()
		attr=pygame.DOUBLEBUF|pygame.OPENGL
		if fullscreen:
			attr|=pygame.FULLSCREEN|pygame.HWSURFACE
		if noframe:
			attr|=pygame.NOFRAME
		elif resize:
			attr|=pygame.RESIZABLE
		if w==-1:
			self.w=GetSystemMetrics(0)
		else:
			self.w=w
		if h==-1:
			self.h=GetSystemMetrics(1)
		else:
			self.h=h
		os.environ['SDL_VIDEO_WINDOW_POS']=str(GetSystemMetrics(0)//2-self.w//2)+","+str(GetSystemMetrics(1)//2-self.h//2)
		self.screen=pygame.display.set_mode((self.w,self.h),attr)
		self.framebuffer=glGenFramebuffers(1)
		self.renderbuffer=glGenRenderbuffers(1)
		glBindRenderbuffer(GL_RENDERBUFFER,self.framebuffer)
		glRenderbufferStorage(GL_RENDERBUFFER,GL_DEPTH_COMPONENT,self.w,self.h)
		glBindRenderbuffer(GL_RENDERBUFFER,0)
		pygame.display.set_caption("Window")
		self.aspect_ratio=float(self.w)/float(self.h)
		glClearDepth(1.0)
		glEnable(GL_DEPTH_TEST)
		glDepthFunc(GL_LEQUAL)
		glEnable(GL_CULL_FACE)
		self.Clock=pygame.time.Clock()
		self.timedelta=1.0
		glViewport(0,0,self.w,self.h)
		self.lighting=False
		self.looping=False
		self.obj=[]
		self.ifkeydown=False
		self.keydown=[]
		self.quat=Quaternion().empty()
		self.x,self.y,self.z=0.0,0.0,0.0
		glEnable(GL_LIGHT0)
		glEnable(GL_NORMALIZE)
		glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3,0.3,0.3])
		glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0,1.0,1.0])
		def event():
			pass
		def reshape():
			glMatrixMode(GL_PROJECTION)
			glLoadIdentity()
			gluPerspective(100,self.aspect_ratio, 0.1, 1000.0)
			glMatrixMode(GL_MODELVIEW)
			glLoadIdentity()
		def draw():
			glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
			self.quat.matrix()
			glTranslatef(-self.x,-self.y,-self.z)
			glLightfv(GL_LIGHT0, GL_POSITION,[1.0,1.0,1.0,0.0])
			for i in self.obj:
				glPushMatrix()
				i.event()
				glPopMatrix()
		self.event=event
		self.reshape=reshape
		self.draw=draw
		self.keydowns=[]
		self.keyups=[]
		self.keys=[[False,False,False] for i in range(512)]
		self.mouse=[[False,False,False],[False,False,False],[False,False,False],[False,False,False],[False,False,False]]
		self.mousedowns=[]
		self.mouseups=[]
	def rotateglobal(self,angle,x,y,z):
		self.quat*=Quaternion().angle(angle,Vector(x,y,z).normalize())
	def rotate(self,angle,x,y,z):
		self.quat=(self.quat.invert()*Quaternion().angle(angle,Vector(x,y,z).normalize())).invert()
	def move(self,vect,dist=1.0):
		self.x+=vect.x*dist
		self.y+=vect.y*dist
		self.z+=vect.z*dist
	def addObject(self,obj):
		self.obj.append(obj)
	def loop(self):
		self.looping=True
		while self.looping:
			self.timedelta=self.Clock.get_time()/1000.0
			for i in self.keydowns:
				self.keys[i][1]=False
			for i in self.keyups:
				self.keys[i][2]=False
			self.keydowns=[]
			self.keyups=[]
			for i in self.mousedowns:
				self.mouse[i][1]=False
			for i in self.mouseups:
				self.mouse[i][2]=False
			self.mousedowns=[]
			self.mouseups=[]
			self.ifkeydown=False
			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					self.looping=False
					pygame.quit()
					break
				if event.type==pygame.KEYDOWN:
					self.keys[event.key][0]=True
					self.keys[event.key][1]=True
					self.keydowns.append(event.key)
					print event.key
				if event.type==pygame.KEYUP:
					self.keys[event.key][0]=False
					self.keys[event.key][2]=True
					self.keyups.append(event.key)
				if event.type==pygame.MOUSEBUTTONDOWN:
					self.mouse[event.button-1][0]=True
					self.mouse[event.button-1][1]=True
					self.mousedowns.append(event.button-1)
					print event.button
				if event.type==pygame.MOUSEBUTTONUP:
					self.mouse[event.button-1][0]=False
					self.mouse[event.button-1][2]=True
					self.mouseups.append(event.button-1)
				if event.type==pygame.MOUSEMOTION:
					self.mousex,self.mousey=event.pos
			if not self.looping:
				break
			self.event()
			self.reshape()
			self.draw()
			pygame.display.flip()
			self.Clock.tick(60)
	def background(self,r,g,b,a=1.0):
		glClearColor(r,g,b,a)
	def exit(self):
		self.looping=False
	def title(self,text):
		pygame.display.set_caption(text)
	def mousevisible(self,q):
		pygame.mouse.set_visible(q)
	def mousesetpos(self,x,y):
		pygame.mouse.set_pos(x,y)