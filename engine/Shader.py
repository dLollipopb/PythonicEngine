from OpenGL.GL import GL_COMPILE_STATUS,GL_VERTEX_SHADER,GL_FRAGMENT_SHADER,glGetShaderiv,glCreateProgram,glAttachShader,glCreateShader,glShaderSource,glCompileShader,glGetShaderInfoLog,glUseProgram,glLinkProgram
from sys import exit
def _shader(shader_type, source):
	shader = glCreateShader(shader_type)
	glShaderSource(shader, source)
	glCompileShader(shader)
	return shader
def _check_error(shader):
	if not glGetShaderiv(shader, GL_COMPILE_STATUS):
		raise Exception,glGetShaderInfoLog(shader)
class Shader:
	def __init__(self):
		self.svertex=''
		self.sfragment=''
		self.vert=None
		self.frag=None
		self.program = glCreateProgram()
	def vertex(self,s):
		self.svertex=s
		self.vert=_shader(GL_VERTEX_SHADER,self.svertex)
		glAttachShader(self.program,self.vert)
	def fragment(self,s):
		self.sfragment=s
		self.frag=_shader(GL_FRAGMENT_SHADER,self.sfragment)
		glAttachShader(self.program,self.frag)
	def compile(self):
		glLinkProgram(self.program)
		_check_error(self.vert)
		_check_error(self.frag)
	def enable(self):
		glUseProgram(self.program)