from py3DSceneEditor.Windows.Object.__init__ import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

from py3dengine.objects.RectangleObject 	import RectangleObject
from py3DSceneEditor.Windows.Object.ObjectWindow import ObjectWindow


class RectangleWindow(ObjectWindow, RectangleObject):
	
	def __init__(self, parent=None):
		ObjectWindow.__init__(self, parent)
		RectangleObject.__init__(self)


		self._p0 =  ControlList('Point 0', default=[[self.point0]],
					   horizontal_headers=['X', 'Y', 'Z'],
					   resizecolumns=False, height=85)

		self._p1 = ControlList('Point 1', default=[[self.point1]],
							   horizontal_headers=['X', 'Y', 'Z'],
							   resizecolumns=False, height=85)

		self._p2 = ControlList('Point 2', default=[[self.point2]],
							   horizontal_headers=['X', 'Y', 'Z'],
							   resizecolumns=False, height=85)

		self._p3 = ControlList('Point 3', default=[[self.point3]],
							   horizontal_headers=['X', 'Y', 'Z'],
							   resizecolumns=False, height=85)

		self._formset = [ '_parent_obj', '_objectName','_colorField','_p0','_p1','_p2','_p3', '_refractionField', ' ']

		self._p0.changed_event = self.__point0Changed
		self._p1.changed_event = self.__point1Changed
		self._p2.changed_event = self.__point2Changed
		self._p3.changed_event = self.__point3Changed

		self.init_form()

	def __point0Changed(self): 
		try:
			self.point0 = np.array(self._p0.value[0], dtype=np.float)
			self._parent.calculateCollisions()
		except:
			pass

	def __point1Changed(self): 
		try:
			self.point1 = np.array(self._p1.value[0], dtype=np.float)
			self._parent.calculateCollisions()
		except:
			pass

	def __point2Changed(self): 
		try:
			self.point2 = np.array(self._p2.value[0], dtype=np.float)
			self._parent.calculateCollisions()
		except:
			pass

	def __point3Changed(self): 
		try:
			self.point3 = np.array(self._p3.value[0], dtype=np.float)
			self._parent.calculateCollisions()
		except:
			pass



	@property
	def wavefrontobject(self): return super(RectangleWindow, self).wavefrontobject

	@wavefrontobject.setter
	def wavefrontobject(self, value):
		RectangleObject.wavefrontobject.fset(self, value)
		self._objectName.value = self.name
		self._colorField.value = [self.color]
		self._p0.value = [self.point0]
		self._p1.value = [self.point1]
		self._p2.value = [self.point2]
		self._p3.value = [self.point3]

##################################################################################################################
##################################################################################################################
##################################################################################################################

if __name__ == "__main__":	 app.start_app( RectangleWindow )
	
