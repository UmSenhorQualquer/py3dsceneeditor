from __init__ import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from py3DEngine.objects.WavefrontObject import WavefrontObject
from py3DSceneEditor.Windows.Object.ObjectWindow import ObjectWindow


class WavefrontWindow(ObjectWindow, WavefrontObject):
	
	def __init__(self, parent=None):
		ObjectWindow.__init__(self, parent)
		WavefrontObject.__init__(self)

		self._terrainField 		= ControlFile('Terrain', 	self._terrainFile 	)
		self._resolutionField 	= ControlText('Resolution', str(self.resolution))
		self._amplitudeField 	= ControlText('Amplitude', 	str(self.amplitude) )
		self._reloadBtn 		= ControlButton('Reload')
		
		self._formset = [ 
			'_objectName','_colorField',
			'_centerOfMassField',
			'_positionField','_rotationField',
			'_terrainField', '_reloadBtn',
			'_resolutionField','_amplitudeField',' ' ]

		self._terrainField.changed = self.__terrainChanged
		self._resolutionField.changed = self.__resolutionChanged
		self._amplitudeField.changed = self.__amplitudeChanged
		self._reloadBtn.value = self.__reloadObj

		self.initForm()

	def __terrainChanged(self): 	self.terrain    = self._terrainField.value
	def __resolutionChanged(self):	self.resolution = int(self._resolutionField.value)
	def __amplitudeChanged(self):	self.amplitude  = float(self._amplitudeField.value)
	def __reloadObj(self): 			self.terrain = self._terrainField.value

	
	def afterLoadSceneObject(self):
		super(WavefrontWindow, self).afterLoadSceneObject()
		self._terrainField.value = str(self._terrainFile)
		self._resolutionField.value = str(self.resolution)
		self._amplitudeField.value = str(self.amplitude)
		
##################################################################################################################
##################################################################################################################
##################################################################################################################

if __name__ == "__main__":	 app.startApp( WavefrontWindow )
	
