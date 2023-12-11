"""FacturacionE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from Dashboard.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login'), name='logout'),
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('get_datos_por_ruc/', get_datos_por_ruc, name='get_datos_por_ruc'),
    path('comprobantes/', lista_documentos, name='comprobantes'),
    re_path(r'^descargar_pdf/(?P<codigo>[^/]+)/$', descargar_pdf, name='descargar_pdf'),
    path('descargar_xml/<str:codigo>/', descargar_xml, name='descargar_xml'),
    path('get_precio_producto/', get_precio_producto, name='get_precio_producto'),
    path('factura/',CrearFacturaView.as_view(), name='factura'),
    path('categorias/',categorias, name='categorias'),
    path('sucursales/',sucursales, name='sucursales'),
    path('sucursales/nuevo/',nuevasucursal, name='nuevosucursal'),
    path('sucursales/editar/<int:id>',editarsucursal, name='editarsucursal'),
    path('stock/',stock, name='stock'),
    path('movimientos/ingresos/',ingresos, name='ingresos'),
    path('movimientos/ingresos/nuevo/',CrearIngresoView.as_view(), name='nuevoingreso'),
    path('movimientos/salidas/',salidas, name='salidas'),
    path('movimientos/salidas/nuevo/',CrearSalidaView.as_view(), name='nuevasalida'),
    path('categorias/nuevo/',nuevacategoria, name='nuevacategoria'),
    path('categorias/editar/<int:pk>/', CategoriaUpdateView.as_view(), name='editarcategoria'),
    path('productos/',productos, name='productos'),
    path('productos/nuevo/',nuevoproducto, name='nuevoproducto'),
    path('productos/editar/<int:id>', editarproducto, name='editarproducto'),
    path('boleta/', boleta, name='boleta'),
    path('notacredito/', notacredito, name='notacredito'),
    path('notadebito/', notadebito, name='notadebito'),
    path('clientes/', clientes, name='clientes'),
    path('clientes/nuevo/', nuevocliente, name='nuevocliente'),
    path('clientes/editar/<int:id>', editarcliente, name='editarcliente'),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', custom_login, name='login'),
    path('logout/',custom_logout, name='logout'),
    path('users/', list_users, name='list_users'),
    path('users/edit/<int:user_id>/', edit_user, name='edit_user'),
]
