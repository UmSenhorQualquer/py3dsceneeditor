from py3DSceneEditor.Windows.Object.__init__ import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import numpy as np
from py3dengine.objects.point import PointObject
from py3DSceneEditor.Windows.Object.ObjectWindow import ObjectWindow


class PointWindow(ObjectWindow, PointObject):
	
	def __init__(self, parent=None):
		ObjectWindow.__init__(self, parent)
		PointObject.__init__(self)

		self._p0 = ControlList('Point', default=[list(self.point)],
							   horizontal_headers=['X', 'Y', 'Z'],
							   resizecolumns=False, height=85)

		self._formset = [ '_parent_obj', '_objectName','_colorField','_p0',' ']

		self._p0.changed_event = self.__point0Changed
		
		self.init_form()

	def __point0Changed(self): 
		try:
			self.point = np.array(self._p0.value[0], dtype=np.float)
			self._parent.repaint()
		except:
			pass

	@property
	def wavefrontobject(self): return super(PointWindow, self).wavefrontobject

	@wavefrontobject.setter
	def wavefrontobject(self, value):
		PointObject.wavefrontobject.fset(self, value)
		self._objectName.value = self.name
		self._colorField.value = [self.color]
		self._p0.value = [self.point]
	
##################################################################################################################
##################################################################################################################
##################################################################################################################

if __name__ == "__main__":	 app.start_app( PointWindow )
	
