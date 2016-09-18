from py3DSceneEditor.Windows.__init__ import *

from pyforms.Controls 	import ControlOpenGL


class Py3DSceneWindow(BaseWidget):


	def __init__(self):
		BaseWidget.__init__(self,'Import cameras from video')


		self._scene 		= ControlOpenGL('Scene')
		
		self._formset = ['_scene']

		self._scene.addPopupMenuOption('Reset zoom and rotation', self._scene.resetZoomAndRotation)

	@property
	def scene(self):
	    return self._scene.value
	@scene.setter
	def scene(self, value):
		self._scene.value = value

	

###########################################################################################
###########################################################################################
###########################################################################################

if __name__ == "__main__":	 app.startApp( ImportCamerasFromVideo )