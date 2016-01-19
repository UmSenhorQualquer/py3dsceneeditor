__author__ 		= "Ricardo Jorge Vieira Ribeiro"
__copyright__ 	= "Copyright 2013, Scientific Software Platform - Neuroscience Programme - Champalimaud Foundation"
__license__ 	= "GNU GPL"
__version__ 	= "1.0.0"
__maintainer__ 	= "Ricardo Jorge Vieira Ribeiro"
__email__ 		= ["ricardo.ribeiro@neuro.fchampalimaud.org", "ricardojvr@gmail.com"]
__status__ 		= "Production"

import cv2
from math import *
from numpy import *
from operator import *
from py3DSceneEditor.Windows.Camera.FindPosition.MarkerRectangle import MarkerRectangle, DistanceBetween

class MarkerDetector(object):
	"""
	Class responsible for the ARMarkers search
	"""
	
	def __init__(self, 
		camera_matrix,
		distortion_coeffs,
		svm_file_model = "model.xml",
		algo=0,
		size=1.0,
		contour_approx=8.0):

		self._camera_matrix 	= camera_matrix
		self._distortion_coeffs = distortion_coeffs
		self.ALGO 				= algo
		self.MARKER_OUTER_SIZE 	= size
		self.COUNTER_APPROXIMATION = contour_approx
		self._model = cv2.SVM(); self._model.load(svm_file_model)

		self.REAL_MARKER_CORNERS = float32([(0.0, 0.0, 0.0),
			(self.MARKER_OUTER_SIZE, 0.0, 0.0),
			(self.MARKER_OUTER_SIZE,self.MARKER_OUTER_SIZE, 0.0),
			(0.0, self.MARKER_OUTER_SIZE,0.0)])
	


	###############################################################
	###############################################################
	###############################################################

	

	def firstRectanglesFilter(self, image):
		"""
		Find rectangles in an image
		"""
		results = []
		contours, hierarchy = cv2.findContours( 
			image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		
		for i, contour in enumerate(contours):
			contour = cv2.approxPolyDP(contour, self.COUNTER_APPROXIMATION, True)
			if  len(contour)==4 and \
				cv2.contourArea(contour) > 100 and \
				cv2.isContourConvex(contour):
				results.append(contour)

		return results

	def secondRectanglesFilter(self, image, contours):

		results = []
		for contour in contours:
			dx, dy, dw, dh = cv2.boundingRect(contour)
			x1, y1, x2, y2 = dx, dy, dx+dw, dy+dh
			center = dx+dw/2, dy+dh/2

			thresh = self._thresh_image[y1:y2, x1:x2]

			rectangle = MarkerRectangle( 
				self._original_image, 
				thresh, 
				contour,
				(dx,dy), 
				center, 
				self._model )
			if rectangle._marker_id>0:
				results.append(rectangle)

		return results


	def find_rectangles(self, image):
		squares = self.firstRectanglesFilter(image)
		criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
		new_squares = []
		for s in squares:
			c = float32(s)
			cv2.cornerSubPix(self._original_image, c,(20,20),(10,10), criteria)
			new_squares.append(c)
		
		results = self.secondRectanglesFilter(image, squares)
		return results
	    		
	###############################################################
	###############################################################
	###############################################################

	def estimate_markers_transformations(self, rectangles, camera_matrix, distortion_coeffs):
		for rect in rectangles:
			if rect._contour==None: continue
			rvecs, tvecs = rect._rvecs, rect._tvecs
			if rvecs!=None and tvecs!=None: 
				if self.ALGO==0: 
					ret, rvecs, tvecs = cv2.solvePnP( 
						self.REAL_MARKER_CORNERS, float32(rect._contour), camera_matrix, 
						distortion_coeffs, rvecs, tvecs, True)
				else: 
					rvecs, tvecs, ret = cv2.solvePnPRansac( 
						self.REAL_MARKER_CORNERS, float32(rect._outer_corners), 
						camera_matrix, distortion_coeffs, rvecs, tvecs, useExtrinsicGuess=True)
			else: 
				if self.ALGO==0: 
					ret, rvecs, tvecs = cv2.solvePnP( self.REAL_MARKER_CORNERS, 
						float32(rect._contour), camera_matrix, distortion_coeffs)
				else: 
					rvecs, tvecs, ret = cv2.solvePnPRansac( self.REAL_MARKER_CORNERS, 
						float32(rect._contour), camera_matrix, distortion_coeffs)
				
			rect._rvecs = rvecs
			rect._tvecs = tvecs
			rect._translation_vector = 	[tvecs[0][0], tvecs[1][0], tvecs[2][0]]
			rect._rotation_vector = 	[rvecs[0][0], rvecs[1][0], rvecs[2][0]]
		return rectangles

	

	###############################################################
	###############################################################
	###############################################################

	def process(self, original, image):
		self._original_image = original
		self._thresh_image 	 = image
		rectangles = self.find_rectangles(image)
		if len(rectangles)>0:   rectangles = self.estimate_markers_transformations(rectangles, self._camera_matrix, self._distortion_coeffs)
		return rectangles






if __name__ == "__main__":

	capture = cv2.VideoCapture('/home/ricardo/subversion/MEShTracker/other/flies/right_final.avi')
	#capture = cv2.VideoCapture('/home/ricardo/subversion/MEShTracker/other/flies/left_final.avi')

	camera_matrix 			= matrix([[ 973.83868801,0.,667.4617181 ],[0.,973.55147583,542.32850545],[0.,0.,1.]])
	distortion_coefficients = array([-3.55507046e-01, 1.76486050e-01, 1.65274132e-03, -1.38058855e-04, -5.18798911e-02])
	
	marker_detector = MarkerDetector(
		camera_matrix, 
		distortion_coefficients, algo=0)
	
	capture.set(cv2.CAP_PROP_POS_FRAMES, 243)

	res = True
	while res:
		res, image = capture.read(); 
		if not res: break

		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY )
		res, thresh = cv2.threshold( gray, 60, 255, cv2.THRESH_BINARY_INV )
		#res, thresh = cv2.threshold( gray, 170, 255, cv2.THRESH_BINARY_INV )

		rectangles = marker_detector.process(gray,thresh)
		
		for rect in rectangles: 
			rect.draw( image )
			if rect._marker_id>0: 
				rect.drawAxis( image, camera_matrix, distortion_coefficients )


		cv2.imshow("Capture", image)
		key = cv2.waitKey(1)
		if key == ord('q'):  break
