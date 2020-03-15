from py3DSceneEditor.Windows.Object.__init__ import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from py3dengine.objects.plane import PlaneObject
from py3DSceneEditor.Windows.Object.ObjectWindow import ObjectWindow


class PlaneWindow(ObjectWindow, PlaneObject):
	
	def __init__(self, parent=None):
		ObjectWindow.__init__(self, parent)
		PlaneObject.__init__(self)

		self._maskField = ControlFile('Mask file', self.maskimg )
		self._width = ControlText('Width', str(self.objwidth) )
		self._height = ControlText('Height', str(self.objheight) )

		self._formset = [ '_parent_obj', '_activeField',
			'_objectName','_colorField',
			'_center_of_massField',
			'_positionField','_rotationField',
			'_width','_height','_maskField', '_refractionField',' ']

		self._width.changed_event = self.__widthChanged
		self._maskField.changed_event = self.__maskChanged
		self._height.changed_event = self.__heightChanged

		self.init_form()

	def __maskChanged(self): 
		if self._maskField.value!='':
			self.maskimg = self._maskField.value
		else:
			self.maskimg = None
		self._parent.repaint()

	def __widthChanged(self): 
		try:
			self.objwidth = eval(self._width.value)
			self._parent.repaint()
		except:
			pass

	def __heightChanged(self): 
		try:
			self.objheight = eval(self._height.value)
			self._parent.repaint()
		except:
			pass

	def after_load_scene_object(self):
		super(PlaneWindow, self).after_load_scene_object()
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

if __name__ == "__main__":	 app.start_app( PlaneWindow )
	
