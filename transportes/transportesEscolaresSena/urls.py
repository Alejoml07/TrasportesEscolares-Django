from django.urls import path
from . import views


app_name= "transportes"
urlpatterns = [
    path('', views.index, name = "index"),
    path('listarUsuarios/', views.listarUsuario, name = "listarUsuario"),
    path('registrarUsuario/', views.registrarUsuario, name = "registrarUsuario"),
    path('guardarUsuario/', views.guardarUsuario, name = "guardarUsuario"),
    path('listarBeneficiario/', views.listarBeneficiario, name = "listarBeneficiario"),
    path('registrarBeneficiario/', views.registrarBeneficiario, name = "registrarBeneficiario"),
    path('guardarBeneficiario/', views.guardarBeneficiario, name = "guardarBeneficiario"),
    path('listarComentarios/', views.listarComentarios, name = "listarComentarios"),
    path('registrarComentarios/', views.registrarComentarios, name = "registrarComentarios"),
    path('guardarComentarios/', views.guardarComentarios, name = "guardarComentarios"),
    path('listarTiposdeServicios/', views.listarTiposdeServicios, name = "listarTiposdeServicios"),
    path('registrarTiposdeServicios/', views.registrarTiposdeServicios, name = "registrarTiposdeServicios"),
    path('guardarTiposdeServicios/', views.guardarTiposdeServicios, name = "guardarTiposdeServicios"),
    path('listarServicios/', views.listarServicios, name = "listarServicios"),
    path('registrarServicios/', views.registrarServicios, name = "registrarServicios"),
    path('guardarServicios/', views.guardarServicios, name = "guardarServicios"),
    path('listarPeticiones/', views.listarPeticiones, name = "listarPeticiones"),
    path('registrarPeticiones/', views.registrarPeticiones, name = "registrarPeticiones"),
    path('guardarPeticiones/', views.guardarPeticiones, name = "guardarPeticiones"),
    path('listarProveedores/', views.listarProveedores, name = "listarProveedores"),
    path('registrarProveedores/', views.registrarProveedores, name = "registrarProveedores"),
    path('guardarProveedores/', views.guardarProveedores, name = "guardarProveedores"),
   
   


]