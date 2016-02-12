from py3DSceneEditor.Windows.Camera.FindPosition.__init__ import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import cv2
from numpy import *
from py3DSceneEditor.Windows.Camera.FindPosition.MarkerDetector import MarkerDetector

class FindPositionWithARMarker(BaseWidget):
	
	def __init__(self, parent=None):
		super(FindPositionWithARMarker,self).__init__('Camera calibrator')
		self._parent = parent
		
		self._squareSize 	= ControlText('Square size', '1.0')
		self._player 		= ControlPlayer('Player')
		self._findPosition 	= ControlButton('Find position')
		self._threshold 	= ControlSlider("Threshold", 100, 0, 255)
		self._invert 		= ControlCheckBox('Invert colors')

		self._formset = [
						('_squareSize','_findPosition'),
						('_threshold','_invert')
						,'_player' ] 

		self._findPosition.value = self.findPositionEvent
		self._player.processFrame = self.__processFrame
		self._threshold.changed= self.__thresholdChanged
			
		self.initForm();
		self.setGeometry(0,0, 500,500)

	def __thresholdChanged(self): self._player.refresh()

	def __processFrame(self, frame):
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY )
		binary = cv2.THRESH_BINARY
		if self._invert.value: binary = cv2.THRESH_BINARY_INV
		res, frame= cv2.threshold( frame, self._threshold.value, 255, binary )
		return frame

	
	def findPositionEvent(self):
		thresh = self.__processFrame(self._player.image)
		gray = cv2.cvtColor(self._player.image, cv2.COLOR_BGR2GRAY )
		
		marker_detector = MarkerDetector(
			self._parent.cameraMatrix, self._parent.cameraDistortion, 
			size=float(self._squareSize.value), algo=1 ) 

		rectangles = marker_detector.process(gray, thresh)

		if len(rectangles)>0:
			print("found")
			rvecs, tvecs = rectangles[0]._rvecs, rectangles[0]._tvecs

			rotM 		 = cv2.Rodrigues( rvecs )[0]
			camPos 		 = -matrix(rotM).T*matrix( tvecs )
			camRotVector = cv2.Rodrigues(	matrix(rotM).T  )[0]
			objRotVector = cv2.Rodrigues(	matrix(rotM)	)[0]

			self._parent._position.value 	= "%f,%f,%f" % ( camPos[0,0], 		camPos[1,0], 		camPos[2,0] 		)
			self._parent._rotation.value 	= "%f,%f,%f" % ( camRotVector[0,0], camRotVector[1,0], 	camRotVector[2,0] 	)
		
			
		else:
			print("not found")
			
	def show(self):
		self._player.value = self._parent._videofile.value
		super(FindPositionWithARMarker, self).show()

##################################################################################################################
##################################################################################################################
##################################################################################################################

if __name__ == "__main__":	 app.startApp( CameraFindPositionWithMarker )
	
