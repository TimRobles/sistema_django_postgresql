from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('applications.home.urls')),
    path('sorteo/', include('applications.sorteo.urls')),
    path('usuario/', include('applications.usuario.urls')),
    path('sociedad/', include('applications.sociedad.urls')),
    path('recepcion/', include('applications.recepcion.urls')),
    path('colaborador/', include('applications.colaborador.urls')),
    path('datos_globales/', include('applications.datos_globales.urls')),
    path('sede/', include('applications.sede.urls')),
    path('material/', include('applications.material.urls')),
    path('proveedores/', include('applications.proveedores.urls')),
    path('clientes/', include('applications.clientes.urls')),
    path('requerimiento_material/', include('applications.requerimiento_de_materiales.urls')),
    path('oferta_proveedor/', include('applications.oferta_proveedor.urls')),
    path('orden_compra/', include('applications.orden_compra.urls')),
    path('comprobante_compra/', include('applications.comprobante_compra.urls')),
    path('recepcion_compra/', include('applications.recepcion_compra.urls')),
    path('nota_ingreso/', include('applications.nota_ingreso.urls')),
    path('movimiento_almacen/', include('applications.movimiento_almacen.urls')),
    path('encuesta/', include('applications.encuesta.urls')),
    path('aptc/', include('applications.sorteo_aptc.urls')),
    path('activos/', include('applications.activos.urls')),
    path('cotizacion/', include('applications.cotizacion.urls')),
    path('cobranza/', include('applications.cobranza.urls')),
    path('logistica/', include('applications.logistica.urls')),

]

urlpatterns += [url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT})]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
