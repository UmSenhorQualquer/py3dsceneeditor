from py3DSceneEditor.Windows.Camera.SelectRay.__init__ import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import cv2
import numpy as np

class SelectCameraRay(BaseWidget):
	
	def __init__(self, parent=None):
		super(SelectCameraRay,self).__init__('Camera ray selector')
		self._parent = parent
		
		self._player = ControlPlayer('Player')
		
		self._formset = ['_player'] 

		self._point = None
		
		self.init_form()

		self._player.process_frame_event = self.__process_frame
		self._player.onDoubleClick = self.onDoubleClickInVideoWindow

		self.setGeometry(0,0, 500,500)





	def __process_frame(self, frame): 
		#frame = cv2.undistort(frame, self.cameraMatrix, self.distortion)

		if self._point:
			cv2.circle(frame, self._point, 4, (0,0,255), -1)
			cv2.circle(frame, self._point, 2, (0,255,0), -1)
		
		return frame



	def onDoubleClickInVideoWindow(self, event, x, y): 
		self._point = int(x), int(y)
		self._parent.selectedRay = self._point
		self._player.refresh()
		

	@property
	def cameraMatrix(self): return self._parent.cameraMatrix

	@property
	def distortion(self): return self._parent.cameraDistortion
	




##################################################################################################################
##################################################################################################################
##################################################################################################################

if __name__ == "__main__":	 app.start_app( SelectCameraRay )
	
