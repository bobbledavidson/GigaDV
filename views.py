#!/usr/bin/env python
# -*- coding: utf-8 -*-
from omero.gateway import *


from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from omeroweb.webgateway import views as webgateway_views
from omeroweb.connector import Server

from omeroweb.webclient.decorators import login_required, render_response
from omeroweb.connector import Connector

from cStringIO import StringIO

import settings
import logging
import traceback
import omero
from omero.rtypes import rint, rstring
import omero.gateway
import random


logger = logging.getLogger(__name__)


try:
    from PIL import Image
except: #pragma: nocover
    try:
        import Image
    except:
        logger.error('No PIL installed, line plots and split channel will fail!')








def index(request,**kwargs):

	
	"""lists all projects with thumbnails"""
	conn=BlitzGateway('root','1234',host='localhost', port=4064)
	conn.connect()

	my_expId = conn.getUser().getId()

	projects = conn.listProjects(my_expId)
#	proj_Ids=[]
#	for project in projects:
#		proj_Ids.append(project.getId())
	
	
	#return HttpResponse("Welcome to GigaDV home-page!")
	return render_to_response('GigaDV/index.html',
		{
		#'projIDs':proj_Ids,
		'projects':projects,
		})


def project(request, projId,**kwargs):
	"""provides details on a specific project"""

	conn=BlitzGateway('root','1234',host='localhost',port=4064)
	conn.connect()

	project = conn.getObject("Project",projId)
	proj_name = project.getName()
        proj_desc = project.getDescription()	
	dataset_IDs = project.listChildren()
#	datasets = []
#	for dsID in dataset_IDs:
#		datasets.append(conn.getObject("Dataset",dsID))

		
	return render_to_response('GigaDV/project.html',
		{'proj_name':proj_name,
		'proj_desc':proj_desc,
		'datasets':dataset_IDs,
		})	


def dataset(request, projId, dsId,**kwargs):


	conn=BlitzGateway('root','1234',host='localhost',port=4064)
	conn.connect()

	project = conn.getObject("Project",projId)
	ds= conn.getObject("Dataset",dsId)
	
	return render_to_response('GigaDV/dataset.html',
		{'dataset':ds,
		'project':project,
		})

def image_view(request,projId, dsId, imageId,**kwargs):
	
	conn=BlitzGateway('root','1234',host='localhost',port=4064)
	conn.connect()

	project=conn.getObject("Project",projId)
	ds=conn.getObject("Dataset",dsId)
	

	return render_to_response('GigaDV/image_view.html',
		{'imageId':imageId,
		'project':project,
		'dataset':ds,
		})


def stack_preview(request,imageId,**kwargs):
	"""Shows a subset of Z-planes for an image """

	conn=BlitzGateway('root','1234',host='localhost',port=4064)
	conn.connect()

	image = conn.getObject("Image", imageId) 	#get image from OMERO
	image_name = image.getName()
	sizeZ =  image.getSizeT()			#get the z dimension

	#5 Z-planes
	z_indexes = [0,int(sizeZ*0.25), int(sizeZ*0.5),int(sizeZ*0.75), sizeZ-1]
	return render_to_response('GigaDV/stack_preview.html',
		{'imageId':imageId,
		'image_name':image_name,
		'z_indexes':z_indexes})


