import math
from OpenGL.GL import glMultMatrixd
class Vector:
	def __init__(self,x,y,z):
		self.x=x
		self.y=y
		self.z=z
	def angle(a,b):
		try:
			return math.acos((a.x*b.x+a.y*b.y+a.z*b.z)/a.len()/b.len())
		except Exception:
			return 0
	def normalize(self):
		d=math.sqrt(self.x**2+self.y**2+self.z**2)
		if d!=0:
			self.x/=d
			self.y/=d
			self.z/=d
		return self
	def __add__(a,b):
		x = a.x + b.x
		y = a.y + b.y
		z = a.z + b.z
		return Vector(x,y,z)
	def mul(a,b):
		x = a.x * b
		y = a.y * b
		z = a.z * b
		return Vector(x,y,z)
	def __mul__(a,b):
		return a.x*b.x+a.y*b.y
	def len(a):
		return math.sqrt(a.x**2+a.y**2+a.z**2)
	def average(a,b,c=0.5):
		x = a.x * (1.0 - c) + b.x * c
		y = a.y * (1.0 - c) + b.y * c
		z = a.z * (1.0 - c) + b.z * c
		return Vector(x,y,z)
def normal(x1,y1,z1,x2,y2,z2,x3,y3,z3):
	ax,ay,az=x1-x2,y1-y2,z1-z2
	bx,by,bz=x2-x3,y2-y3,z2-z3
	nx,ny,nz=ay*bz-az*by,az*bx-ax*bz,ax*by-ay*bx
	ds=math.sqrt(nx**2+ny**2+nz**2)
	return nx/ds,ny/ds,nz/ds
def normalsum(*norm):
	x,y,z=0.0,0.0,0.0
	for i in norm:
		x+=i[0]
		y+=i[1]
		z+=i[2]
	mx=max(x,y,z)
	x/=mx
	y/=mx
	z/=mx
	return x,y,z

class Quaternion:
	def __init__(self,w=0.0,x=0.0,y=0.0,z=0.0):
		self.w,self.x,self.y,self.z=w,x,y,z
	def empty(self):
		self.w,self.x,self.y,self.z=1.0,0.0,0.0,0.0
		return self
	def angle(self,angle,vect):
		return Quaternion(math.cos(angle/2.0),vect.x*math.sin(angle/2.0),vect.y*math.sin(angle/2.0),vect.z*math.sin(angle/2.0))
	def normal(self):
		d=math.sqrt(self.x**2+self.y**2+self.z**2)
		return Quaternion(self.w,self.x/d,self.y/d,self.z/d)
	def invert(self):
		return Quaternion(self.w,-self.x,-self.y,-self.z)
	def scale(self,val):
		return Quaternion(self.w*val,self.x*val,self.y*val,self.z*val)
	def __add__(a,b):
		w = a.w + b.w
		x = a.x + b.x
		y = a.y + b.y
		z = a.z + b.z
		return Quaternion(w,x,y,z)
	def __mul__(a,b):
		w = a.w * b.w - a.x * b.x - a.y * b.y - a.z * b.z
		x = a.w * b.x + a.x * b.w + a.y * b.z - a.z * b.y
		y = a.w * b.y - a.x * b.z + a.y * b.w + a.z * b.x
		z = a.w * b.z + a.x * b.y - a.y * b.x + a.z * b.w
		return Quaternion(w,x,y,z)
	def mulvect(a,b):
		w = -a.x * b.x - a.y * b.y - a.z * b.z
		x = a.w * b.x + a.y * b.z - a.z * b.y
		y = a.w * b.y - a.x * b.z + a.z * b.x
		z = a.w * b.z + a.x * b.y - a.y * b.x
		return Quaternion(w,x,y,z)
	def rotatevect(a,b):
		t = a.mulvect(b)*a.invert()
		return Vector(t.x,t.y,t.z)
	def matrix(m):
		data=[1.0 - 2.0 * ( m.y * m.y + m.z * m.z ),
		2.0 * (m.x * m.y + m.z * m.w),
		2.0 * (m.x * m.z - m.y * m.w),
		0.0,
		
		2.0 * ( m.x * m.y - m.z*m.w),
		1.0 - 2.0*(m.x* m.x + m.z * m.z ),
		2.0 * (m.z * m.y + m.x * m.w ),
		0.0,

		2.0 * ( m.x * m.z + m.y * m.w ),
		2.0 * ( m.y * m.z - m.x * m.w ),
		1.0 - 2.0 * ( m.x * m.x + m.y * m.y ),
		0.0,

		0,
		0,
		0,
		1.0]
		glMultMatrixd(data)