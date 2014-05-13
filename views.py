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
from omero.rtypes import rint, rstring, wrap
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
	conn=BlitzGateway('__public__','s3cr3t5',host='localhost', port=4064)
	conn.connect()

#	my_expId = conn.getUser().getId()

#	projects = conn.listProjects(my_expId)
#	projects = conn.getObjects("Project")
	

#	groupId = 3 #public group - this may not be necessary if public user is default for public group. 
#	conn.SERVICE_OPTS.setOmeroGroup(groupId)
	projects = conn.listProjects() 		#will only list projects in user's default group - default group for __public__ is public group. Projects can be published by moving them from 'private' group to 'public' group using OMERO.insight

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

	conn=BlitzGateway('__public__','s3cr3t5',host='localhost',port=4064)
	conn.connect()

	project = conn.getObject("Project",projId)
	proj_name = project.getName()
        proj_desc = project.getDescription()	
	dataset_IDs = list(project.listChildren())
#	datasets = []
#	for dsID in dataset_IDs:
#		datasets.append(conn.getObject("Dataset",dsID))

	image_IDs = []
	for dsid in dataset_IDs:
		# code for getting random thumbnail image (using 'rating' of 5 to select good images)
		queryService = conn.getQueryService()
		params = omero.sys.ParametersI()
		params.addLong('dsid', dsid.getId())
		params.addLong('five', 5)
		params.addString('ratingNs', omero.constants.metadata.NSINSIGHTRATING)
		params.theFilter = omero.sys.Filter()
		params.theFilter.limit = wrap(1)

		query = "select i from Image as i"\
        		" left outer join i.datasetLinks as dl join dl.parent as dataset"\
        		" left outer join i.annotationLinks as al join al.child as ann"\
        		" where dataset.id = :dsid"\
        		" and ann.ns = :ratingNs and ann.longValue = :five"

		img = queryService.findByQuery(query, params, conn.SERVICE_OPTS)
		img_id= img.id.val
			
		# end of thumbnail code 
		image_IDs.append( img_id)

	dataset_image_pairs = zip(dataset_IDs,image_IDs)


	return render_to_response('GigaDV/project.html',
		{'proj_name':proj_name,
		'proj_desc':proj_desc,
		'datasets':dataset_image_pairs,
		})	


def dataset(request, projId, dsId,**kwargs):


	conn=BlitzGateway('__public__','s3cr3t5',host='localhost',port=4064)
	conn.connect()

	project = conn.getObject("Project",projId)
	ds= conn.getObject("Dataset",dsId)
	
	return render_to_response('GigaDV/dataset.html',
		{'dataset':ds,
		'project':project,
		})


def image(request, projId, dsId, imId,**kwargs):
	conn=BlitzGateway('__public__','s3cr3t5', host='localhost', port=4064)
	conn.connect()

	project=conn.getObject("Project",projId)
	ds=conn.getObject("Dataset",dsId)
	image=conn.getObject("Image",imId)


	return render_to_response('GigaDV/image.html',
		{'dataset':ds,
		'project':project,
		'image':image,
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


	groupId = image.details.group.id.val


	#5 Z-planes
	z_indexes = [0,int(sizeZ*0.25), int(sizeZ*0.5),int(sizeZ*0.75), sizeZ-1]
	return render_to_response('GigaDV/stack_preview.html',
		{'imageId':imageId,
		'image_name':image_name,
		'z_indexes':z_indexes,
		'groupId':groupId})


