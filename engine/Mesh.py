from OpenGL.GL import *
import math,sys
from traceback import format_exc as errstr
def normal(x1,y1,z1,x2,y2,z2,x3,y3,z3):
	ax,ay,az=x1-x2,y1-y2,z1-z2
	bx,by,bz=x2-x3,y2-y3,z2-z3
	nx,ny,nz=ay*bz-az*by,az*bx-ax*bz,ax*by-ay*bx
	ds=math.sqrt(nx**2+ny**2+nz**2)
	return nx/ds,ny/ds,nz/ds
def lexer(s,lx=[" ","\t","\n"],space=False):
	k=""
	lex=[]
	for i in s:
		if i in lx:
			if k!="" or space:
				lex.append(k)
				k=""
		else:
			k+=i
	if k!="" or space:
		lex.append(k)
		k=""
	return lex
def ret_value(s):
	if s=="":
		return 0
	if math.floor(float(s))==float(int(s)):
		return int(s)
	return float(s)
def load_obj(path):
	vertices=[]
	texcoords=[]
	normals=[]
	faces=[]
	f=open(path,"r")
	for i in f:
		l=lexer(i)
		if l[0]=="v":
			vertices.append((float(l[1]),float(l[2]),float(l[3])))
		elif l[0]=="vt":
			texcoords.append((float(l[1]),float(l[2])))
		elif l[0]=="vn":
			normals.append((float(l[1]),float(l[2]),float(l[3])))
		elif l[0]=="f":
			for j in xrange(len(l)-3):
				face=[]
				face.append(map(lambda ii:ret_value(ii)-1,lexer(l[1],["/",],True)))
				face.append(map(lambda ii:ret_value(ii)-1,lexer(l[2+j],["/",],True)))
				face.append(map(lambda ii:ret_value(ii)-1,lexer(l[3+j],["/",],True)))
				faces.append(face)
	return vertices,texcoords,normals,faces
class Mesh:
	def __init__(self,ptype=None,normal=True,texture=True,color=False):
		self.verticesBuffer,self.verticesData=glGenBuffers(1),[]
		if texture:self.textureBuffer,self.textureData=glGenBuffers(1),[]
		if normal:self.normalBuffer,self.normalData=glGenBuffers(1),[]
		if color:self.colorBuffer,self.colorData=glGenBuffers(1),[]
		self.verticesCount=0
		self.ptype=ptype
		self.texture,self.normal,self.color=texture,normal,color
	def clearVbo(self):
		self.verticesData,self.normalData,self.textureData,self.colorData,self.verticesCount=[],[],[],[],0
	def drawVbo(self):
		glBindBuffer(GL_ARRAY_BUFFER,self.verticesBuffer)
		arr=(ctypes.c_float*(self.verticesCount*3))(*self.verticesData)
		glBufferData(GL_ARRAY_BUFFER,self.verticesCount*3*4,arr,GL_STATIC_DRAW)
		if self.texture:
			glBindBuffer(GL_ARRAY_BUFFER,self.textureBuffer)
			arr=(ctypes.c_float*(self.verticesCount*2))(*self.textureData)
			glBufferData(GL_ARRAY_BUFFER, self.verticesCount*2*4,arr,GL_STATIC_DRAW);
		if self.normal:
			glBindBuffer(GL_ARRAY_BUFFER,self.normalBuffer)
			arr=(ctypes.c_float*(self.verticesCount*3))(*self.normalData)
			glBufferData(GL_ARRAY_BUFFER, self.verticesCount*3*4,arr,GL_STATIC_DRAW);
		if self.color:
			glBindBuffer(GL_ARRAY_BUFFER,self.colorBuffer)
			arr=(ctypes.c_ubyte*(self.verticesCount*3))(*self.colorData)
			glBufferData(GL_ARRAY_BUFFER, self.verticesCount*3,arr,GL_STATIC_DRAW);
	def draw(self):
		glBindBuffer(GL_ARRAY_BUFFER,self.verticesBuffer)
		glVertexPointer(3,GL_FLOAT,0,None)
		glEnableClientState(GL_VERTEX_ARRAY)
		if self.texture:
			glBindBuffer(GL_ARRAY_BUFFER,self.textureBuffer)
			glTexCoordPointer(2,GL_FLOAT,0,None)
			glEnableClientState(GL_TEXTURE_COORD_ARRAY)
		if self.normal:
			glBindBuffer(GL_ARRAY_BUFFER,self.normalBuffer)
			glNormalPointer(GL_FLOAT,0,None)
			glEnableClientState(GL_NORMAL_ARRAY)
		if self.color:
			glBindBuffer(GL_ARRAY_BUFFER,self.colorBuffer)
			glColorPointer(3,GL_UNSIGNED_BYTE,0,None)
			glEnableClientState(GL_COLOR_ARRAY)
		glDrawArrays(self.ptype,0,self.verticesCount)
		glDisableClientState(GL_VERTEX_ARRAY)
		if self.texture:glDisableClientState(GL_TEXTURE_COORD_ARRAY)
		if self.normal:glDisableClientState(GL_NORMAL_ARRAY)
		if self.color:glDisableClientState(GL_COLOR_ARRAY)
	def loadObj(self,path,vt=True,vn=True):
		vertices,texcoords,normals,faces=load_obj(path)
		for i in faces:
			self.verticesData+=vertices[i[0][0]]+vertices[i[1][0]]+vertices[i[2][0]]
			if vt:
				self.textureData+=texcoords[i[0][1]]+texcoords[i[1][1]]+texcoords[i[2][1]]
			else:
				self.textureData+=[0.0,0.0,1.0,0.0,0.0,1.0]
			if vn:
				self.normalData+=normals[i[0][2]]+normals[i[1][2]]+normals[i[2][2]]
			else:
				try:
					self.normalData+=normal(*(vertices[i[0][0]]+vertices[i[1][0]]+vertices[i[2][0]]))*3
				except Exception:
					self.normalData+=[0.0,0.0,0.0]*3
			self.verticesCount+=3
		self.ptype=GL_TRIANGLES
		self.drawVbo()