from py3dengine.objects.RectangularLightObject import RectangularLightObject

from py3DSceneEditor.Windows.Object.RectangleWindow import RectangleWindow
from py3DSceneEditor.Windows.Object.__init__ import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

from py3dengine.objects.RectangleObject 	import RectangleObject
from py3DSceneEditor.Windows.Object.ObjectWindow import ObjectWindow


class RectangularLightWindow(RectangleWindow, RectangularLightObject):
	FORMSET = [
		'_parent_obj', '_objectName','_colorField','_p0','_p1','_p2','_p3', '_refractionField',
		'_focal_point_field', '_rays_step_field', '_calculate_rays_btn', '_collide_rays_btn', ' '
	]

	
	def __init__(self, parent=None):
		self._calculate_rays_btn = ControlButton('Calculate rays', default=self.calculate_rays)
		self._collide_rays_btn = ControlButton('Collide rays', default=self.collide_rays_evt)

		self._focal_point_field = ControlText('Focal point', default='-1')
		self._rays_step_field = ControlText('Rays step', default='1.0')

		RectangleWindow.__init__(self, parent)
		RectangularLightObject.__init__(self)



	def collide_rays_evt(self):
		for r in self.rays:
			r.collide( self._parent.objects )

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
	
