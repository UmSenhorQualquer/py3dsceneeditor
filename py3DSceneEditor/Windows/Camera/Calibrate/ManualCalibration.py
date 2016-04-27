from py3DSceneEditor.Windows.Camera.Calibrate.__init__ import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import cv2
import numpy as np
from PyQt4 import QtGui

class ManualCalibration(BaseWidget):
	
	def __init__(self, parent=None):
		super(ManualCalibration,self).__init__('Camera calibrator')
		self._parent = parent
		
		self._player 			= ControlPlayer('Player')
		self._realobject 		= ControlList('Real object points')
		self._addObjPoint 		= ControlButton('Add object point')
		self._pixelsobject 		= ControlList('Pixels')
		self._calibrateBtn 		= ControlButton('Calibrate')
		self._usecalibration 	= ControlCheckBox('Play video with calibration values')
		
		self._formset = [ '_player','=',
				[('_realobject','_pixelsobject'), ('_addObjPoint','_usecalibration','_calibrateBtn'),] 
			]

		self._calibrateBtn.value = self.__calibrationEvent
		self._realobject.showGrid = False
		self._realobject.showHeader = False
		self._realobject.showRowsNumber = False
		self._realobject.selectEntireRow = True
		self._realobject.addPopupMenuOption('Delete', self.__deleteObjPoint)

		self._pixelsobject.showGrid = False
		self._pixelsobject.showHeader = False
		self._pixelsobject.showRowsNumber = False
		self._pixelsobject.selectEntireRow = True
		self._pixelsobject.addPopupMenuOption('Delete', self.__deletePixelPoint)

		self._addObjPoint.value = self.__addObjectPoint

		self._player.processFrame = self.__processFrame
		
		self.initForm()
		
		self.setGeometry(0,0, 500,500)

	def clear(self): self._realobject.clear()

	def __addObjectPoint(self):
		self._realobject+= ['0,0']

	def __processFrame(self, frame): 
		if self._usecalibration.value: 
			frame = cv2.undistort(frame, self.cameraMatrix, self.distortion)

		return frame



	def __deleteObjPoint(self): self._realobject -= -1
	def __deletePixelPoint(self): self._pixelsobject -= -1
	
	def __calibrationEvent(self):
		pass
	
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
	
