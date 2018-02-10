import logging; logger=logging.getLogger(__file__)

from py3DSceneEditor.Windows.Object.__init__ import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np


class ObjectWindow(BaseWidget):

	loaded_objects = []
	
	def __init__(self, parent=None):
		BaseWidget.__init__(self, 'Object editor')
		
		# parent object
		self._parent = parent
		
		self._activeField 		= ControlCheckBox('Active')
		self._objectName 		= ControlText('Name')
		self._colorField 		= ControlText('Color', '1.0,1.0,1.0,1.0')
		self._positionField 	= ControlText('Position', '0.0,0.0,0.0')
		self._rotationField 	= ControlText('Rotation', '0.0,0.0,1.0,0.0')
		self._centerOfMassField = ControlText('Mass center', '0.0,0.0,0.0')
		self._refractionField 	= ControlText('Refraction', '')
		self._parent_obj 		= ControlCombo('Parent object')
		
		
		self._activeField.changed_event 	  = self.__active_changed_evt
		self._objectName.changed_event 		  = self.__name_changed_evt
		self._colorField.changed_event 		  = self.__color_changed_evt
		self._positionField.changed_event 	  = self.__position_changed_evt
		self._rotationField.changed_event 	  = self.__rotation_changed_evt
		self._centerOfMassField.changed_event = self.__center_of_mass_changed_evt
		self._refractionField.changed_event   = self.__refraction_changed_evt
		self._parent_obj.changed_event 		  = self.__parent_obj_changed_evt

		#self.setMinimumHeight(700)
		self.setMinimumWidth(400)
		self.set_margin(5)

		# add to a list all the new objects
		self.loaded_objects.append(self)
		
	@classmethod
	def update_allobjects_list(cls):
		"""
		Update the parents list in all the loaded objects.
		"""
		for obj in cls.loaded_objects:
			obj.update_objects_list()

	def update_objects_list(self):
		"""
		Updates the objects list in the _parent_obj combobox
		"""

		self._updating_objectslist = True # avoid recursive call when the parent is updated
		
		self._parent_obj.clear()
		self._parent_obj.add_item('---None---', 0)
		for obj in self.loaded_objects:
			if obj==self: continue
			self._parent_obj.add_item(obj.name, obj)

		self._parent_obj.value = self.parentObj

		del self._updating_objectslist # delete the flag


	def updateMesh(self): 
		super(ObjectWindow, self).updateMesh()
		if hasattr(self, '_parent') and self._parent is not None:
			self._parent.calculateCollisions()

	def __refraction_changed_evt(self): 
		if self._refractionField.value=='': self.refraction = None
		else:
			self.refraction = float(self._refractionField.value) if self._refractionField.value!='None' else None


	def __parent_obj_changed_evt(self):
		if hasattr(self, '_updating_objectslist'): return
		if self._parent_obj.value:
			self.parentObj = self._parent_obj.value
		else:
			self.parentObj = None
		self._parent.update_objects_tree()

	def __active_changed_evt(self): self.active = self._activeField.value
	
	def __color_changed_evt(self): 
		try:
			self.color = eval(self._colorField.value)
			self._parent.calculateCollisions()
		except:
			pass

	def __position_changed_evt(self):
		try:
			self.position = eval(self._positionField.value)
			self._parent.calculateCollisions()
		except:
			pass

	def __rotation_changed_evt(self):
		try:
			self.rotation = eval(self._rotationField.value)
			self._parent.calculateCollisions()
		except:
			pass

	def __center_of_mass_changed_evt(self):
		self.centerOfMass = eval(self._centerOfMassField.value)
		self._parent.calculateCollisions()

	def __name_changed_evt(self):
		self.setWindowTitle(self._objectName.value)
		treeItem = self._parent.find_node_by_name(self.name)
		self.name = self._objectName.value
		if treeItem: treeItem.setText(0, self.name)
		ObjectWindow.update_allobjects_list()

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

if __name__ == "__main__":	 app.start_app( ObjectWindow )
	