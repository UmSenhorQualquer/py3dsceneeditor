from py3DSceneEditor.Windows.Camera.__init__ import *
from numpy import *
from py3dengine.cameras.Camera 					import Camera
from py3dengine.cameras.Ray 						import Ray
from py3DSceneEditor.Windows.Camera.FindPosition.FindPositionWithARMarker 		import FindPositionWithARMarker
from py3DSceneEditor.Windows.Camera.FindPosition.FindPositionWithChessMarker 	import FindPositionWithChessMarker
from py3DSceneEditor.Windows.Camera.FindPosition.FindPositionManually 			import FindPositionManually
from py3DSceneEditor.Windows.Camera.Calibrate.CalibrateCameraWithMarker 		import CalibrateCameraWithMarker
from py3DSceneEditor.Windows.Camera.SelectRay.SelectCameraRay					import SelectCameraRay
from py3DSceneEditor.Windows.Camera.SelectRay.ObjectsProjection				import ObjectsProjection
from py3DSceneEditor.Windows.Camera.Calibrate.ManualCalibration 			import ManualCalibration
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math, numpy as np

class CameraWindow(BaseWidget, Camera):
	
	def __init__(self, parent=None):
		BaseWidget.__init__(self, 'Scene calibrator')
		Camera.__init__(self)
		self._parent = parent
		self._updating = False

		self.setMinimumHeight(500)
		self.setMinimumWidth(400)

		self._calibratorWindow 				= CalibrateCameraWithMarker(self)
		self._manualCalibrationWindow 		= ManualCalibration(self)
		self._findPositionWithARMarker 		= FindPositionWithARMarker(self)
		self._findPositionWithChessMarker 	= FindPositionWithChessMarker(self)
		self._findPositionManuallyWindow 	= FindPositionManually(self)
		self._selectCameraRayWindow 		= SelectCameraRay(self)
		self._objectsProjectionWindow		= ObjectsProjection(self)

		self._toolbox = ControlToolBox('Properties')

		self._videofile = ControlFile('Video'); 
		self._distortion = ControlText('Distortion', '[-0.355507045984, 0.176486045122, 0.00165274133906, -0.000138058851007, -0.0518798902631]')
		self._videoCalibrationBtn = ControlButton('Calibrate')
		self._videoManualCalibrationBtn = ControlButton('Calibrate manually')
		
		self._cameraName = ControlText('Name')
		self._width = ControlText('Width', "1280")
		self._height = ControlText('Height', "960")
		self._fxField = ControlText('Focal x', '973.83868801')
		self._fyField = ControlText('Focal y', '973.83868801')
		self._cameraMtx = ControlTextArea('Camera matrix')

		self._displayFocalLength = ControlSlider('Focal length', 1.0, 1.0, 100.0)
		self._displayColor 		 = ControlText('Color','0.0,0.0,0.0,0.0')
		self._displayFaces 		 = ControlCheckBox('Display faces')
		self._show 				 = ControlCheckBox('Show')
		
		self._findPositionWithArMarkerBtn = ControlButton('Find transf. using a AR marker')
		self._findPositionWithChessMarkerBtn = ControlButton('Find transf. using a Chess marker')
		self._findPosManuallyBtn = ControlButton('Find transf. manually')
		self._showObjectsProjectionBtn = ControlButton('Show objects projection')

		self._position = ControlText('Cam. Pos.', "0,0,0")
		self._rotation = ControlText('Cam. Rot.', "0,0,0")
		
		self._raysList 		= ControlList('Rays')
		self._addNewRay 	= ControlButton('New ray')

		self._raysList.select_entire_row = True

		self._toolbox.value = [ 
			('Camera matrix and distortion',
				[(self._width, self._height),
				(self._fxField, self._fyField), 
				self._cameraMtx,
				self._distortion,
				self._videoCalibrationBtn,
				self._videoManualCalibrationBtn]  ),
			('Camera transformations',
				[self._position,self._rotation,
				self._findPositionWithArMarkerBtn,
				self._findPositionWithChessMarkerBtn,
				self._findPosManuallyBtn]
				),
			('Renderization',
				[(self._show,self._displayFaces),
				self._displayColor,
				self._displayFocalLength,
				self._showObjectsProjectionBtn]),
			('Rays', 
				[self._addNewRay,
				self._raysList])
		]

		self._formset = [
			'_cameraName',
			'_videofile',
			'_toolbox',' ' ]

		self.init_form()

		self._raysList.add_popup_menu_option('Select ray in the image', self.__showSelectCameraRay)
		self._raysList.add_popup_menu_option('Get intersection', self.__showIntersection)
		self._raysList.add_popup_menu_option('-')
		self._raysList.add_popup_menu_option('Calc distance between points', self.__showCalcDistance)
		self._raysList.add_popup_menu_option('-')
		self._raysList.add_popup_menu_option('Remove', self.__removeRay)


		self._raysList.changed_event 						= self.__rayChanged				
		self._videoManualCalibrationBtn.value       = self.__manualCalibrateEvent
		self._videoCalibrationBtn.value 			= self.__calibrateBtnEvent
		self._findPosManuallyBtn.value 				= self.__findPositionManualEvent
		self._findPositionWithArMarkerBtn.value 	= self.__findPositionWithArMarkerEvent
		self._findPositionWithChessMarkerBtn.value 	= self.__findPositionWithChessMarkerEvent
		self._showObjectsProjectionBtn.value		= self.__showObjectsProjectionEvent
		self.set_margin(5)

		self._videofile.changed_event 	= self.__videofileChanged
		self._cameraName.changed_event 	= self.__nameChanged

		self._width.changed_event 		= self.__imagePropWidthChanged
		self._height.changed_event 		= self.__imagePropHeightChanged
		self._fxField.changed_event 		= self.__imagePropFxChanged
		self._fyField.changed_event 		= self.__imagePropFyChanged
		self._cameraMtx.changed_event     = self.__cameraMtxChanged
		self._distortion.changed_event 	= self.__imagePropDistortionChanged
		
		self._position.changed_event 			= self.__cameraPositionChanged
		self._rotation.changed_event 			= self.__cameraRotationChanged

		self._displayFocalLength.changed_event = self.__displayFocalLengthChanged
		self._displayColor.changed_event 	= self.__displayColorChanged
		self._displayFaces.changed_event 	= self.__displayFacesChanged
		self._show.changed_event 			= self.__showChanged

		self._addNewRay.value = self.__addNewRayEvent

		self._updating = True

	def __loadRays(self):
		objs = []
		for row in self._raysList.value:
			cell = row[0]
			try:
				u,v = eval(cell)
				p0, p1 = self.pixelLinePoints(u,v, self.maxFocalLength)
				ray = Ray(p0, p1)
				objs.append( ray )
			except Exception as e:
				print("error converting ray", str(e))
		self.rays = objs

	def __rayChanged(self, row=0, col=0):
		if self._updating: 
			print("Updated")
			self.__loadRays()
			self._parent.calculateCollisions()


	def __addNewRayEvent(self): 
		self._raysList += ['0,0']
		self.__rayChanged()
		

	def __removeRay(self): 
		self._raysList -= -1
		self.__rayChanged()
	
	def __showIntersection(self):
		ray = self.selectedRay

		if ray: 
			ray.collide(self._parent.objects)
			msg  = 'From: ' + str(ray.points[0]) + '\n'
			msg += 'To: ' 	+ str(ray.points[1]) + '\n'
			msg += 'Distance: ' + str(ray.length) + '\n'
			self.info(msg,'Ray intersection')

	def DistanceBetween(p0, p1):   return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2 + (p0[2] - p1[2])**2)

	def __showCalcDistance(self):
		rays = self.selectedRays

		if len(rays)==2: 
			ray1, ray2 = rays
			ray1.collide(self._parent.objects)
			ray2.collide(self._parent.objects)
			msg  = 'From: ' + str(ray1.points[1]) + '\n'
			msg += 'To: ' 	+ str(ray2.points[1]) + '\n'
			p0 = ray1.points[1]
			p1 = ray2.points[1]
			dist = math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2 + (p0[2] - p1[2])**2)
			msg += 'Distance: ' + str(dist) + '\n'
			self.info(msg, 'Distance between rays end points')

	def __showSelectCameraRay(self):
		self._parent._mdi += self._selectCameraRayWindow

	def __findPositionManualEvent(self):
		self._findPositionManuallyWindow.objects = self._parent.objects
		self._parent._mdi += self._findPositionManuallyWindow

	def __showObjectsProjectionEvent(self):
		self._parent._mdi += self._objectsProjectionWindow
		
	def __findPositionWithArMarkerEvent(self): self._parent._mdi += self._findPositionWithARMarker

	def __findPositionWithChessMarkerEvent(self): self._parent._mdi += self._findPositionWithChessMarker

	def __videofileChanged(self): 
		self._calibratorWindow._player.value 			= self._videofile.value
		self._findPositionWithARMarker._player.value 	= self._videofile.value
		self._findPositionWithChessMarker._player.value = self._videofile.value
		self._selectCameraRayWindow._player.value 		= self._videofile.value
		self._objectsProjectionWindow._player.value 	= self._videofile.value
		self._manualCalibrationWindow._player.value 	= self._videofile.value


	def __cameraPositionChanged(self):
		try:
			self.position 		= eval( self._position.value )
			#self._parent.repaint()
			self.__loadRays()
			self._parent.calculateCollisions()
		except: 
			print("error in CameraWindow in the function __cameraPositionChanged")

	def __cameraRotationChanged(self):
		try:
			self.rotationVector = eval( self._rotation.value )
			#self._parent.repaint()
			self.__loadRays()
			self._parent.calculateCollisions()
		except: print("error in CameraWindow in the function __cameraRotationChanged")

	def __displayFocalLengthChanged(self): 
		self.maxFocalLength = float(self._displayFocalLength.value);
		self._parent.repaint()
	
	def __displayColorChanged(self):
		try:
			self._color = eval(self._displayColor.value);
			self._parent.repaint()
		except:
			pass

	def __displayFacesChanged(self): self.showFaces = self._displayFaces.value; self._parent.repaint()
	def __showChanged(self): self._parent.repaint()

	def __imagePropWidthChanged(self):
		try:
			self.cameraWidth = float(self._width.value)
		except:
			self.cameraWidth = 0
		self.cameraCx = self.cameraWidth / 2.0
		self._parent.repaint()
	def __imagePropHeightChanged(self):
		try:
			self.cameraHeight = float(self._height.value)
		except:
			self.cameraHeight = 0
		self.cameraCy = self.cameraHeight / 2.0
		self._parent.repaint()
	def __cameraMtxChanged(self):
		try:
			self.cameraMatrix 	= matrix( eval(self._cameraMtx.value) )
			self._width.value 	= str(self.cameraMatrix[0,2]*2)
			self._height.value 	= str(self.cameraMatrix[1,2]*2)
			self._fxField.value = str(self.cameraMatrix[0,0])
			self._fyField.value = str(self.cameraMatrix[1,1])
			self._parent.repaint()
		except:
			pass
		

	def __imagePropFxChanged(self):
		try:
			self.cameraFx = float(self._fxField.value);
			self._parent.repaint()
		except:
			pass

	def __imagePropFyChanged(self):
		try:
			self.cameraFy = float(self._fyField.value);
			self._parent.repaint()
		except:
			pass
		
	def __imagePropDistortionChanged(self):
		try:
			self.cameraDistortion = float32( list(eval(self._distortion.value)) ); self._parent.repaint()
			self._calibratorWindow.distortion 			= self.cameraDistortion
			self._findPositionWithARMarker.distortion 	= self.cameraDistortion
			self._findPositionWithChessMarker.distortion = self.cameraDistortion
			self._selectCameraRayWindow._player.refresh()
		except:
			pass

	def __manualCalibrateEvent(self):
		self._manualCalibrationWindow.clear()
		self._parent._mdi += self._manualCalibrationWindow

	def __calibrateBtnEvent(self):
		self._calibratorWindow.clear()
		self._parent._mdi += self._calibratorWindow

	def __nameChanged(self):
		self.setWindowTitle(self._cameraName.value)
		if hasattr(self, 'parentRowControl'):
			self.parentRowControl.setText(self._cameraName.value)
		self.name = self._cameraName.value

		
	@property
	def fovY(self): return math.degrees( 2*math.atan2( float(self._width.value)/2.0, float(self._fyField.value) ) )

	@property
	def parentRowControl(self): return self._parentRowControl
	@parentRowControl.setter
	def parentRowControl(self, value):
		if value!=None:
			self._parentRowControl = value
			self._cameraName.value = value.text()
		else:
			del self._parentRowControl
		
	
	@property
	def selectedRays(self):
		indexes = self._raysList.mouseSelectedRowsIndexes
		if indexes==None: return None
		res = []
		for index in indexes:
			cell = self._raysList.value[index][0]
			try:
				u,v = eval(cell)
				p0, p1 = self.pixelLinePoints(u,v, self.maxFocalLength)
				ray = Ray(p0, p1)
				res.append(ray)
			except:
				pass
		return res

	@property
	def selectedRay(self):
		index = self._raysList.selected_row_index
		if index==None: return None

		cell = self._raysList.value[index][0]
		try:
			u,v = eval(cell)
			p0, p1 = self.pixelLinePoints(u,v, self.maxFocalLength)
			ray = Ray(p0, p1)
			return ray
		except:
			pass

	@selectedRay.setter
	def selectedRay(self, value):
		if isinstance(value, tuple): 
			index = self._raysList.selected_row_index
			self._raysList.setValue(0, index, str(value).replace(')','').replace('(',''))
			self.__rayChanged()


	def DrawGL(self, objects=[]):
		if self._show.value: super(CameraWindow, self).DrawGL(objects)
		

	##########################################################################################
	###########Properties ####################################################################
	##########################################################################################




