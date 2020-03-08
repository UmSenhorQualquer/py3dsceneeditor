from py3DSceneEditor.Windows.Object.__init__ import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from py3dengine.objects.TriangleObject import TriangleObject
from py3DSceneEditor.Windows.Object.ObjectWindow import ObjectWindow


class TriangleWindow(ObjectWindow, TriangleObject):
	
	def __init__(self, parent=None):
		ObjectWindow.__init__(self, parent)
		TriangleObject.__init__(self)

		self._p0 = ControlText('Point 0', str(self.point0) )
		self._p1 = ControlText('Point 1', str(self.point1) )
		self._p2 = ControlText('Point 2', str(self.point2) )

		self._formset = [ '_parent_obj', '_objectName','_colorField','_p0','_p1','_p2',' ']

		self._p0.changed_event = self.__point0Changed
		self._p1.changed_event = self.__point1Changed
		self._p2.changed_event = self.__point2Changed

		self.init_form()

	def __point0Changed(self): 
		try:
			self.point0 = eval(self._p0.value)
			self._parent.repaint()
		except:
			pass

	def __point1Changed(self): 
		try:
			self.point1 = eval(self._p1.value)
			self._parent.repaint()
		except:
			pass

	def __point2Changed(self): 
		try:
			self.point2 = eval(self._p2.value)
			self._parent.repaint()
		except:
			pass

	@property
	def wavefrontobject(self): return super(TriangleWindow, self).wavefrontobject

	@wavefrontobject.setter
	def wavefrontobject(self, value):
		TriangleObject.wavefrontobject.fset(self, value)
		self._objectName.value = self.name
		self._colorField.value = [self.color]
		self._p0.value = str(self.point0)
		self._p1.value = str(self.point1)
		self._p2.value = str(self.point2)
	
##################################################################################################################
##################################################################################################################
##################################################################################################################

if __name__ == "__main__":	 app.start_app( TriangleWindow )
	
