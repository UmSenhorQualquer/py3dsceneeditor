from py3DSceneEditor.Windows.__init__ import *

from pyforms.controls 	import ControlOpenGL


class Py3DSceneWindow(BaseWidget):


	def __init__(self):
		BaseWidget.__init__(self,'Import cameras from video')


		self._scene 		= ControlOpenGL('Scene')
		
		self._formset = ['_scene']

		self._scene.add_popup_menu_option('Reset zoom and rotation', self._scene.reset_zoom_and_rotation)

	@property
	def scene(self):
	    return self._scene.value
	@scene.setter
	def scene(self, value):
		self._scene.value = value


	def repaint(self):
		super(Py3DSceneWindow,self).repaint()
		self._scene.repaint()

	

###########################################################################################
###########################################################################################
###########################################################################################

if __name__ == "__main__":	 app.start_app( ImportCamerasFromVideo )