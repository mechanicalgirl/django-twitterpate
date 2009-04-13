from django.conf.urls.defaults import *
from django.contrib.comments.models import Comment
from django.views.generic.simple import direct_to_template

from twitterpate import views

urlpatterns = patterns('',
    url(r'^id/(?P<id>\w+)/*$',          views.show_id,        name='view_by_id'),
    url(r'^all/*$',                     views.show_all,       name='show_all'),
    url(r'^$',                          views.show_all,       name='show_all'),
)

