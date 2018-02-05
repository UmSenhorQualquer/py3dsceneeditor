from py3DSceneEditor.Windows.Camera.FindPosition.__init__ import *
from numpy import *
from py3DSceneEditor.Windows.Object.MarkerWindow import MarkerWindow
import cv2, pickle


class FindPositionManually(BaseWidget):

    def __init__(self, parent):
        BaseWidget.__init__(self,'Calibrating')
        self._parent = parent
        
        self._player = ControlPlayer("Video")
        self._findBtn = ControlButton('Find')
        self._object = ControlCombo('Object')
        self._usethresh = ControlCheckBox('Use threshold')
        self._threshold = ControlSlider("Threshold", 100, 0, 255)
        self._invert        = ControlCheckBox('Invert colors')
        self._points = ControlText('Points')
        self._formset = [ 
            ('_object','_findBtn'),
            ('_usethresh','_threshold','_invert'),
            '_player', '_points']

        self._player.double_click_event  = self.onDoubleClickInVideoWindow
        self._player.process_frame_event = self.process_frame
        self._threshold.changed_event    = self.__thresholdChanged
        self._usethresh.changed_event    = self.__usethreshChanged
        self.__usethreshChanged()

        self._pointsList = []

        self.init_form()
        
        self._points.changed_event = self.__pointsChangedEvent
        self._findBtn.value = self.__findEvent
        self.setGeometry(0,0, 500,500)

    def __thresholdChanged(self): self._player.refresh()

    def __usethreshChanged(self): 
        self._threshold.enabled = self._usethresh.value
        self._invert.enabled = self._usethresh.value

    def __pointsChangedEvent(self):
        self._pointsList = eval(self._points.value)
        self._player.refresh()

    def __findEvent(self):
        marker = self._object.value
        objectPoints = float32([marker.point0, marker.point1, marker.point2, marker.point3, marker.point4])

        print("########################################################")
        print('Camera matrix',  self._parent.cameraMatrix)
        print('Distortion', self._parent.cameraDistortion)
        
        print("objectPoints", objectPoints)
        print("pointsList", self._pointsList)
        print("########################################################")

        retval, rvecs, tvecs = cv2.solvePnP(
            objectPoints,
            float32(self._pointsList), self._parent.cameraMatrix, self._parent.cameraDistortion)

        """
        rvecs, tvecs, inliers = cv2.solvePnPRansac(
            objectPoints,
            float32(self._pointsList), self._parent.cameraMatrix, self._parent.cameraDistortion)"""

        print(rvecs, tvecs)
        rotM = cv2.Rodrigues( rvecs )[0]
        camPos = -matrix(rotM).T*matrix(tvecs)
        camRotVector = cv2.Rodrigues(matrix(rotM).T)[0]
        objRotVector = cv2.Rodrigues(matrix(rotM))[0]

        self._parent._position.value    = "%f,%f,%f" % ( camPos[0,0], camPos[1,0], camPos[2,0] )
        self._parent._rotation.value    = "%f,%f,%f" % ( camRotVector[0,0], camRotVector[1,0], camRotVector[2,0] )
       
    def process_frame(self, frame):
        #distortion = self._parent.cameraDistortion
        #distortion = array([0,0,0,0,0])
        #frame = cv2.undistort(frame, self._parent.cameraMatrix, distortion)

        if self._usethresh.value:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY )
            binary = cv2.THRESH_BINARY
            if self._invert.value: binary = cv2.THRESH_BINARY_INV
            res, frame= cv2.threshold( frame, self._threshold.value, 255, binary )
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR )
        
        for point in self._pointsList: cv2.circle(frame, point, 4, (0,0,255), -1)
        for point in self._pointsList: cv2.circle(frame, point, 2, (0,255,0), -1)
        
        return frame

    def onDoubleClickInVideoWindow(self, event, x, y):
        mousePos = int(x), int(y)
        self._pointsList.append( mousePos )
        self._points.value = str(self._pointsList)
        self._player.refresh()

    @property
    def objects(self): return self._object.value
    @objects.setter
    def objects(self, value):
        for marker in value: 
            if isinstance(marker, MarkerWindow):
                self._object.add_item(marker.name, marker)
    
    def show(self):
        self._player.value = self._parent._videofile.value
        super(FindPositionManually, self).show()
    
##################################################################################################################
##################################################################################################################
##################################################################################################################

if __name__ == "__main__":   app.start_app( BySelectingPoints )
    
