from .physarray import PhysArray
import numpy as np

class Hydro:
	def __init__(self, parent, grid):
		self.parent = parent
		self.grid = grid

	def updateGrid(self, grid):
		self.grid = grid
		
	def fillHydro(self, filename, type):
		if type == 'postbounce':
			data = np.genfromtxt(filename, skip_header=6, max_rows=self.parent.nx, \
														usecols=(5,6,7,9,10,11), unpack=True)
			
			setattr(self, 'density', PhysArray(data[1], unit='g/cm^3', \
																			grid=self.grid))
			setattr(self, 'pressure', PhysArray(data[4], unit='erg/cm^3', \
																			 grid=self.grid))
			setattr(self, 'temperature', PhysArray(data[2]*11604525006.17, unit='K',\
														grid=self.grid))
			setattr(self, 'entropy', PhysArray(data[3], unit='k_B', grid=self.grid))
			setattr(self, 'velocity', PhysArray(data[0], unit='cm/s', \
																			 grid=self.grid))
			setattr(self, 'energy', PhysArray(data[5], unit='erg/g', grid=self.grid))
		
		elif type == 'kepler':
			data = filename
			setattr(self, 'density', PhysArray(data['cell density'].astype(float).fillna(0.0).values[:],
                                      unit='g/cm^3', grid=self.grid))
			setattr(self, 'pressure', PhysArray(data['cell pressure'].astype(float).fillna(0.0).values[:],
                                       unit='erg/cm^3', grid=self.grid))
			setattr(self, 'temperature', PhysArray(data['cell temperature'].astype(float).fillna(0.0).values[:],
                                          unit='K', grid=self.grid))
			setattr(self, 'entropy', PhysArray(data['cell specific entropy'].astype(float).fillna(0.0).values[:],
                                      unit='k_B', grid=self.grid))
			setattr(self, 'velocity', PhysArray(data['cell outer velocity'].astype(float).fillna(0.0).values[:],
                                       unit='cm/s', grid=self.grid))
			if 'cell specific energy' in data.keys():
				setattr(self, 'energy', PhysArray(data['cell specific energy'].astype(float).fillna(0.0).values[:],
                                     unit='erg/g', grid=self.grid))
			elif 'cell spec. int. energy' in data.keys():
				setattr(self, 'energy', PhysArray(data['cell spec. int. energy'].astype(float).fillna(0.0).values[:],
																		 unit='erg/g', grid=self.grid))
			setattr(self, 'omega', PhysArray(data['cell angular velocity'].astype(float).fillna(0.0).values[:],
                                    unit='rad/s', grid=self.grid))
		elif type == 'mesa':
			data = filename
			setattr(self, 'density', PhysArray(10 ** data['logRho'].values[:],
                                      unit='g/cm^3', grid=self.grid))
			setattr(self, 'pressure', PhysArray(10 ** data['logP'].values[:],
                                       unit='erg/cm^3', grid=self.grid))
			setattr(self, 'temperature', PhysArray(10 ** data['logT'].astype(float).fillna(0.0).values[:],
                                          unit='K', grid=self.grid))
			setattr(self, 'entropy', PhysArray(data['entropy'].values[:],
                                      unit='k_B', grid=self.grid))
			setattr(self, 'velocity', PhysArray(data['velocity'].values[:],
                                       unit='cm/s', grid=self.grid))
			if 'energy' in data.keys():
				setattr(self, 'energy', PhysArray(data['energy'].values[:],
                                     unit='erg/g', grid=self.grid))
			setattr(self, 'omega', PhysArray(data['omega'].values[:],
                                    unit='rad/s', grid=self.grid))


	def rhor3(self):
		return PhysArray(self.density * (self.density.grid[0].axis**3), unit='g', \
											grid=self.grid)