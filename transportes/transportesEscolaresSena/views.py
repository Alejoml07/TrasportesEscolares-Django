from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse 

#Mensaje tipo cookie temporales 
from django.contrib import messages

#Gestion de errores de base de datos 
from django.db import IntegrityError

from .models import Cliente,Beneficiarios,Comentarios,TiposdeServicios,Servicios,Peticiones,Proveedores


# Create your views here.

def index(request):
    return render(request, 'transportes/index.html')

def listarUsuario(request):
    q = Cliente.objects.all()
    contexto = {'datos': q}

    return render(request, 'transportes/login/listarUsuario.html', contexto)

def registrarUsuario(request):
    return render(request, 'transportes/login/registrarUsuario.html')

def guardarUsuario(request):
    try:
        if request.method == "POST":
            q = Cliente(nombre = request.POST["nombre"],apellido = request.POST["apellido"],correo = request.POST["correo"],direccion = request.POST["direccion"],documento = request.POST["documento"],fecha_nacimiento = request.POST["fecha_nacimiento"])
            q.save()

            messages.success(request, "Trabajador guardado exitosamente")
        else:
            messages.warning(request, "No se han enviado datos...")

    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarUsuario')

def listarBeneficiario(request):
    b = Beneficiarios.objects.all()
    contextob = {'datosB': b}

    return render(request, 'transportes/login/listarBeneficiario.html', contextob)

def registrarBeneficiario(request):
    return render(request, 'transportes/login/registrarBeneficiario.html')

def guardarBeneficiario(request):
    try:
        if request.method == "POST":
            q = Beneficiarios(nombre = request.POST["nombre"],apellido = request.POST["apellido"],documento = request.POST["documento"],fecha_nacimiento = request.POST["fecha_nacimiento"])
            q.save()

            messages.success(request, "Trabajador guardado exitosamente")
        else:
            messages.warning(request, "No se han enviado datos...")

    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarBeneficiario')

def listarComentarios(request):
    c = Comentarios.objects.all()
    contextoC = {'datosC': c}

    return render(request, 'transportes/login/listarComentarios.html', contextoC)

def registrarComentarios(request):
    return render(request, 'transportes/login/registrarComentarios.html')

def guardarComentarios(request):
    try:
        if request.method == "POST":
            q = Comentarios(cliente = request.POST["cliente"],tipo = request.POST["tipo"],desc = request.POST["desc"])
            q.save()

            messages.success(request, "Trabajador guardado exitosamente")
        else:
            messages.warning(request, "No se han enviado datos...")

    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarComentarios')

def listarTiposdeServicios(request):
    t = TiposdeServicios.objects.all()
    contextoT = {'datosT': t}

    return render(request, 'transportes/login/listarTiposdeServicios.html', contextoT)

def registrarTiposdeServicios(request):
    return render(request, 'transportes/login/registrarTiposdeServicios.html')

def guardarTiposdeServicios(request):
    try:
        if request.method == "POST":
            q = TiposdeServicios(nombre = request.POST["nombre"],caracteristicas = request.POST["caracteristicas"])
            q.save()

            messages.success(request, "Trabajador guardado exitosamente")
        else:
            messages.warning(request, "No se han enviado datos...")

    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarTiposdeServicios')

def listarServicios(request):
    s = Servicios.objects.all()
    contextoS = {'datosS': s}

    return render(request, 'transportes/login/listarServicios.html', contextoS)

def registrarServicios(request):
    return render(request, 'transportes/login/registrarServicios.html')

def guardarServicios(request):
    try:
        if request.method == "POST":
            q = Servicios(nombre = request.POST["nombre"],tipo_serv = request.POST["tipo_serv"])
            q.save()

            messages.success(request, "Trabajador guardado exitosamente")
        else:
            messages.warning(request, "No se han enviado datos...")

    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarServicios')

def listarPeticiones(request):
    p = Peticiones.objects.all()
    contextoP = {'datosP': p}

    return render(request, 'transportes/login/listarPeticiones.html', contextoP)

def registrarPeticiones(request):
    return render(request, 'transportes/login/registrarPeticiones.html')

def guardarPeticiones(request):
    try:
        if request.method == "POST":
            q = Peticiones(cliente = request.POST["cliente"],servicios = request.POST["servicios"],direccion = request.POST["direccion"],colegio = request.POST["colegio"],horario = request.POST["horario"],comentario_add = request.POST["comentario_add"])
            q.save()

            messages.success(request, "Trabajador guardado exitosamente")
        else:
            messages.warning(request, "No se han enviado datos...")

    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarPeticiones')

def listarProveedores(request):
    r = Proveedores.objects.all()
    contextoR = {'datosR': r}

    return render(request, 'transportes/login/listarProveedores.html', contextoR)

def registrarProveedores(request):
    return render(request, 'transportes/login/registrarProveedores.html')

def guardarProveedores(request):
    try:
        if request.method == "POST":
            q = Proveedores(nombre = request.POST["nombre"],apellido = request.POST["apellido"],correo = request.POST["correo"],direccion = request.POST["direccion"],documento = request.POST["documento"],fecha_nacimiento = request.POST["fecha_nacimiento"],marca_veh = request.POST["marca_veh"],color_veh = request.POST["color_veh"],documentacion_veh = request.POST["documentacion_veh"])
            q.save()

            messages.success(request, "Trabajador guardado exitosamente")
        else:
            messages.warning(request, "No se han enviado datos...")

    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarProveedores')