from OpenGL.GL import *
import math
from Mesh import Mesh
from Matrix import Quaternion,Vector
def normal(x1,y1,z1,x2,y2,z2,x3,y3,z3):
	ax,ay,az=x1-x2,y1-y2,z1-z2
	bx,by,bz=x2-x3,y2-y3,z2-z3
	nx,ny,nz=ay*bz-az*by,az*bx-ax*bz,ax*by-ay*bx
	ds=math.sqrt(nx**2+ny**2+nz**2)
	return nx/ds,ny/ds,nz/ds
class Model:
	def __init__(self):
		class EmptyMesh:
			def __init(self):
				pass
			def draw(self):
				pass
			def drawVbo(self):
				pass
		self.x,self.y,self.z=0.0,0.0,0.0
		self.w,self.h,self.d=1.0,1.0,1.0
		self.mesh=EmptyMesh()
		self.tex=0
		self.quat=Quaternion().empty()
		self.shad=False
	def texture(self,t):
		self.tex=t
	def rotate(self,angle,x,y,z):
		self.quat=self.quat*Quaternion().angle(angle,Vector(x,y,z).normalize())
	def rotateglobal(self,angle,x,y,z):
		self.quat=(self.quat.invert()*Quaternion().angle(angle,Vector(x,y,z).normalize())).invert()
	def move(self,vect,dist=1.0):
		self.x+=vect.x*dist
		self.y+=vect.y*dist
		self.z+=vect.z*dist
	def shader(self,shader):
		self.shader=shader
		self.shad=True
	def event(self):
		glTranslatef(self.x,self.y,self.z)
		self.quat.matrix()
		glScalef(self.w,self.h,self.d)
		if self.mesh.texture:
			glEnable(GL_TEXTURE_2D)
			glBindTexture(GL_TEXTURE_2D,self.tex)
		if self.mesh.normal:
			glEnable(GL_LIGHTING)
		if self.shad:
			self.shader.enable()
		self.mesh.draw()
		if self.shad:
			glUseProgram(0)
		if self.mesh.texture:
			glDisable(GL_TEXTURE_2D)
		if self.mesh.normal:
			glDisable(GL_LIGHTING)