from py3DSceneEditor.Windows.Object.__init__ import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from py3dengine.objects.ellipse import EllipseObject
from py3DSceneEditor.Windows.Object.ObjectWindow import ObjectWindow


class EllipseWindow(ObjectWindow, EllipseObject):
	
	def __init__(self, parent=None):
		ObjectWindow.__init__(self, parent)
		EllipseObject.__init__(self)


		self._faControl = ControlText('A', str(self.fA) )
		self._fbControl = ControlText('B', str(self.fB) )

		self._formset = [ '_parent_obj', '_objectName','_colorField','_faControl','_fbControl',' ']

		self._faControl.changed_event = self.__faControlChanged
		self._fbControl.changed_event = self.__fbControlChanged

		self.init_form()

	def __faControlChanged(self): 
		try:
			self.fA = eval(self._faControl.value)
			self._parent.repaint()
		except:
			pass

	def __fbControlChanged(self):
		try:
			self.fB = eval(self._fbControl.value)
			self._parent.repaint()
		except:
			pass

	@property
	def wavefrontobject(self): return super(EllipseWindow, self).wavefrontobject

	@wavefrontobject.setter
	def wavefrontobject(self, value):
		EllipseObject.wavefrontobject.fset(self, value)
		self._objectName.value = self.name
		self._colorField.value = str(self.color)
		self._faControl.value = str(self.fA)
		self._fbControl.value = str(self.fB)
	
##################################################################################################################
##################################################################################################################
##################################################################################################################

if __name__ == "__main__":	 app.start_app( EllipseWindow )
	
