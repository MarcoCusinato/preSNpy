import h5py
import numpy as np
from ..geometry import grid
from ..physics import hydro
from ..physics import nuclear
from .. import global_vars as gv

class Postbounce1D:
	def __init__(self, filename):
		'''
		 Postbounce profile data 1D
		'''
		self.filename = filename
		self.file = h5py.File(gv.SNMODELS_DIR + filename, 'r')
		self.ndim = 1

		self.grid = grid.GridList()
		self.grid.append(grid.Grid('radius', self.file['xzn'][:], unit='cm'))
		self.grid.append(grid.Grid('mass', self.file['massb'][:], unit='Msun'))


		# Initialize SCALAR quantities
		self.nx = self.file['nx'][()]
		self.nuc_ad = self.file['nnuc_ad'][()]
		self.pmass = self.file['pmass'][()]
		self.pmbar = self.file['pmbar'][()]
		self.pmgrv = self.file['pmgrv'][()]

		# Initialize GRID quantities
		#self.grid = grid.Grid(self, 1)
		#self.grid.fillGrid()

		# Initialize HYDRO quantities
		self.hydro = hydro.Hydro(self)
		self.hydro.fillHydro(self.grid)

		# Initialize NUCLEAR quantities
		self.nuclear = nuclear.Nuclear(self)
		self.nuclear.fillNuclear(self.grid)
	
	def starMass(self):
		'''
			Return the mass of the star.
		'''
		return self.grid[1].axis[-1]

	def starRadius(self):
		'''
			Return the radius of the star.
		'''
		return self.grid[0].axis[-1]
	
	def compactness(self, masslim=2.5):
		'''
			Return the compactness of the star.
			The compactness is defined as the ratio between the enclosed mass 
			'masslim' (in unit of Msun) and the radius that encloses that mass 
			(in unit of 1000 km).

			Reference: O'Connor & Ott (2011)
		'''
		idx = np.argmin(np.fabs(self.grid.getAxis('mass') - masslim))
		rlim = self.grid.getAxis('radius')[idx] / (1.e5) # in km
		xi = masslim / (rlim/1000)
		return xi
	
	def M4(self):
		'''
			Return the mass coordinate where the entropy per kb is 4.
		'''
		idx = np.argmin(np.fabs(self.hydro.entropy - 4))
		return self.grid.getAxis('mass')[idx]

	def ZAMS_mass(self):
		'''
			Return the zero-age main sequence mass of the star (in unit of Msun).
		'''
		s = ''
		spl = self.filename.split('_')
		for sp in spl[0]:
			if sp.isdigit():
				s += sp
		s += '.' + spl[1]
		return float(s)