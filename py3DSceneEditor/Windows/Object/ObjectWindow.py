from py3DSceneEditor.Windows.Object.__init__ import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

class ObjectWindow(BaseWidget):
	
	def __init__(self, parent=None):
		BaseWidget.__init__(self, 'Object editor')
		self._parent = parent
		
		self._activeField 	= ControlCheckBox('Active')
		self._objectName 	= ControlText('Name')
		self._colorField 	= ControlText('Color', '1.0,1.0,1.0,1.0')
		self._positionField = ControlText('Position', '0.0,0.0,0.0')
		self._rotationField = ControlText('Rotation', '0.0,0.0,1.0,0.0')
		self._centerOfMassField 	= ControlText('Mass center', '0.0,0.0,0.0')
		self._refractionField 	= ControlText('Refraction', '')
		
		
		self._activeField.changed 		= self.__activeChanged
		self._objectName.changed 		= self.__nameChanged
		self._colorField.changed 		= self.__colorChanged
		self._positionField.changed 	= self.__positionChanged
		self._rotationField.changed 	= self.__rotationChanged
		self._centerOfMassField.changed = self.__centerOfMassChanged
		self._refractionField.changed   = self.__refractionChanged

		self.layout().setMargin(5)

	def updateMesh(self): 
		super(ObjectWindow, self).updateMesh()
		self._parent.calculateCollisions()

	def __refractionChanged(self): 
		if self._refractionField.value=='': self.refraction = None
		else:
			self.refraction = float(self._refractionField.value) if self._refractionField.value!='None' else None

	def __activeChanged(self): self.active = self._activeField.value
	
	def __colorChanged(self): 
		self.color = eval(self._colorField.value)
		self._parent.calculateCollisions()

	def __positionChanged(self):
		self.position = eval(self._positionField.value)
		self._parent.calculateCollisions()

	def __rotationChanged(self):
		self.rotation = eval(self._rotationField.value)
		self._parent.calculateCollisions()

	def __centerOfMassChanged(self):
		self.centerOfMass = eval(self._centerOfMassField.value)
		self._parent.calculateCollisions()

	def __nameChanged(self):
		self.setWindowTitle(self._objectName.value)
		treeItem = self._parent.find_node_by_name(self.name)
		self.name = self._objectName.value
		if treeItem: treeItem.setText(self.name)
		
	def afterLoadSceneObject(self):
		super(ObjectWindow, self).afterLoadSceneObject()		
		self._objectName.value			= self.name
		self._colorField.value 			= str(self.color)
		self._positionField.value 		= str(self.position)
		self._rotationField.value 		= str(self.rotation)
		self._centerOfMassField.value 	= str(self.centerOfMass)
		self._activeField.value			= self.active
		self._refractionField.value		= '' if self.refraction==None else str(self.refraction)


	@property
	def parentRowControl(self): return self._parentRowControl
	@parentRowControl.setter
	def parentRowControl(self, value):
		self._parentRowControl = value
		self._objectName.value = value.text()




##################################################################################################################
##################################################################################################################
##################################################################################################################

if __name__ == "__main__":	 app.startApp( ObjectWindow )
	