# -*- coding: utf-8 -*-
import cairo
import math

class Group:
	def __init__(self):
		self.children = []
		self.dx = 0
		self.dy = 0
		
		self.group = True
	
	def translate(self, dx, dy):
		self.dx, self.dy = (dx, dy)
		for child in filter(lambda c: c.group, self.children):
			child.dx = self.dx
			child.dy = self.dy
		print "translate!",dx,dy
	
	def add_child(self, child, something=None):
		self.children.append(child)
		child.parent = self
		
		if child.group:
			child.dx = self.dx
			child.dy = self.dy
	
	def find_child(self, item):
		return self.children.index(item)
	
	def remove_child(self, index):
		del self.children[index]
	
	def set_simple_transform(self, x, y, scale, rotation):
		self.dx = x
		self.dy = y
		for child in filter(lambda c: c.group, self.children):
			child.dx = self.dx
			child.dy = self.dy
		self.transform = (x, y, scale, rotation)
		print "transform!", x, y, scale, rotation
	
	def render(self, context):
		for child in self.children:
			child.render(context)

class Points:
	def __init__(self, points):
		self.points = points

class Ellipse:
	def __init__(self):
		pass

class TextProps:
	anchor = None

class gtk:
	ANCHOR_SW = 0
	ANCHOR_NORTH = 1
	ANCHOR_EAST = 2
	ANCHOR_SOUTH = 3

class gobject:
	SIGNAL_RUN_LAST = None
	TYPE_NONE = None
	TYPE_PYOBJECT = None
	

class Text:
	def __init__(self, **kwargs):
		self.args = kwargs
		self.props = TextProps()
		self.group = False
		self.rotation = 0
	
	def get_parent(self):
		return self.parent
	
	def render(self, context):
		if self.rotation==0:
			x = self.props.x+self.parent.dx
			y = self.props.y+self.parent.dy
		else:
			x = self.props.y+self.parent.dx
			y = -1*self.props.x+self.parent.dy
		text = self.args["text"]
		
		x_bearing, y_bearing, width, height, x_advance, y_advance = context.text_extents(text)
		if self.rotation==0:
			if self.props.anchor == gtk.ANCHOR_SW:
				pass
			elif self.props.anchor == gtk.ANCHOR_NORTH:
				x -= (width)/2
				y += height
			elif self.props.anchor == gtk.ANCHOR_EAST:
				x -= width
				y += (height)/2
			elif self.props.anchor == gtk.ANCHOR_SOUTH:
				x -= width/2
				y -= height
		else:
			if self.props.anchor == gtk.ANCHOR_SOUTH:
				x -= height
				y += width/2
		
		context.move_to(x, y)
		context.rotate(self.rotation)
		context.show_text(text)
		context.rotate(-1*self.rotation)
	
	def rotate(self, deg, x, y):
		self.rotation = deg/360.0*2*math.pi

class Rect:
	pass

class MoreProps:
	def __init__(self):
		self.points = []
		self.stroke_color = "#000000000000"
		self.line_dash = None

class Polyline:
	def __init__(self, **kwargs):
		self.props = MoreProps()
		if "points" in kwargs:
			self.props.points = kwargs["points"]
		self.group = False
		if "parent" in kwargs:
			kwargs["parent"].add_child(self)
	
	def get_parent(self):
		return self.parent
	
	def render(self, context):
		if self.props.line_dash != None:
			context.set_dash(self.props.line_dash.dashes)
		else:
			context.set_dash([])
		points = map(lambda (x,y): (x+self.parent.dx, y+self.parent.dy), self.props.points.points)
		context.new_path()
		context.move_to(points[0][0], points[0][1])
		for x,y in points[1:]:
			context.line_to(x,y)
		c = self.props.stroke_color[1:]
		if len(c) == 12:
			r = int(c[:4],16)
			g = int(c[4:8],16)
			b = int(c[8:],16)
			context.set_source_rgb(*map(lambda x: float(x)/16**4,(r,g,b)))
		elif len(c) == 6:
			r = int(c[:2],16)
			g = int(c[2:4],16)
			b = int(c[4:],16)
			context.set_source_rgb(*map(lambda x: float(x)/16**2,(r,g,b)))
		context.stroke()

class LineDash:
	def __init__(self, dashes):
		self.dashes = dashes

class Props:
	anchor = None

class Canvas:
	def __init__(self,**kwargs):
		print kwargs
		self.root = Group()
		self.bounds = None
	
	def connect(self, signal, f):
		pass
	
	def set_bounds(self, left, top, right, bottom):
		self.bounds = (left, top, right, bottom)
	
	def get_bounds(self):
		if self.bounds == None:
			return (-1, -1, -1, -1)
		else:
			return self.bounds
	
	def get_root_item(self):
		return self.root
	
	def show(self):
		pass
		
	def render(self, context, something, somethingelse):
		context.set_font_size(15.0)
		self.root.render(context)
	
	props = Props

def polyline_new_line(parent,x1,y1,x2,y2):
	return Polyline(parent=parent,points=[(x1,x2),(y1,y2)])
