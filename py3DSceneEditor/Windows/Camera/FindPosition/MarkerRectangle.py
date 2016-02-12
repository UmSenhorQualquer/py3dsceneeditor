__author__ = "Ricardo Jorge Vieira Ribeiro"
__copyright__ = "Copyright 2013, Scientific Software Platform - Neuroscience Programme - Champalimaud Foundation"
__license__ = "GNU GPL"
__version__ = "1.0.0"
__maintainer__ = "Ricardo Jorge Vieira Ribeiro"
__email__ = ["ricardo.ribeiro@neuro.fchampalimaud.org", "ricardojvr@gmail.com"]
__status__ = "Production"

import cv2, itertools
from numpy import *
#from tools import *

def DistanceBetween(p0, p1):   return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)


def RotateImage(image, angle):
	if hasattr(image, 'shape'):
		image_center = tuple(array(image.shape)/2)
		shape = image.shape
	elif hasattr(image, 'width') and hasattr(image, 'height'):
		image_center = (image.width/2, image.height/2)
		shape = narray((image.width, image.height))
	else:
		raise Exception( 'Unable to acquire dimensions of image for type {0}.'.format(type(image)) )
	
	rot_mat = cv2.getRotationMatrix2D(image_center[0:2], angle, scale=1.0)
	result = cv2.warpAffine(image, rot_mat, shape[0:2], flags=cv2.INTER_LINEAR)
	return result


def DivideImageByThresholdBlocks( image, divide = 2):
	h, w = image.shape[:2]
	w_step, h_step = w / divide, h / divide
	x_values = [x for x in arange(0, w, w_step)]
	y_values = [y for y in arange(0, h, h_step)]
	external_product =  list( itertools.product(*[x_values, y_values ]) )
	thresh_values = []
	for i in range(len(external_product)):
		p1 = external_product[ i ]
		p2 = p1[0]+w_step, p1[1]+h_step
		img =  image[p1[1]:p2[1], p1[0]:p2[0]]
		avg = average( img)
		thresh_values.append(avg)
	return thresh_values





