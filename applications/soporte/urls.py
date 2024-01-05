from django.urls import path
from . import views

app_name='soporte_app'

urlpatterns = [
    path('problema/', views.ProblemaListView.as_view(), name='problema_inicio'),
    path('problema-tabla/', views.ProblemaTabla, name='problema_tabla'),
    path('problema/registrar/', views.ProblemaCreateView.as_view(), name='problema_registrar'),

] 