#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


from setuptools import setup

setup(

	name				='py3DSceneEditor',
	version 			='0.0',
	description 		="""""",
	author  			='Ricardo Ribeiro',
	author_email		='ricardojvr@gmail.com',
	license 			='MIT',

	
	packages=[
		'py3DSceneEditor',
		'py3DSceneEditor.Windows',
		'py3DSceneEditor.Windows.Object',
		'py3DSceneEditor.Windows.Camera',
		'py3DSceneEditor.Windows.Camera.Calibrate',
		'py3DSceneEditor.Windows.Camera.FindPosition',
		'py3DSceneEditor.Windows.Camera.SelectRay',],

	package_data={'py3DSceneEditor': ['style.css']},


	#install_requires=[
	#	"pyforms >= 0.1.3",
	#	"pyopengl >= 3.1.0",
	#	"numpy >= 1.6.1"
	#],

	entry_points={
		'console_scripts':['py3DSceneEditorApp=py3DSceneEditor.main:main']
	}
)