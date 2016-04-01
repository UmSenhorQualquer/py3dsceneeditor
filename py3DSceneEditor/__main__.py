import sys, os, numpy as np

sys.path.append("..")

from OpenGL.GL 		import *
from OpenGL.GLUT 	import *
from OpenGL.GLU 	import *
from PyQt4 			import QtGui
import pyforms
from pyforms 			import BaseWidget
from pyforms.Controls 	import ControlButton
from pyforms.Controls 	import ControlOpenGL
from pyforms.Controls 	import ControlSlider
from pyforms.Controls 	import ControlText
from pyforms.Controls 	import ControlList
from pyforms.Controls 	import ControlCombo
from pyforms.Controls 	import ControlFile
from pyforms.Controls 	import ControlDockWidget
from pyforms.Controls 	import ControlToolBox
from pyforms.Controls 	import ControlPlayer
from pyforms.Controls 	import ControlTreeView


from py3DSceneEditor.Windows.Camera.CameraWindow 	import CameraWindow
from py3DSceneEditor.Windows.Object.ObjectWindow 	import ObjectWindow
from py3DSceneEditor.Windows.Object.TriangleWindow 	import TriangleWindow
from py3DSceneEditor.Windows.Object.PointWindow 	import PointWindow
from py3DSceneEditor.Windows.Object.RectangleWindow import RectangleWindow
from py3DSceneEditor.Windows.Object.EllipsoidWindow import EllipsoidWindow
from py3DSceneEditor.Windows.Object.MarkerWindow 	import MarkerWindow
from py3DSceneEditor.Windows.Object.EllipseWindow 	import EllipseWindow
from py3DSceneEditor.Windows.Object.CylinderWindow 	import CylinderWindow
from py3DSceneEditor.Windows.Object.PlaneWindow 	import PlaneWindow
from py3DSceneEditor.Windows.Object.WavefrontWindow import WavefrontWindow
from py3DSceneEditor.Windows.Object.TreeSceneModel 	import TreeItem, TreeModel

from py3DEngine.scenes.GLScene import GLScene
from py3DEngine.utils.WavefrontOBJFormat.WavefrontOBJReader import WavefrontOBJReader
from py3DEngine.utils.WavefrontOBJFormat.WavefrontOBJWriter import WavefrontOBJWriter


