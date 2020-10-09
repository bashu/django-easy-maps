from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = [
    url(r"^admin/", admin.site.urls),
]

urlpatterns += [
    url(r"^$", TemplateView.as_view(template_name="index.html")),
]
