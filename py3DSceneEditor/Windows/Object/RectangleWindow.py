from py3DSceneEditor.Windows.Object.__init__ import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from py3dengine.objects.RectangleObject 	import RectangleObject
from py3DSceneEditor.Windows.Object.ObjectWindow import ObjectWindow


class RectangleWindow(ObjectWindow, RectangleObject):
	
	def __init__(self, parent=None):
		ObjectWindow.__init__(self, parent)
		RectangleObject.__init__(self)

		self._p0 = ControlText('Point 0', str(self.point0) )
		self._p1 = ControlText('Point 1', str(self.point1) )
		self._p2 = ControlText('Point 2', str(self.point2) )
		self._p3 = ControlText('Point 3', str(self.point3) )

		self._formset = [ '_parent_obj', '_objectName','_colorField','_p0','_p1','_p2','_p3', '_refractionField', ' ']

		self._p0.changed_event = self.__point0Changed
		self._p1.changed_event = self.__point1Changed
		self._p2.changed_event = self.__point2Changed
		self._p3.changed_event = self.__point3Changed

		self.init_form()

	def __point0Changed(self): 
		try:
			self.point0 = eval(self._p0.value)
			self._parent.calculateCollisions()
		except:
			pass

	def __point1Changed(self): 
		try:
			self.point1 = eval(self._p1.value)
			self._parent.calculateCollisions()
		except:
			pass

	def __point2Changed(self): 
		try:
			self.point2 = eval(self._p2.value)
			self._parent.calculateCollisions()
		except:
			pass

	def __point3Changed(self): 
		try:
			self.point3 = eval(self._p3.value)
			self._parent.calculateCollisions()
		except:
			pass



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

if __name__ == "__main__":	 app.start_app( RectangleWindow )
	
