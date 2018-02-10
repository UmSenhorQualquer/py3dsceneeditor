from py3DSceneEditor.Windows.Camera.SelectRay.__init__ import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import cv2
import numpy as np

class ObjectsProjection(BaseWidget):
	
	def __init__(self, parent=None):
		super(ObjectsProjection,self).__init__('Camera ray selector')
		self._parent = parent
		
		self._player = ControlPlayer('Player')
		self._formset = ['_player'] 
		
		self.init_form()

		self._player.process_frame_event = self.__process_frame

		self.setGeometry(0,0, 500,500)

		self._camera = parent
		self._main = parent._parent


	def __process_frame(self, frame): 
		for obj in self._main.objects:
			pts = obj.projectIn(self._camera)
			for p in pts:
				x,y = p = int(round(p[0])), int(round(p[1]))
				if 0<=x<self._camera.cameraWidth and 0<=y<self._camera.cameraHeight:
					cv2.circle(frame, p, 5, (255,255,255), -1)
					cv2.circle(frame, p, 2, (0,255,0), -1)

		return frame




##################################################################################################################
##################################################################################################################
##################################################################################################################

if __name__ == "__main__":	 app.start_app( SelectCameraRay )
	
