from py3DSceneEditor.Windows.Camera.Calibrate.__init__ import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import cv2
import numpy as np
from PyQt4 import QtGui

class CalibrateCameraWithMarker(BaseWidget):
	
	def __init__(self, parent=None):
		super(CalibrateCameraWithMarker,self).__init__('Camera calibrator')
		self._parent = parent
		
		self._player = ControlPlayer('Player')
		self._frames = ControlList('Frames')
		self._addFrameBtn = ControlButton('Add frame')
		self._calibrateBtn = ControlButton('Calibrate')
		self._sizeOfSquare = ControlText('Square size', '0.304')
		self._patternSize = ControlText('Pattern size', '5,7')
		self._threshold = ControlSlider('Threshold', 150, 0, 255)
		self._invert = ControlCheckBox('Invert')
		self._findmarker = ControlCheckBox('Find marker')
		self._usecalibration = ControlCheckBox('Play video with calibration values')
		self._usethresh = ControlCheckBox('Use threshold')

		self._formset = [ '_player','=',
				[
					('_usethresh','_threshold','_invert','_findmarker'),
					('_sizeOfSquare','_patternSize','_usecalibration',
					'_addFrameBtn','_calibrateBtn'),
					'_frames'] 
			]

		self._addFrameBtn.value = self.__addFrameEvent
		self._calibrateBtn.value = self.__calibrationEvent
		self._threshold.changed= self.__thresholdChanged
		self._frames.showGrid = False
		self._frames.showHeader = False
		self._frames.showRowsNumber = False
		self._frames.selectEntireRow = True
		self._usethresh.changed = self.__usethreshChanged
		self._frames.addPopupMenuOption('Delete', self.__deleteFrame)

		self._player.processFrame = self.__processFrame
		
		self.initForm()
		
		self.setGeometry(0,0, 500,500)

	def clear(self): self._frames.clear()

	def __thresholdChanged(self): self._player.refresh()

	def __usethreshChanged(self): 
		self._threshold.enabled = self._usethresh.value
		self._invert.enabled = self._usethresh.value

	def __processFrame(self, frame): 
		if self._usecalibration.value:
			frame = cv2.undistort(frame, self.cameraMatrix, self.distortion)

		showingImg = frame
		if self._usethresh.value:
			if len(frame.shape)>2: 
				gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY )
			else: 
				gray = frame.copy()
			binary = cv2.THRESH_BINARY
			if self._invert.value: binary = cv2.THRESH_BINARY_INV
			ret,gray = cv2.threshold(gray,self._threshold.value,255,binary)
			showingImg = gray

		if self._findmarker.value:
			pattern_size = eval(self._patternSize.value)
			found, corners = self.__findMarker(frame, pattern_size, 
				self._usethresh.value, self._threshold.value, self._invert.value)
			#if len(frame.shape)==2: frame = cv2.merge( (frame, frame, frame) )

			cv2.drawChessboardCorners(showingImg, pattern_size, corners, found)


		return showingImg



	def __deleteFrame(self): self._frames -= -1
	def __addFrameEvent(self):
		if self._player.enabled:
			self._frames += [ "Frame: %d, Use Threshold %s, Threshold: %d, Inverted: %s" % (self._player.video_index, self._usethresh.value, self._threshold.value, self._invert.value) ]
			self._frames.cells[-1][0].image 		= self._player.image
			self._frames.cells[-1][0].threshold 	= self._threshold.value
			self._frames.cells[-1][0].inverted 		= self._invert.value
			self._frames.cells[-1][0].usethreshold 	= self._usethresh.value

	def __findMarker(self, img, pattern_size, usethreshold, threshold, inverted):
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY ) if len(img.shape)>2 else img.copy()
		
		if usethreshold:
			binary = cv2.THRESH_BINARY_INV if inverted else cv2.THRESH_BINARY
			ret,img = cv2.threshold(img,threshold,255,binary)
		
		found, corners = cv2.findChessboardCorners(img, pattern_size)
		if found:
			term = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1 )
			cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), term)
					
		return found, corners

	def __calibrationEvent(self):
		square_size = float(self._sizeOfSquare.value)
		pattern_size = eval(self._patternSize.value)

		pattern_points = np.zeros( (np.prod(pattern_size), 3), np.float32 )
		pattern_points[:,:2] = np.indices(pattern_size).T.reshape(-1, 2)
		pattern_points *= square_size

		if len( self._frames.cells )>0:
			
			obj_points = []
			img_points = []
			h, w = 0, 0

			good_images = 0
			for cell in self._frames.cells:
				image = cell[0].image
				if image==None: continue

				h, w = image.shape[:2]
				threshold = cell[0].threshold 
				inverted = cell[0].inverted
				usethreshold = cell[0].inverted
				
				found, corners = self.__findMarker(image, pattern_size, usethreshold, threshold, inverted)

				if found:
					good_images += 1

					img_points.append(corners.reshape(-1, 2))
					obj_points.append(pattern_points)
				else:
				    #QtGui.QMessageBox.alert(None, 'Error', 'No chessboards found.' )
				    print("no chessboards found")
				
				

			if good_images>0:
				rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (w, h))
				print("RMS:", rms)
				print("camera matrix:\n", camera_matrix)
				print("distortion coefficients: ", dist_coefs.ravel())

				self._parent._distortion.value = str(list(dist_coefs.ravel()))
				self._parent._fxField.value = str(camera_matrix[0,0])
				self._parent._fyField.value = str(camera_matrix[1,1])
				self._parent._width.value  = str(camera_matrix[0,2])
				self._parent._height.value = str(camera_matrix[1,2])

				QtGui.QMessageBox.information(None, 'Complete', 
					'Calibration is completed. Used %d images' % good_images )
			else:
			    QtGui.QMessageBox.critical(None, 'Error', 'No good images found.' )

	@property
	def cameraMatrix(self): return self._parent.cameraMatrix
	@cameraMatrix.setter
	def cameraMatrix(self, value): pass

	@property
	def distortion(self): return self._parent.cameraDistortion
	@distortion.setter
	def distortion(self, value): pass



##################################################################################################################
##################################################################################################################
##################################################################################################################

if __name__ == "__main__":	 app.startApp( CalibrateCameraWithMarker )
	
