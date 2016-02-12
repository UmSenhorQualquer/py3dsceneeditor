from py3DSceneEditor.Windows.Object.__init__ import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from py3DEngine.objects.PlaneObject import PlaneObject
from py3DSceneEditor.Windows.Object.ObjectWindow import ObjectWindow


class PlaneWindow(ObjectWindow, PlaneObject):
	
	def __init__(self, parent=None):
		ObjectWindow.__init__(self, parent)
		PlaneObject.__init__(self)

		self._maskField = ControlFile('Mask file', self.maskimg )
		self._width = ControlText('Width', str(self.objwidth) )
		self._height = ControlText('Height', str(self.objheight) )

		self._formset = [ '_activeField',
			'_objectName','_colorField',
			'_centerOfMassField',
			'_positionField','_rotationField',
			'_width','_height','_maskField', '_refractionField',' ']

		self._width.changed = self.__widthChanged
		self._maskField.changed = self.__maskChanged
		self._height.changed = self.__heightChanged

		self.initForm()

	def __maskChanged(self): 
		if self._maskField.value!='':
			self.maskimg = self._maskField.value
		else:
			self.maskimg = None
		self._parent.repaint()

	def __widthChanged(self): 
		self.objwidth = eval(self._width.value)
		self._parent.repaint()

	def __heightChanged(self): 
		self.objheight = eval(self._height.value)
		self._parent.repaint()

	def afterLoadSceneObject(self):
		super(PlaneWindow, self).afterLoadSceneObject()
		self._width.value 				= str(self.objwidth)
		self._height.value 				= str(self.objheight)
		self._maskField.value 			= str(self.maskimg)

	"""
	@property
	def wavefrontobject(self): return super(PlaneWindow, self).wavefrontobject

	@wavefrontobject.setter
	def wavefrontobject(self, value):
		PlaneObject.wavefrontobject.fset(self, value)
		
		self._objectName.value 	= self.name
		self._colorField.value 	= str(self.color)
		self._height.value 		= str(value.getProperty('height','1'))
		
		self._width.value 		= str(value.getProperty('width','1'))
		self._maskField.value 	= value.getProperty('mask file','')
	"""
	
##################################################################################################################
##################################################################################################################
##################################################################################################################

if __name__ == "__main__":	 app.startApp( PlaneWindow )
	
