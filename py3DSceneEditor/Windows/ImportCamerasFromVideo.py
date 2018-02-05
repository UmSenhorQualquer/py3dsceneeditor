from py3DSceneEditor.Windows.__init__ import *


class ImportCamerasFromVideo(BaseWidget):


	def __init__(self):
		BaseWidget.__init__(self,'Import cameras from video')

		self._video 		= ControlFile('Video')
		self._player 		= ControlPlayer('Player')
		self._step 			= ControlNumber('Frames step')
		self._button 		= ControlButton('Run tracking')
		self._events		= ControlEventTimeline('Events timeline')

		self._formset = [ ('_video','_step','_button'), '_player','_events']

		self._video.changed_event = self.__videoChangedEvent
		self._player.process_frame_event = self.__process_frame
		self._step.changed_event  = self.__framesStepChange
		self._events.pointerChanged = self.__eventPointerChanged
		self._changePointer = True

	def __eventPointerChanged(self):
		if self._changePointer: 
			self._player.video_index = self._events.value
			self._player.refresh()

	def __process_frame(self, frame):
		self._changePointer = False
		self._events.value = self._player.video_index
		self._changePointer = True
		return frame

	def __videoChangedEvent(self):
		self._player.value = self._video.value
		self._events.max = self._player.max

	def __framesStepChange(self):
		pass

###########################################################################################
###########################################################################################
###########################################################################################

if __name__ == "__main__":	 app.start_app( ImportCamerasFromVideo )