class SceneCalibrator(BaseWidget, GLScene):
	
	def __init__(self):
		super(SceneCalibrator, self).__init__('Scene calibrator')
		GLScene.__init__(self)
		
		self._axis = None

		self._cameras 		= ControlList('Cameras')
		self._scene 		= ControlOpenGL('Scene')
		self._addCameraBtn 	= ControlButton("Add camera")
		self._objectsTypes 	= ControlCombo("Type")
		self._addObjectBtn 	= ControlButton("Add object")
		self._toolbox 		= ControlToolBox('ToolBox')
		self._tooldock		= ControlDockWidget('Scene', 		  side=ControlDockWidget.SIDE_RIGHT, order=0)
		self._detaildock	= ControlDockWidget('Object details', side=ControlDockWidget.SIDE_RIGHT, order=1)
		self._objectsTree	= ControlTreeView('Objects')
		
		self._formset = [ '_scene' ]

		self._tooldock.value = self._toolbox
		self.docks = {'right': [self._tooldock, self._detaildock] }

		#Events
		self._addCameraBtn.value 	= self.__addCamera
		self._addObjectBtn.value 	= self.__addObject
		
		self._scene.value 			= self
		self._toolbox.value 		= [ 
			('Cameras',[self._addCameraBtn, self._cameras]						  ),
			('Objects',[self._objectsTypes, self._addObjectBtn, self._objectsTree]),
		]

		self._objectsTypes.addItem('Triangle', 	0)
		self._objectsTypes.addItem('Marker', 	1)
		self._objectsTypes.addItem('Rectangle', 2)
		self._objectsTypes.addItem('Ellipsoid', 3)
		self._objectsTypes.addItem('Ellipse', 	4)
		self._objectsTypes.addItem('Cylinder',  5)
		self._objectsTypes.addItem('Plane',  	6)
		self._objectsTypes.addItem('Mesh',  	7)
		self._objectsTypes.addItem('Point',  	8)


		self.initForm()
		
		self._cameras.showGrid 			= False
		self._cameras.showHeader 		= False
		self._cameras.showRowsNumber 	= False
		self._cameras.selectEntireRow 	= True
		self._cameras.editable 			= False

		self._objectsTree.showGrid 			= False
		self._objectsTree.showHeader 		= False
		self._objectsTree.showRowsNumber 	= False
		self._objectsTree.selectEntireRow 	= True
		self._objectsTree.editable		 	= False

		self._scene.addPopupMenuOption('Reset zoom and rotation', self._scene.resetZoomAndRotation)

		self._cameras.itemSelectionChanged 		= self.__cameraSelectionChangedEvent
		self._objectsTree.itemSelectionChanged 	= self.__objectSelectionChangedEvent
		self._objectsTree.itemChangedEvent 		= self.__objectChangedEvent
		self._cameras.addPopupMenuOption('Delete', self.__deleteCamera)
		self._objectsTree.addPopupMenuOption('Delete', self.__deleteObject)

		self.mainmenu = [
				{
					'File': [
						{'Open scene': 	  self.__importData},
						{'Save scene as': self.__exportData}
					]
				}
			]

	
		#self.__loadScene('/home/ricardo/Desktop/01Apollo201403210900/scene_new.obj')
		#self.__loadScene('scene.obj')

		print("------------ loaded -------------------------")

	########################################################################
	############################### CAMERA #################################
	########################################################################

	def __cameraSelectionChangedEvent(self): 
		self._scene.repaint()
		row = self._cameras.mouseSelectedRowIndex
		if row!=None:
			cell = self._cameras.getCell(0, row)
			self._detaildock.value = cell._window

	def __addCamera(self): 
		self._cameras += ['New camera']
		row = self._cameras.getCell(0, self._cameras.count-1)
		row._window = CameraWindow(self)
		row._window.parentRowControl = row

	def __deleteCamera(self): self._cameras -= -1

	########################################################################
	############################### CAMERA #################################
	########################################################################

	def __addObject(self):
		objtype = self._objectsTypes.value

		if objtype==0: obj = TriangleWindow(self)
		if objtype==1: obj = MarkerWindow(self)
		if objtype==2: obj = RectangleWindow(self)
		if objtype==3: obj = EllipsoidWindow(self)
		if objtype==4: obj = EllipseWindow(self)
		if objtype==5: obj = CylinderWindow(self)
		if objtype==6: obj = PlaneWindow(self)
		if objtype==7: obj = WavefrontWindow(self)
		if objtype==8: obj = PointWindow(self)

		self.objects.append( obj )
		self.__updateObjectsTree()

	def __deleteObject(self):
		item = self._objectsTree.selectedItem
		if item!=None:
			obj = self.getObject(item.text())
			self._objects.remove(obj)
			self._objectsTree -= -1
			self.calculateCollisions()

	def __updateObjectsTree(self, objects=None, treeItemNode=None):
		root = False
		print("__updateObjectsTree")
		if treeItemNode==None: 	
			treeItemNode = self._objectsTree.model().invisibleRootItem()
			treeItemNode.removeRows(0, treeItemNode.rowCount() )
			root = True

		if objects==None: objects = self._objects

		for obj in objects:
			if not(root and obj.parentObj!=None):
				item = TreeItem(obj)
				treeItemNode.appendRow( item )

				self.__updateObjectsTree( obj._childs, item)


	def __objectSelectionChangedEvent(self): 
		item = self._objectsTree.selectedItem
		if item!=None:
			win = self.getObject( str(item.text()) )
			if win!=None: 
				self._detaildock.value = win

	
	def __objectChangedEvent(self, item):
		self.recursivelySetHierarchyRoot( self._objectsTree.value, item ) 

	def recursivelySetHierarchyRoot(self, root, item):
		if root!=item and root.text()==item.text(): return
		
		obj = self.getObject(root.text())

		if obj!=None: obj.cleanChilds()

		for rowIndex in range(root.rowCount()):
			child = root.child(rowIndex)
			if obj!=None and ( (item==child and child.text()==item.text()) or child.text()!=item.text() ): 
				child_obj = self.getObject( child.text() )
				obj.addChild(child_obj)
			self.recursivelySetHierarchyRoot( child, item )

	def find_node_by_name(self, name, root=None):
		if root==None: root = self._objectsTree.value
		if str(root.text())==name: return root
		
		for index in range(root.rowCount()):
			child = root.child(index)
			res = self.find_node_by_name( name, child )
			if res: return res

		return None
		

	########################################################################
	########################################################################
	########################################################################
	def calculateCollisions(self):
		objects = self.objects
		for camera in self.cameras:
			for ray in camera.rays: 
				v = np.array(ray._b)-np.array(ray._a)
				v = v/np.linalg.norm(v)
				ray._b = np.array(ray._a) + v*camera.maxFocalLength
				ray.color = camera.color

				ray.collide(objects)
		self.repaint();


	def __importData(self):
		filename = QtGui.QFileDialog.getOpenFileName(self, "Open file", "", "*.obj")
		if filename: self.__loadScene(filename)

	def __exportData(self):
		filename = str(QtGui.QFileDialog.getSaveFileName(self, "Save file", "", "*.obj"))
		if filename: 
			if not filename.endswith('.obj'): filename += '.obj'
			self.__saveScene(filename)

	def __loadScene(self, filename):
		w = WavefrontOBJReader(filename)
		self.objects = w.objects
		self.cameras = w.cameras

		self.calculateCollisions()
		
	def getSceneModelTree(self, findNode=None): return self._objectsTree._model.nodeChildrens(findNode=findNode)

	def repaint(self): self._scene.repaint()




	def __saveScene(self, filename): WavefrontOBJWriter(self).export(filename)

	@property
	def objects(self): 
		try:
			return self._objects
		except:
			print( "No objects yet")
			return []

	@objects.setter
	def objects(self, value): 

		self._objects = []
		for o in value: 
			objtype = o.getProperty('type')
			
			if objtype=='TriangleObject': 	obj = TriangleWindow(self)
			if objtype=='MarkerObject': 	obj = MarkerWindow(self)
			if objtype=='RectangleObject': 	obj = RectangleWindow(self)
			if objtype=='EllipsoidObject': 	obj = EllipsoidWindow(self)
			if objtype=='EllipseObject': 	obj = EllipseWindow(self)
			if objtype=='CylinderObject': 	obj = CylinderWindow(self)
			if objtype=='PlaneObject': 		obj = PlaneWindow(self)
			if objtype=='PointObject': 		obj = PointWindow(self)

			#For historical reasons
			if objtype=='WavefrontObject' or objtype=='TerrainObject': 	obj = WavefrontWindow(self)

			print(o)
			obj.wavefrontobject = o; self._objects.append(obj)

		self.initHierarchy(value)

		self.__updateObjectsTree()	

	@property
	def cameras(self):
		try:
			return [self._cameras.getCell(0,row)._window for row in range(self._cameras.count)]
		except:
			print("No cameras yet")
			return []


	@cameras.setter
	def cameras(self, value):
		for o in value:
			if o.getProperty('type')=='Camera': 
				self._cameras += [ o.name ]
				row = self._cameras.getCell(0, self._cameras.count-1)
				win = CameraWindow(self)
				win.parentRowControl = row
				win.wavefrontobject = o
				row._window = win


	@property
	def selectedObject(self):
		"""
		Return the current selected camera
		"""
		row = self._cameras.mouseSelectedRowIndex
		if row!=None:
			cell = self._cameras.getCell(0, row)
			return cell._window
		else:
			return None
	
	@selectedObject.setter
	def selectedObject(self, value): pass



##################################################################################################################
##################################################################################################################
##################################################################################################################
def main(): pyforms.startApp( SceneCalibrator )

if __name__ == "__main__":	main()