from __init__ import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from py3DEngine.objects.RectangleObject 	import RectangleObject
from py3DSceneEditor.Windows.Object.ObjectWindow import ObjectWindow


class RectangleWindow(ObjectWindow, RectangleObject):
	
	def __init__(self, parent=None):
		ObjectWindow.__init__(self, parent)
		RectangleObject.__init__(self)

		self._p0 = ControlText('Point 0', str(self.point0) )
		self._p1 = ControlText('Point 1', str(self.point1) )
		self._p2 = ControlText('Point 2', str(self.point2) )
		self._p3 = ControlText('Point 3', str(self.point3) )

		self._formset = [ '_objectName','_colorField','_p0','_p1','_p2','_p3', '_refractionField', ' ']

		self._p0.changed = self.__point0Changed
		self._p1.changed = self.__point1Changed
		self._p2.changed = self.__point2Changed
		self._p3.changed = self.__point3Changed

		self.initForm()

	def __point0Changed(self): 
		self.point0 = eval(self._p0.value)
		self._parent.calculateCollisions()

	def __point1Changed(self): 
		self.point1 = eval(self._p1.value)
		self._parent.calculateCollisions()

	def __point2Changed(self): 
		self.point2 = eval(self._p2.value)
		self._parent.calculateCollisions()

	def __point3Changed(self): 
		self.point3 = eval(self._p3.value)
		self._parent.calculateCollisions()



	@property
	def wavefrontobject(self): return super(RectangleWindow, self).wavefrontobject

	@wavefrontobject.setter
	def wavefrontobject(self, value):
		RectangleObject.wavefrontobject.fset(self, value)
		self._objectName.value = self.name
		self._colorField.value = str(self.color)
		self._p0.value = str(self.point0)
		self._p1.value = str(self.point1)
		self._p2.value = str(self.point2)
		self._p3.value = str(self.point3)

##################################################################################################################
##################################################################################################################
##################################################################################################################

if __name__ == "__main__":	 app.startApp( RectangleWindow )
	
