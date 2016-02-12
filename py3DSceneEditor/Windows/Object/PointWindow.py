from py3DSceneEditor.Windows.Object.__init__ import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from py3DEngine.objects.PointObject import PointObject
from py3DSceneEditor.Windows.Object.ObjectWindow import ObjectWindow


class PointWindow(ObjectWindow, PointObject):
	
	def __init__(self, parent=None):
		ObjectWindow.__init__(self, parent)
		PointObject.__init__(self)

		self._p0 = ControlText('Point', str(self.point) )

		self._formset = [ '_objectName','_colorField','_p0',' ']

		self._p0.changed = self.__point0Changed
		
		self.initForm()

	def __point0Changed(self): 
		self.point = eval(self._p0.value)
		self._parent.repaint()

	@property
	def wavefrontobject(self): return super(PointWindow, self).wavefrontobject

	@wavefrontobject.setter
	def wavefrontobject(self, value):
		PointObject.wavefrontobject.fset(self, value)
		self._objectName.value = self.name
		self._colorField.value = str(self.color)
		self._p0.value = str(self.point)
	
##################################################################################################################
##################################################################################################################
##################################################################################################################

if __name__ == "__main__":	 app.startApp( PointWindow )
	
