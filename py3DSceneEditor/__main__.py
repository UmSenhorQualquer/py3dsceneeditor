from pysettings import conf
import sys, os, numpy as np

from OpenGL.GL 		import *
from OpenGL.GLUT 	import *
from OpenGL.GLU 	import *
from AnyQt.QtWidgets import QFileDialog
import pyforms
from pyforms 			import BaseWidget
from pyforms.controls 	import ControlButton
from pyforms.controls 	import ControlOpenGL
from pyforms.controls 	import ControlSlider
from pyforms.controls 	import ControlText
from pyforms.controls 	import ControlList
from pyforms.controls 	import ControlCombo
from pyforms.controls 	import ControlFile
from pyforms.controls 	import ControlDockWidget
from pyforms.controls 	import ControlToolBox
from pyforms.controls 	import ControlPlayer
from pyforms.controls 	import ControlTree
from pyforms.controls 	import ControlMdiArea


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

from py3dengine.scenes.GLScene import GLScene
from py3DSceneEditor.Windows.py3Dscene_window import Py3DSceneWindow

from py3dengine.utils.WavefrontOBJFormat.WavefrontOBJReader import WavefrontOBJReader
from py3dengine.utils.WavefrontOBJFormat.WavefrontOBJWriter import WavefrontOBJWriter





