from django.urls import path
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', TemplateView.as_view(template_name="index.html")),
]
