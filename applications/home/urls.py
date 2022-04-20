from django.urls import path
from applications.home.views import (
    ConsultaRucView,
    HomePage
)

app_name = 'home_app'

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('consulta-ruc/<int:ruc>/', ConsultaRucView, name='consulta_ruc'),
]