from . import views
from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

 url(r'^upload/$', views.upload, name="upload"),
 url(r'^form-detail/(?P<random_url>[-\w]+)/$', views.form_detail, name="form_detail")
]