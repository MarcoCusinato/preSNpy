class Grid:
	def __init__(self, name, axis, unit=None):
		from numpy import array
		from ..physics.physarray import PhysArray

		if isinstance(axis, list):
			axis = array(axis)

		if unit is not None:
			axis = PhysArray(axis, unit=unit)

		if axis.ndim != 1:
			raise ValueError('Grid must be 1-dimensional')
		
		self.name = name
		self.axis = axis
	'''
	def fillGrid(self):
		self.radius = self.parent.file['xzn'][:]
		self.mass = self.parent.file['mass'][:]
		self.bar_mass = self.parent.file['massb'][:]
		self.grav_mass = self.parent.file['massg'][:]
		if self.dim > 1:
			self.theta = self.parent.file['theta'][:]
			if self.dim > 2:
				self.phi = self.parent.file['phi'][:]	
	'''

class GridList(list):
	def axisNames(self, index):
		return self[index].name
	
	def hasAxis(self, name):
		try:
			self[name]
			return True
		except:
			return False