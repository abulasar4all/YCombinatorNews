from django.conf.urls import url,include
from stories.views import index, story

urlpatterns = [
	url(r'^$', index),
	url(r'^story/$', story)
]