class SceneCalibrator(BaseWidget, GLScene):
	
	def __init__(self):
		
		super(SceneCalibrator, self).__init__('Scene calibrator')
		GLScene.__init__(self)
		

		self._axis = None

		self._scenewindow 	= Py3DSceneWindow()
		
		self._cameras 		= ControlList('Cameras')
		self._add_cam_btn 	= ControlButton("Add camera")
		self._objs_types 	= ControlCombo("Type")
		self._add_obj_btn 	= ControlButton("Add object")
		self._toolbox 		= ControlToolBox('ToolBox')
		self._tooldock		= ControlDockWidget('Scene', 		  side=ControlDockWidget.SIDE_RIGHT, order=0)
		self._detaildock	= ControlDockWidget('Object details', side=ControlDockWidget.SIDE_RIGHT, order=1)
		self._objtree		= ControlTree('Objects')
		self._mdi 			= ControlMdiArea()
		
		self._formset = [ '_mdi' ]

		self._mdi += self._scenewindow

		self._tooldock.value = self._toolbox

		self.docks = {'right': [self._tooldock, self._detaildock] }

		#Events
		self._add_cam_btn.value 	= self.__add_camera
		self._add_obj_btn.value 	= self.__add_object
		
		self._scenewindow.scene		= self
		self._toolbox.value 		= [ 
			('Cameras',[self._add_cam_btn, self._cameras]						  ),
			('Objects',[self._objs_types, self._add_obj_btn, self._objtree]),
		]

		self._objs_types.add_item('Triangle', 	0)
		self._objs_types.add_item('Marker', 	1)
		self._objs_types.add_item('Rectangle', 2)
		self._objs_types.add_item('Ellipsoid', 3)
		self._objs_types.add_item('Ellipse', 	4)
		self._objs_types.add_item('Cylinder',  5)
		self._objs_types.add_item('Plane',  	6)
		self._objs_types.add_item('Mesh',  		7)
		self._objs_types.add_item('Point',  	8)


		self.init_form()
		

		self._cameras.select_entire_row = True
		self._cameras.readonly 			= True

		self._objtree.show_header 	= False
		
		self._cameras.item_selection_changed_event 	= self.__camera_selection_changed_evt
		self._objtree.item_selection_changed_event 	= self.__object_selection_changed_event
		self._cameras.add_popup_menu_option('Delete', self.__delete_camera)
		self._objtree.add_popup_menu_option('Delete', self.__delete_object)

		self.mainmenu = [
				{
					'File': [
						{'Open scene': 	  self.__importData},
						{'Save scene as': self.__exportData}
					]
				}
			]


		#self.__loadScene('py-3d-engine/examples/DolphinScene.obj')
		#print("------------ loaded -------------------------")

	########################################################################
	############################### CAMERA #################################
	########################################################################

	def __camera_selection_changed_evt(self): 
		self._scenewindow.repaint()
		row = self._cameras.selected_row_index
		if row!=None:
			cell = self._cameras.get_cell(0, row)
			self._detaildock.value = cell._window

	def __add_camera(self): 
		self._cameras += ['New camera']
		row = self._cameras.get_cell(0, self._cameras.rows_count-1)
		row._window = CameraWindow(self)
		row._window.parentRowControl = row

	def __delete_camera(self): self._cameras -= -1

	########################################################################
	############################### CAMERA #################################
	########################################################################

	def __add_object(self):
		objtype = self._objs_types.value

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
		self.update_objects_tree()

	def __delete_object(self):
		item = self._objtree.selected_item
		if item!=None:
			obj = self.getObject(item.text(0))
			self._objects.remove(obj)
			self._objtree -= -1
			self.calculateCollisions()

	def update_objects_tree(self, objects=None, tree_node=None):

		if tree_node==None: 
			print('clear objects tree')
			print(self._objects)
			self._objtree.clear()
		if objects==None: 	objects = self._objects

		for obj in objects:
			if not(tree_node==None and obj.parentObj!=None):
				item = self._objtree.create_child(obj.name, tree_node)
				self._objtree.add_popup_menu_option('Remove', self.__delete_object, item=item)
				self.update_objects_tree(obj.childs, item)

		ObjectWindow.update_allobjects_list()


	def __object_selection_changed_event(self): 
		item = self._objtree.selected_item
		if item!=None:
			win = self.getObject( str(item.text(0)) )
			if win!=None: 
				self._detaildock.value = win


	def find_node_by_name(self, name, root=None):
		if root==None: root = self._objtree.invisibleRootItem()

		if str(root.text(0))==name: return root
		
		for index in range(root.childCount()):
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
		filename, _ = QFileDialog.getOpenFileName(self, "Open file", "", "*.obj")
		if filename: self.__loadScene(filename)

	def __exportData(self):
		filename, _ = QFileDialog.getSaveFileName(self, "Save file", "", "*.obj")
		if filename: 
			if not filename.endswith('.obj'): filename += '.obj'
			self.__saveScene(filename)

	def __loadScene(self, filename):
		w = WavefrontOBJReader(filename)
		self.objects = w.objects
		self.cameras = w.cameras

		self.calculateCollisions()
		
	def getSceneModelTree(self, findNode=None): return self._objtree._model.nodeChildrens(findNode=findNode)

	def repaint(self): 
		self._scenewindow.repaint()




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

			obj.wavefrontobject = o; self._objects.append(obj)

		self.set_hierarchy(value)

		self.update_objects_tree()	

	@property
	def cameras(self):
		try:
			return [self._cameras.get_cell(0,row)._window for row in range(self._cameras.rows_count)]
		except:
			print("No cameras yet")
			return []


	@cameras.setter
	def cameras(self, value):
		for o in value:
			if o.getProperty('type')=='Camera': 
				self._cameras += [ o.name ]
				row = self._cameras.get_cell(0, self._cameras.rows_count-1)
				win = CameraWindow(self)
				win.parentRowControl = row
				win.wavefrontobject = o
				row._window = win


	@property
	def selected_object(self):
		"""
		Return the current selected camera
		"""
		row = self._cameras.selected_row_index
		if row!=None:
			cell = self._cameras.get_cell(0, row)
			return cell._window
		else:
			return None
	
	@selected_object.setter
	def selected_object(self, value): pass



##################################################################################################################
##################################################################################################################
##################################################################################################################
def main(): pyforms.start_app( SceneCalibrator )

if __name__ == "__main__":	main()