from __init__ import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from py3DEngine.objects.EllipsoidObject import EllipsoidObject
from py3DSceneEditor.Windows.Object.ObjectWindow import ObjectWindow


class EllipsoidWindow(ObjectWindow, EllipsoidObject):
	
	def __init__(self, parent=None):
		ObjectWindow.__init__(self, parent)
		EllipsoidObject.__init__(self)


		self._faControl = ControlText('A', str(self.fA) )
		self._fbControl = ControlText('B', str(self.fB) )
		self._fcControl = ControlText('C', str(self.fC) )

		self._formset = [ '_activeField',
			'_objectName','_colorField',
			'_positionField','_rotationField', '_centerOfMassField',
			'_faControl','_fbControl','_fcControl', ' ']

		self._faControl.changed = self.__faControlChanged
		self._fbControl.changed = self.__fbControlChanged
		self._fcControl.changed = self.__fcControlChanged

		self.initForm()

	def __faControlChanged(self): 
		self.fA = eval(self._faControl.value)
		self._parent.repaint()

	def __fbControlChanged(self): 
		self.fB = eval(self._fbControl.value)
		self._parent.repaint()

	def __fcControlChanged(self): 
		self.fC = eval(self._fcControl.value)
		self._parent.repaint()


	def afterLoadSceneObject(self):
		super(EllipsoidWindow, self).afterLoadSceneObject()
		self._faControl.value = str(self.fA)
		self._fbControl.value = str(self.fB)
		self._fcControl.value = str(self.fC)
	
##################################################################################################################
##################################################################################################################
##################################################################################################################

if __name__ == "__main__":	 app.startApp( EllipsoidWindow )
	
