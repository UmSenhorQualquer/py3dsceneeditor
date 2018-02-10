#!/usr/bin/python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('py3DSceneEditor/__init__.py', 'r') as fd:
	__version__ 	= eval(fd.readline().split('=')[1])
	__author__      = eval(fd.readline().split('=')[1])
	__credits__     = eval(fd.readline().split('=')[1])
	__license__     = eval(fd.readline().split('=')[1])
	__maintainer__  = eval(fd.readline().split('=')[1])
	__email__       = eval(fd.readline().split('=')[1])
	__status__      = eval(fd.readline().split('=')[1])

setup(
	name				='Python 3D scene editor',
	version 			=__version__,
	description 		="""This application is used to construct 3D scenes to be used with the Python 3D Engine.""",
	author  			=__author__,
	author_email		=__email__,
	license 			=__license__,

	packages=find_packages(),


	package_data={'py3DSceneEditor': ['style.css']},
	entry_points={
		'console_scripts':['py3DSceneEditorApp=py3DSceneEditor:__main__']
	}
)