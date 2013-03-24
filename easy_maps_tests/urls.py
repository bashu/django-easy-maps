from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.shortcuts import render_to_response


admin.autodiscover()

def index(request):
    return render_to_response('index.html')


urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
)
