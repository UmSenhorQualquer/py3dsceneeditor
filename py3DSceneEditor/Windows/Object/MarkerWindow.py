from py3DSceneEditor.Windows.Object.__init__ import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from py3dengine.objects.MarkerObject 	import MarkerObject
from py3DSceneEditor.Windows.Object.ObjectWindow import ObjectWindow


class MarkerWindow(ObjectWindow, MarkerObject):
	
	def __init__(self, parent=None):
		ObjectWindow.__init__(self, parent)
		MarkerObject.__init__(self)

		self._p0 = ControlText('Point 0', str(self.point0) )
		self._p1 = ControlText('Point 1', str(self.point1) )
		self._p2 = ControlText('Point 2', str(self.point2) )
		self._p3 = ControlText('Point 3', str(self.point3) )
		self._p4 = ControlText('Point 4', str(self.point4) )

		self._formset = [ '_parent_obj', '_objectName','_colorField','_p0','_p1','_p2','_p3','_p4',' ']

		self._p0.changed_event = self.__point0Changed
		self._p1.changed_event = self.__point1Changed
		self._p2.changed_event = self.__point2Changed
		self._p3.changed_event = self.__point3Changed
		self._p4.changed_event = self.__point4Changed

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

	def __point3Changed(self): 
		try:
			self.point3 = eval(self._p3.value)
			self._parent.repaint()
		except:
			pass

	def __point4Changed(self):
		try:
			self.point4 = eval(self._p4.value)
			self._parent.repaint()
		except:
			pass


	@property
	def wavefrontobject(self): return super(MarkerWindow, self).wavefrontobject

	@wavefrontobject.setter
	def wavefrontobject(self, value):
		MarkerObject.wavefrontobject.fset(self, value)
		self._objectName.value = self.name
		self._colorField.value = str(self.color)
		self._p0.value = str(self.point0)
		self._p1.value = str(self.point1)
		self._p2.value = str(self.point2)
		self._p3.value = str(self.point3)
		self._p4.value = str(self.point4)
	
##################################################################################################################
##################################################################################################################
##################################################################################################################

if __name__ == "__main__":	 app.start_app( TriangleWindow )
	