class MarkerRectangle(object):
	"""
	Describes one ARMarker
	"""

	MARKER_OUTER_SIZE = 1.0

	PROJECTION_IMAGE_SIZE = 50
	PROJECTION_IMAGE_BOX = ( PROJECTION_IMAGE_SIZE, PROJECTION_IMAGE_SIZE )
	DESTINY_CONNERS = float32( [ (0,0), (0,PROJECTION_IMAGE_SIZE), (PROJECTION_IMAGE_SIZE,PROJECTION_IMAGE_SIZE), (PROJECTION_IMAGE_SIZE,0) ])
		
	WARP_PRESPECTIVE_FLAGS = cv2.INTER_LINEAR + cv2.WARP_FILL_OUTLIERS

	PROJECTED_IMAGE_MASK = zeros( (50,50), dtype=uint8 )
	KERNEL = cv2.getStructuringElement(cv2.MORPH_CROSS,(5,5))

	PROJECTED_IMAGE_CELL_MASK = zeros( (10,10), dtype=uint8)


	def __init__(self, image, original_image, contour, referencePoint, center, model):
		"""
		Constructor: Init the default values
		"""
		cv2.ellipse( self.PROJECTED_IMAGE_MASK 	, (25, 25), (20,20), 0, 0, 360, (1), -1, cv2.AA)
		cv2.ellipse( self.PROJECTED_IMAGE_CELL_MASK , (5, 5), (5,5), 0, 0, 360, (1), -1, cv2.AA)

		self._referencePoint = referencePoint
		self._direction = 0
		self._contour = contour
		self._model = model
		self._rvecs = None
		self._tvecs = None
		self._history = []
		self._centroid = center
		self.process(contour, image, referencePoint, center, original_image)

	def process(self, contour, image, referencePoint, center, original_image=None):
		self._history.append(center)
		self._outer_center = center
		self._marker_id = -1
		
		self._map_matrix, self._projected_img, \
			self._direction, self._outer_corners = self.__decode_marker_2D(image, \
				contour,  referencePoint)
		self._contour = self._outer_corners



	def update( self, rectangle):
		self._history.append(rectangle._outer_center)
		self._projected_img = rectangle._projected_img
		self._contour = rectangle._contour
		self._direction = rectangle._direction
		self._referencePoint = rectangle._referencePoint
		self._outer_corners = rectangle._outer_corners
		self._outer_center = rectangle._outer_center
		


	def __refine_boundaries( self, hsv_v_image, original_contour, contour_left_conner_point, filter_hsv_value=False, original_image=None):
		if filter_hsv_value: hsv_v_image = cv2.inRange(hsv_v_image, array(250), array(255) )
		#res, gray = cv2.threshold(hsv_v_image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
		#gray = cv2.adaptiveThreshold(hsv_v_image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,3,0)
		#gray = cv2.Canny(hsv_v_image, 100, 200, apertureSize=3)
		#gray = cv2.Canny(hsv_v_image, 0, 1, apertureSize=3)
		gray = cv2.Canny(hsv_v_image, 0, 1, apertureSize=3)

		#gray = extractObject(hsv_v_image , threshold_values=[ (301, 0), (351, 0), (401, 0), (1001, 0) ])
		#gray = extractObject(hsv_v_image , threshold_values=[ (201, 0) ])
		contours, hierarchy = cv2.findContours(gray.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		outer_corners  = None
		if len(contours)>0:
			bigger = None
			biggerArea = cv2.contourArea(original_contour)
			for c in contours:
				area = cv2.contourArea(c)
				if area>biggerArea: biggerArea = area; bigger = c
			if bigger!=None:
				cnt_len = cv2.arcLength(bigger, True)
				selected = cv2.approxPolyDP(bigger, 5, True)
				if len(selected)!=4:  outer_corners = [a[0] for a in original_contour]
				else: outer_corners = [ (a[0][0]+contour_left_conner_point[0], a[0][1] + contour_left_conner_point[1]) for a in selected]
			else:
				outer_corners = [a[0] for a in original_contour]
		else: outer_corners = [a[0] for a in original_contour]
		return hsv_v_image, outer_corners


	def __align_marker_corners(self, corners, direction):
		if direction<=0: return corners
		if direction==1: return [ corners[1], corners[2], corners[3], corners[0] ]
		if direction==2: return [ corners[2], corners[3], corners[0], corners[1] ]
		if direction==3: return [ corners[3], corners[0], corners[1], corners[2] ]
		



	def __read_blocks(self, projected_img):
		h, w = projected_img.shape[:2]
		w_step, h_step = 10, 10
		x_values = [x for x in arange(0, w, w_step)]
		y_values = [y for y in arange(0, h, h_step)]
		external_product =  list( itertools.product(*[x_values, y_values ]) )
		activated = []
		for p1 in external_product:
			p2 = p1[0]+w_step, p1[1]+h_step
			avg = average( self.PROJECTED_IMAGE_CELL_MASK * projected_img[p1[1]:p2[1], p1[0]:p2[0]] )
			activated.append( (avg/255.0) >= 0.5 )
			#cv2.rectangle( self._projected_img, p1, p2, (0,0,255), -1 )
			#if activated[i]: cv2.rectangle( self._projected_img, p1, p2,100, 3 )			
			#text = "%d" % i
			#cv2.putText(self._projected_img, text , (p1[0]+mask_size/2, p1[1]+mask_size/2), cv2.FONT_HERSHEY_PLAIN, 0.3, 255, thickness = 3, lineType=cv2.CV_AA)
			#cv2.putText(self._projected_img, text , (p1[0]+mask_size/2, p1[1]+mask_size/2), cv2.FONT_HERSHEY_PLAIN, 0.3, 0, thickness = 1, lineType=cv2.CV_AA)	
		return activated

	def __check_direction(self, projected_image):
		"""
		Find the marker direction
		@param projected_img: Marker image
		@type projected_img: Numpy OpenCV image
		"""		
		image = projected_image * self.PROJECTED_IMAGE_MASK
		contours, hierarchy = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		if len(contours)>=3 or len(contours)<=1:
			image = cv2.erode(image,self.KERNEL)
			image = cv2.dilate(image,self.KERNEL)
			contours, hierarchy = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		smallest, centroid = 100000 , None
		for contour in contours:
			m = cv2.moments(contour); area = m['m00']
			if smallest>area and area>0: centroid, smallest  = ( m['m10']/m['m00'],m['m01']/m['m00'] ), area

		rotation = 0
		if centroid!=None:
			if smallest<=140:
				if centroid[0]>=25 and centroid[1]<=25: 
					image = RotateImage(image, 90)
					rotation = 3
				elif centroid[0]>=25 and centroid[1]>=25: 
					image = RotateImage(image, 180)
					rotation = 2
				elif centroid[0]<=25 and centroid[1]>=25: 
					image = RotateImage(image, 270)
					rotation = 1
			else:
				if centroid[0]>=25 and centroid[1]<=25: 
					image = RotateImage(image, 90+180)
					rotation = 3
				elif centroid[0]>=25 and centroid[1]>=25: 
					image = RotateImage(image, 180+180)
					rotation = 2
				elif centroid[0]<=25 and centroid[1]>=25: 
					image = RotateImage(image, 270+180)
					rotation = 1

		
		return rotation, image



	def __check_id(self, activated, projected_image, use_svm = False):
		"""
		Find the marker direction
		@param projected_img: Marker image
		@type projected_img: Numpy OpenCV image
		"""
		if activated[8] and activated[13] and not activated[18]  and activated[17]  and activated[16]: return 1
		if activated[8] and activated[13] and activated[18]  and not activated[17]  and not activated[16]: return 2
		if not activated[8]  and activated[13] and activated[18]  and activated[17] and not activated[16]  : return 3
		if use_svm: return self._model.predict( float32( DivideImageByThresholdBlocks(projected_image) )  )
		else: return 0
		
	def __decode_marker_2D(self, gray, outer_corners, contour_left_conner_point, use_svm = False):
		corners = float32( outer_corners)


		map_matrix = cv2.getPerspectiveTransform(corners, self.DESTINY_CONNERS)
		projected_img = cv2.warpPerspective( gray, map_matrix, self.PROJECTION_IMAGE_BOX, flags = self.WARP_PRESPECTIVE_FLAGS )
		res, projected_img = cv2.threshold(projected_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

		d = list( outer_corners )

		direction, projected_img 	= self.__check_direction(projected_img)
		active_blocks 				= self.__read_blocks(projected_img)
		outer_corners 				= self.__align_marker_corners( outer_corners, direction)
		self._marker_id 			= self.__check_id(active_blocks, projected_img, use_svm)
		
		
		return map_matrix, projected_img, direction, outer_corners
	

############################################################################
############################################################################
############################################################################
############################################################################


	def distance(self, rectangle):  return DistanceBetween( self._outer_center, rectangle._outer_center )


############################################################################
############################################################################
############################################################################
############################################################################
	
	def __repr__(self): 	return "MARKER ID:%s" % self._marker_id
	def __str__(self): 	return "MARKER ID:%s" % self._marker_id
	def __unicode__(self): 	return u"MARKER ID:%s" % self._marker_id

	def draw(self,image):
		"""
		Draw: Draw a contour arround the blob
		@param image: Image where to draw the contour
		@type image: Opencv Numpy Image
		"""
		"""
		for i, point in enumerate(self._outer_corners):
			text = "%d" % i
			cv2.putText(image, text , tuple(point), cv2.FONT_HERSHEY_PLAIN, 1.3, (0, 0, 255), thickness = 1, lineType=cv2.CV_AA)
		"""
		#cv2.polylines(image, int32([self._outer_corners ]), True, (0,255,0), 1 )
		if self._marker_id<=0.0: 

			v = (array(self._outer_corners[2])-array(self._outer_corners[0]) )/2
			p = self._outer_corners[0]+v
			cv2.circle(image, tuple(p), 1, (0,255,0), 2 )

			#cv2.line(image,tuple(self._outer_corners[1]), tuple(self._outer_corners[2]), (255,255,0), 2 )
			#cv2.line(image,tuple(self._outer_corners[2]), tuple(self._outer_corners[3]), (255,0,255), 2 )

			dist1 = DistanceBetween(self._outer_corners[0], self._outer_corners[1])
			dist2 = DistanceBetween(self._outer_corners[1], self._outer_corners[2])
			dist3 = DistanceBetween(self._outer_corners[2], self._outer_corners[3])
			dist4 = DistanceBetween(self._outer_corners[3], self._outer_corners[0])

			if min(dist1,dist2,dist3,dist4)==dist1:
				cv2.line(image,tuple(self._outer_corners[0]), tuple(self._outer_corners[1]), (255,0,255), 1 )
			elif min(dist1,dist2,dist3,dist4)==dist2:
				cv2.line(image,tuple(self._outer_corners[1]), tuple(self._outer_corners[2]), (255,0,255), 1 )
			elif min(dist1,dist2,dist3,dist4)==dist3:
				cv2.line(image,tuple(self._outer_corners[2]), tuple(self._outer_corners[3]), (255,0,255), 1 )
			elif min(dist1,dist2,dist3,dist4)==dist4:
				cv2.line(image,tuple(self._outer_corners[3]), tuple(self._outer_corners[0]), (255,0,255), 1 )
			
			if max(dist1,dist2,dist3,dist4)==dist1:
				cv2.line(image,tuple(self._outer_corners[0]), tuple(self._outer_corners[1]), (0,255,100), 1 )
			elif max(dist1,dist2,dist3,dist4)==dist2:
				cv2.line(image,tuple(self._outer_corners[1]), tuple(self._outer_corners[2]), (0,255,100), 1 )
			elif max(dist1,dist2,dist3,dist4)==dist3:
				cv2.line(image,tuple(self._outer_corners[2]), tuple(self._outer_corners[3]), (0,255,100), 1 )
			elif max(dist1,dist2,dist3,dist4)==dist4:
				cv2.line(image,tuple(self._outer_corners[3]), tuple(self._outer_corners[0]), (0,255,100), 1 )
			

			"""
			if dist1>=dist2:
				cv2.polylines(image, int32([self._outer_corners[1:2] ]), True, (0,0,255), 9 )
			else:
				cv2.polylines(image, int32([self._outer_corners[3:] ]), True, (0,255,0), 9)
			"""
			
			#cv2.putText(image, "%0.3f" % dist1 ,  tuple(self._outer_corners[1]) ,  cv2.FONT_HERSHEY_PLAIN, 0.7, (0, 100, 0), thickness = 1, lineType=cv2.CV_AA)
			#cv2.putText(image, "%0.3f" % dist2 ,  tuple(self._outer_corners[3]) ,  cv2.FONT_HERSHEY_PLAIN, 0.7, (0, 100, 0), thickness = 1, lineType=cv2.CV_AA)
			
		else:

			p0, p1 = self._outer_center

			#trans = round(self._translation_vector[0], 2), round(self._translation_vector[1], 2), round(self._translation_vector[2], 2)
			#text = "ID: %s,  Dir: %s" % (self._marker_id, str(trans) )
			text = "ID: %s" % (self._marker_id )

			#rots = round(self._rotation_vector[0], 2), round(self._rotation_vector[1], 2), round(self._rotation_vector[2], 2)
			#rots = round( (rots[0]**2+rots[1]**2+rots[2]**2)**0.5, 2)
			#text = "ID: %s,  Dir: %s" % (self._marker_id, str(rots) )
			#text = "ID: %s; DIR: %d" % ( self._marker_id, self._direction )
			#resizeGLtext = "%s" % ( self._marker_id )
			#myRoundedList = [ round(elem, 2) for elem in self._rotation_vector ]
			#text = "%s %s" % ( self._marker_id, str(myRoundedList) )
			cv2.putText(image, text ,  (p0, p1-30) ,  cv2.FONT_HERSHEY_PLAIN, 0.7, (255, 255, 255), thickness = 3, lineType=cv2.CV_AA)
			cv2.putText(image, text ,  (p0, p1-30) ,  cv2.FONT_HERSHEY_PLAIN, 0.7, (0, 0, 255), thickness = 1, lineType=cv2.CV_AA)
	



	def drawAxis(self,colorImg, camera_matrix, distortion_coeffs):
		RealAxisPoints3D = float32([ [0,0,0], [1,0,0], [0,1,0], [0,0,1] ])
		rotation_vector 		= float32( self._rotation_vector )

		#rots = round(self._rotation_vector[0], 2), round(self._rotation_vector[1], 2), round(self._rotation_vector[2], 2)
		#rots = round( (rots[0]**2+rots[1]**2+rots[2]**2)**0.5, 2)
		#if rots<1.57079632679: RealAxisPoints3D[2][1] = -1

		translation_vector 	= float32( self._translation_vector)
		axis_points, jacobian = cv2.projectPoints(RealAxisPoints3D, rotation_vector,translation_vector,camera_matrix, distortion_coeffs )
		axisPoints = [ ( int(math.ceil(a[0][0])), int(math.ceil(a[0][1])) ) for a in axis_points]
		try:
			cv2.line(colorImg,axisPoints[0], axisPoints[1],(255,0,0),2,8,0)
			cv2.line(colorImg,axisPoints[0], axisPoints[2],(0,0,255),2,8,0)
			cv2.line(colorImg,axisPoints[0], axisPoints[3],(0,255,0),2,8,0)
		except: pass
		