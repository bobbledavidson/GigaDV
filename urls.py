from  django.conf.urls.defaults import *
from GigaDV import views

urlpatterns= patterns('django.views.generic.simple',url(r'^$',views.index,name='GigaDV_index'),
)
