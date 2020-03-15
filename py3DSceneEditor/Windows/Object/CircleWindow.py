from py3DSceneEditor.Windows.Object.__init__ import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from py3dengine.objects.circle import CircleObject
from py3DSceneEditor.Windows.Object.ObjectWindow import ObjectWindow


class CircleWindow(ObjectWindow, CircleObject):

	FORMSET = [ '_parent_obj', '_objectName',
				'_positionField',
				'_colorField','_faControl','_fbControl',' ']
	
	def __init__(self, parent=None):
		ObjectWindow.__init__(self, parent)
		CircleObject.__init__(self)


		self._faControl = ControlText('A', str(self.fA) )
		self._fbControl = ControlText('B', str(self.fB) )

		self.formset = self.FORMSET

		self._faControl.changed_event = self.__faControlChanged
		self._fbControl.changed_event = self.__fbControlChanged


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
	def wavefrontobject(self): return super(CircleObject, self).wavefrontobject

	@wavefrontobject.setter
	def wavefrontobject(self, value):
		CircleObject.wavefrontobject.fset(self, value)
		self._objectName.value = self.name
		self._colorField.value = [self.color]
		self._faControl.value = str(self.fA)
		self._fbControl.value = str(self.fB)

	@property
	def focal_point(self):
		return float(self._focal_point.value)

	@property
	def rays_step(self):
		return float(self._rays_step.value)
##################################################################################################################
##################################################################################################################
##################################################################################################################

if __name__ == "__main__":	 app.start_app( CircleObject )
	
