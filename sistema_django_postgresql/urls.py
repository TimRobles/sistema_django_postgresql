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
    path('datos-globales/', include('applications.datos_globales.urls')),
    path('sede/', include('applications.sede.urls')),
    path('material/', include('applications.material.urls')),
    path('proveedores/', include('applications.proveedores.urls')),
    path('clientes/', include('applications.clientes.urls')),
    path('requerimiento-material/', include('applications.requerimiento_de_materiales.urls')),
    path('oferta-proveedor/', include('applications.oferta_proveedor.urls')),
    path('orden-compra/', include('applications.orden_compra.urls')),
    path('comprobante-compra/', include('applications.comprobante_compra.urls')),
    path('recepcion-compra/', include('applications.recepcion_compra.urls')),
    path('nota-ingreso/', include('applications.nota_ingreso.urls')),
    path('movimiento-almacen/', include('applications.movimiento_almacen.urls')),
    path('encuesta/', include('applications.encuesta.urls')),
    path('aptc/', include('applications.sorteo_aptc.urls')),
    path('activos/', include('applications.activos.urls')),
    path('cotizacion/', include('applications.cotizacion.urls')),
    path('cobranza/', include('applications.cobranza.urls')),
    path('logistica/', include('applications.logistica.urls')),
    path('comprobante-venta/', include('applications.comprobante_venta.urls')),
    path('comprobante-despacho/', include('applications.comprobante_despacho.urls')),
    path('sorteo-webinar/', include('applications.sorteo_webinar.urls')),
    path('envio-clientes/', include('applications.envio_clientes.urls')),
    path('calidad/', include('applications.calidad.urls')),
    path('soporte-sistema/', include('applications.soporte_sistema.urls')),
    path('traslado-producto/', include('applications.traslado_producto.urls')),
    path('muestra/', include('applications.muestra.urls')),
    path('reportes/', include('applications.reportes.urls')),
    path('reportes-panel/', include('applications.reportes_panel.urls')),
    path('nota/', include('applications.nota.urls')),
    path('garantia/', include('applications.garantia.urls')),
    path('contabilidad/', include('applications.contabilidad.urls')),
]

urlpatterns += [url(r'^ftp/(?P<path>.*)', serve, {'document_root': settings.FTP_ROOT})]
urlpatterns += [url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT})]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
