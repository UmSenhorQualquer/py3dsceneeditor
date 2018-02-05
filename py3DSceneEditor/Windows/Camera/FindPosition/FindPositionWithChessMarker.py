from py3DSceneEditor.Windows.Camera.FindPosition.__init__ import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import cv2
from numpy import *
from py3DSceneEditor.Windows.Camera.FindPosition.FindPositionWithARMarker import FindPositionWithARMarker

class FindPositionWithChessMarker(FindPositionWithARMarker):
	
	
	
	def findPositionEvent(self):
		pattern_size 	= (9, 6)
		pattern_points 	= zeros( (prod(pattern_size), 3), float32 )
		pattern_points[:,:2] = indices(pattern_size).T.reshape(-1, 2)
		pattern_points *= float(self._squareSize.value)

		
			
		image = self._player.image
		if len(image.shape)>2:
			img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY )
		else:
			img = image.copy()
		h, w = img.shape[:2]

		binary = cv2.THRESH_BINARY
		if self._invert.value: binary = cv2.THRESH_BINARY_INV

		res, img= cv2.threshold( img, self._threshold.value, 255, binary)
		found, corners = cv2.findChessboardCorners(img, pattern_size)
		
		if found:
			term = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1 )
			cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), term)

			rvecs, tvecs, inliers = cv2.solvePnPRansac(pattern_points, corners, self._parent.cameraMatrix, self._parent.cameraDistortion)

			rotM 		 = cv2.Rodrigues( rvecs )[0]
			camPos 		 = -matrix(rotM).T*matrix( tvecs )
			camRotVector = cv2.Rodrigues(	matrix(rotM).T  )[0]
			objRotVector = cv2.Rodrigues(	matrix(rotM)	)[0]

			self._parent._position.value 	= "%f,%f,%f" % ( camPos[0,0], 		camPos[1,0], 		camPos[2,0] 		)
			self._parent._rotation.value 	= "%f,%f,%f" % ( camRotVector[0,0], camRotVector[1,0], 	camRotVector[2,0] 	)

	def show(self):
		self._player.value = self._parent._videofile.value
		super(FindPositionWithChessMarker, self).show()

##################################################################################################################
##################################################################################################################
##################################################################################################################

if __name__ == "__main__":	 app.start_app( FindPositionWithChessMarker )
	
