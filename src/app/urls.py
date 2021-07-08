from os import name
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

from core import views

from admin import view_admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', views.HomeView.as_view(), name='home'),
    path('contact/',views.ContactView.as_view(), name='contact'),
    path('nosotros/',views.NosotrosView.as_view(), name='nosotros'),
    path('cart/', include('cart.urls', namespace='cart')),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    
    path('adminprincipal/', view_admin.adminprincipal, name='admin'),
    path('admin_ver_productos/', view_admin.Admin_ver_productos.as_view(), 
         name='admin_ver_productos'),
    path('admin_añadir_productos/', view_admin.Admin_Agregar_productos.as_view(), 
         name='admin_agregar_productos'),
    path('admin_actualizar_productos/<int:pk>/', view_admin.Actualizar_producto.as_view(),
         name='admin_actualizar_productos'),
    path('admin_eliminar_productos/<int:pk>/', view_admin.Eliminar_producto.as_view(),
         name='admin_eliminar_productos'),
    path('admin_ver_proveedores/', view_admin.Admin_ver_proveedores.as_view(), 
        name='admin_ver_proovedores'),
    path('admin_añadir_proveedores/', view_admin.Admin_Agregar_proveedores.as_view(), 
        name='admin_agregar_proovedores'),
    path('admin_actualizar_proovedores/<int:pk>/', view_admin.Actualizar_proveedores.as_view(),
         name='admin_actualizar_proovedores'),
    path('admin_ver_ventas/', view_admin.Admin_ver_ordenes, 
         name='admin_ver_ventas'),
    path('admin_ver_pagos/', view_admin.Admin_ver_pagos.as_view(), 
         name='admin_ver_pagos'),
    path('admin_ver_usuarios/', view_admin.Admin_ver_usuarios, 
         name='admin_ver_usuarios'),
    path('admin_registrar_usuarios/', view_admin.administrador_signup_view , 
         name='admin_registrar_usuarios'),
     
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    