##########################################################################################
###########Refresh values#################################################################
##########################################################################################

	def refreshWindowValues(self):

		self._position.value 	= ','.join(map(str,self.position.tolist()))
		self._rotation.value 	= ','.join(map(str,self.rotationVector.tolist()))
		
		self._distortion.value 			= ','.join(map(str,self.cameraDistortion.tolist()))
		self._cameraName.value 			= self.name
		self._width.value 				= str(self.cameraMatrix[0,2]*2)
		self._height.value 				= str(self.cameraMatrix[1,2]*2)
		self._fxField.value 			= str(self.cameraMatrix[0,0])
		self._fyField.value 			= str(self.cameraMatrix[1,1])
		self._displayFocalLength.value 	= self.maxFocalLength
		self._displayColor.value 		= str(','.join(map(str,self.color)))
		self._displayFaces.value 		= self.showFaces
		self._cameraMtx.value 			= np.array2string(self.cameraMatrix, separator=',', suppress_small=True)
		
		self.__loadRays()
		

##########################################################################################
###########Overide WavefrontOBJCamera#####################################################
##########################################################################################

	@property
	def wavefrontobject(self):
		obj = super(CameraWindow, self).wavefrontobject
		obj.addProperty('videofile', self._videofile.value)
		obj.addProperty('visible', 	self._show.value )

		obj.addProperty('nrays', len(self._raysList.value) )
		for i, row in enumerate(self._raysList.value): obj.addProperty('ray_%d' % i, row[0] )
			
		return obj

	@wavefrontobject.setter
	def wavefrontobject(self, value):
		self._updating = False

		Camera.wavefrontobject.fset(self, value)
		self._videofile.value 	= value.getProperty('videofile')
		self._show.value 		= value.getProperty('visible')=='True'

		nrays = value.getProperty('nrays')

		if nrays: nrays = int(nrays)
		else: nrays = 0

		for i in range(nrays):
			self._raysList += [ str(value.getProperty('ray_%d' % i)) ]

		self.refreshWindowValues()
		self._updating = True

###########################################################################################
###########################################################################################
###########################################################################################

if __name__ == "__main__":	 app.start_app( CameraWindow )
	
