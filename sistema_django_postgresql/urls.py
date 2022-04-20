
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.static import serve
from django.conf import settings
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('applications.home.urls')),
    path('usuario/', include('applications.usuario.urls')),
    path('sociedad/', include('applications.sociedad.urls')),
]

urlpatterns += [url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT})]