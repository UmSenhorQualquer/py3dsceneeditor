from py3DSceneEditor.Windows.Object.__init__ import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from py3dengine.objects.ellipsoid import EllipsoidObject
from py3DSceneEditor.Windows.Object.ObjectWindow import ObjectWindow


class EllipsoidWindow(ObjectWindow, EllipsoidObject):
	
	def __init__(self, parent=None):
		ObjectWindow.__init__(self, parent)
		EllipsoidObject.__init__(self)


		self._faControl = ControlText('A', str(self.fA) )
		self._fbControl = ControlText('B', str(self.fB) )
		self._fcControl = ControlText('C', str(self.fC) )

		self._formset = [ '_parent_obj', '_activeField',
			'_objectName','_colorField',
			'_positionField','_rotationField', '_center_of_massField',
			'_faControl','_fbControl','_fcControl', ' ']

		self._faControl.changed_event = self.__faControlChanged
		self._fbControl.changed_event = self.__fbControlChanged
		self._fcControl.changed_event = self.__fcControlChanged

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

	def __fcControlChanged(self): 
		try:
			self.fC = eval(self._fcControl.value)
			self._parent.repaint()
		except:
			pass


	def after_load_scene_object(self):
		super(EllipsoidWindow, self).after_load_scene_object()
		self._faControl.value = str(self.fA)
		self._fbControl.value = str(self.fB)
		self._fcControl.value = str(self.fC)
	
##################################################################################################################
##################################################################################################################
##################################################################################################################

if __name__ == "__main__":	 app.start_app( EllipsoidWindow )
	
