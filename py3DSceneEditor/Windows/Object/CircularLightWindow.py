from py3DSceneEditor.Windows.Object.__init__ import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from py3dengine.objects.CircularLightObject import CircularLightObject
from .CircleWindow import CircleWindow
from py3DSceneEditor.Windows.Object.ObjectWindow import ObjectWindow


class CircularLightWindow(CircleWindow, CircularLightObject):

	FORMSET = ['_parent_obj', '_objectName',
			   '_positionField',
			   '_colorField', '_faControl', '_fbControl',
			   '_focal_point', '_rays_step', '_calculate_rays_btn', '_collide_rays_btn', ' ']

	def __init__(self, parent=None):
		ObjectWindow.__init__(self, parent)
		CircularLightObject.__init__(self)

		self._calculate_rays_btn = ControlButton('Calculate rays', default=self.calculate_rays)
		self._collide_rays_btn = ControlButton('Collide rays', default=self.collide_rays_evt)

		self._focal_point = ControlText('Focal point', default='-1')
		self._rays_step = ControlText('Rays step', default='1.0')

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

	def collide_rays_evt(self):
		for r in self.rays:
			r.collide( self._parent.objects )

	@property
	def wavefrontobject(self): return super(CircularLightObject, self).wavefrontobject

	@wavefrontobject.setter
	def wavefrontobject(self, value):
		CircularLightObject.wavefrontobject.fset(self, value)
		self._objectName.value = self.name
		self._colorField.value = [self.color]
		self._faControl.value = str(self.fA)
		self._fbControl.value = str(self.fB)


##################################################################################################################
##################################################################################################################
##################################################################################################################

if __name__ == "__main__":	 app.start_app( CircularLightWindow )
	
