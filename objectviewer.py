import engine,os,pygame,math,sys
from copy import copy,deepcopy
from OpenGL.GL import *
from OpenGL.GLU import *
camx,camy,camz,camquat=0.0,0.0,0.0,engine.Matrix.Quaternion()
win=engine.Window(800,600)
def normal(x1,y1,z1,x2,y2,z2,x3,y3,z3):
	ax,ay,az=x1-x2,y1-y2,z1-z2
	bx,by,bz=x2-x3,y2-y3,z2-z3
	nx,ny,nz=ay*bz-az*by,az*bx-ax*bz,ax*by-ay*bx
	ds=math.sqrt(nx**2+ny**2+nz**2)
	return nx/ds,ny/ds,nz/ds
def read(file):
	f=open(file,"r")
	s=""
	for i in f:
		s+=i
	f.close()
	return s
def export_list(file,lst):
	pass
def import_list(file):
	s=read(file)
	lst=[]
	ln={}
	lex=[]
	k=""
	prev=""
	for i in s:
		if i==" ":
			lex.append(k)
			k=""
		elif i=="\n":
			if prev=="\n":
				lst.append(deepcopy(ln))
				ln={}
			else:
				lex.append(k)
				k=""
				ln[lex[0]]=lex[1:]
				lex=[]
		else:
			k+=i
		prev=i
	return lst
def import_types(file):
	typ=import_list(file)
	types={}
	for i in typ:
		name=i['name'][0]
		types[name]={}
		if 'texture' in i:
			if i['texture'][1]=="smooth":
				types[name]['texture']=engine.Texture.smooth(i['texture'][0])
		if 'mesh' in i:
			types[name]['mesh']=engine.Mesh()
			types[name]['mesh'].loadObj(i['mesh'][0])
		if 'shader' in i:
			types[name]['shader']=i['shader'][0]
	return types
def import_objects(file,types,shader={}):
	obj=import_list(file)
	for i in obj:
		object=engine.Model()
		type=i['type'][0]
		if 'mesh' in types[type]:
			object.mesh=types[type]['mesh']
		if 'texture' in types[type]:
			object.texture(types[type]['texture'])
		if 'shader' in types[type]:
			object.shader(shader[types[type]['shader']])
		if 'x' in i:
			object.x=float(i['x'][0])
		if 'y' in i:
			object.y=float(i['y'][0])
		if 'z' in i:
			object.z=float(i['z'][0])
		if 'w' in i:
			object.w=float(i['w'][0])
		if 'h' in i:
			object.h=float(i['h'][0])
		if 'd' in i:
			object.d=float(i['d'][0])
		win.addObject(object)
def import_shaders(file):
	shader={}
	shd=import_list(file)
	for i in shd:
		name=i['name'][0]
		shad=engine.Shader()
		if 'vertex' in i:
			s=read(i['vertex'][0])
			shad.vertex(s)
		if 'fragment' in i:
			s=read(i['fragment'][0])
			shad.fragment(s)
		shad.compile()
		shader[name]=shad
	return shader
shader=import_shaders("shaders.list")
types=import_types("types.list")
import_objects("objects.list",types,shader)
mx,my=0,0
def draw():
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	win.quat.matrix()
	glTranslatef(-win.x,-win.y,-win.z)
	glLightfv(GL_LIGHT0, GL_POSITION,[1.0,1.0,1.0,0.0])
	for i in win.obj:
		glPushMatrix()
		i.event()
		glPopMatrix()
	glViewport(0,0,win.w,win.h)
def event():
	global mx,my
	if win.mouse[0][1] or win.mouse[2][1]:
		mx,my=win.mousex,win.mousey
	if win.mouse[0][0]:
		win.move(win.quat.invert().rotatevect(engine.Matrix.Vector(win.mousex-mx,my-win.mousey,0.0)),win.timedelta)
		win.mousesetpos(mx,my)
	if win.mouse[2][0]:
		win.rotate((mx-win.mousex)*win.timedelta,0.0,1.0,0.0)
		win.rotate((my-win.mousey)*win.timedelta,1.0,0.0,0.0)
		win.mousesetpos(mx,my)
	if win.mouse[4][1]:
		win.move(win.quat.invert().rotatevect(engine.Matrix.Vector(0.0,0.0,1.0)),1.0)
	if win.mouse[3][1]:
		win.move(win.quat.invert().rotatevect(engine.Matrix.Vector(0.0,0.0,-1.0)),1.0)
win.event=event
win.draw=draw
win.loop()