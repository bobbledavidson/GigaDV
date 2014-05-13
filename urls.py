from  django.conf.urls.defaults import *
from GigaDV import views

#copied from omeroweb/urls.py in the hopes of enabling static files
#from django.views.static import serve
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns= patterns('django.views.generic.simple',
	url(r'^$',views.index,name='GigaDV_index'),
	url(r'^project/(?P<projId>[0-9]+)/$',views.project,name='GigaDV_publication'),
	url(r'^project/(?P<projId>[0-9]+)/dataset/(?P<dsId>[0-9]+)/$',views.dataset,name='GigaDV_dataset'),
	url(r'^project/(?P<projId>[0-9]+)/dataset/(?P<dsId>[0-9]+)/image_view/(?P<imageId>[0-9]+)/$',views.image_view,name='GigaDV_image_view'),
	url(r'^stack_preview/(?P<imageId>[0-9]+)/$',views.stack_preview,name='GigaDV_stack_preview'),
	url(r'^project/(?P<projId>[0-9]+)/dataset/(?P<dsId>[0-9]+)/image/(?P<imId>[0-9]+)/$',views.image,name='GigaDV_image'),	
)
