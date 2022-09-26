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


def formularioEditar(request, id):
    p = Cliente.objects.get(pk = id)
    contexto = { "cliente": p }
    return render(request, 'transportes/login/editarUsuario.html', contexto)


def actualizarUsuario(request):
    try:
        if request.method == "POST":
            #Obtener la instancia de producto a modificar
            p =  Cliente.objects.get(pk = request.POST["id"])
            
            p.nombre = request.POST["nombre"]
            p.apellido = request.POST["apellido"]
            p.correo = request.POST["correo"]
            p.direccion = request.POST["direccion"]
            p.documento = request.POST["documento"]
            p.fecha_nacimiento = request.POST["fecha_nacimiento"]

            
            p.save()
            messages.success(request, "Producto actualizado correctamente!!")
        else:
            messages.warning(request, "Usted no ha enviado datos...")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarUsuario')


def eliminarUsuario(request, id):
    try:
        p =  Cliente.objects.get(pk = id)
        p.delete()
        messages.success(request, "Producto eliminado correctamente!!")
    except IntegrityError:
        messages.warning(request, "No puede eliminar este producto porque otros registros están relacionados con él....")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarUsuario')
    


#-------------------------BENEFICIARIO--------------------------------------------


def listarBeneficiario(request):
    b = Beneficiarios.objects.all()
    contextob = {'datosB': b}

    return render(request, 'transportes/login/listarBeneficiario.html', contextob)

def registrarBeneficiario(request):
    u = Cliente.objects.all()
    contexto = {'cli': u}
    return render(request, 'transportes/login/registrarBeneficiario.html', contexto)

def guardarBeneficiario(request):
    try:
        if request.method == "POST":
            u =  Cliente.objects.get(pk = request.POST["cliente"])
            q = Beneficiarios(
                cliente = u,
                nombre = request.POST["nombre"],
                apellido = request.POST["apellido"],
                documento = request.POST["documento"],
                fecha_nacimiento = request.POST["fecha_nacimiento"])
            q.save()

            messages.success(request, "Trabajador guardado exitosamente")
        else:
            messages.warning(request, "No se han enviado datos...")

    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarBeneficiario')

def formularioEditarBeneficiario(request, id):
    p = Beneficiarios.objects.get(pk = id)
    c = Cliente.objects.all()
    contexto = { "beneficiario": p, "cli":c }
    return render(request, 'transportes/login/editarBeneficiario.html', contexto)


def actualizarBeneficiario(request):
    try:
        if request.method == "POST":
            #Obtener la instancia de producto a modificar
            p =  Beneficiarios.objects.get(pk = request.POST["id"])
            c =  Cliente.objects.get(pk = request.POST["cliente"])
            p.cliente = c
            p.nombre = request.POST["nombre"]
            p.apellido = request.POST["apellido"]
            p.documento = request.POST["documento"]
            p.fecha_nacimiento = request.POST["fecha_nacimiento"]

            p.save()
            messages.success(request, "Producto actualizado correctamente!!")
        else:
            messages.warning(request, "Usted no ha enviado datos...")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarBeneficiario')


def eliminarBeneficiario(request, id):
    try:
        p =  Beneficiarios.objects.get(pk = id)
        p.delete()
        messages.success(request, "Producto eliminado correctamente!!")
    except IntegrityError:
        messages.warning(request, "No puede eliminar este producto porque otros registros están relacionados con él....")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarBeneficiario')

#--------------------COMENTARIOS----------------------------------------
def listarComentarios(request):
    c = Comentarios.objects.all()
    contextoC = {'datosC': c}

    return render(request, 'transportes/login/listarComentarios.html', contextoC)

def registrarComentarios(request):
    u = Cliente.objects.all()
    contexto = {'cli': u}
    return render(request, 'transportes/login/registrarComentarios.html',contexto)

def guardarComentarios(request):
    try:
        if request.method == "POST":
            u =  Cliente.objects.get(pk = request.POST["cliente"])
            q = Comentarios(
                cliente = u,
                tipo = request.POST["tipo"],
                desc = request.POST["desc"])
            q.save()

            messages.success(request, "Trabajador guardado exitosamente")
        else:
            messages.warning(request, "No se han enviado datos...")

    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarComentarios')

def formularioEditarComentarios(request, id):
    p = Comentarios.objects.get(pk = id)
    c = Cliente.objects.all()
    contexto = { "beneficiario": p, "cli":c }
    return render(request, 'transportes/login/editarComentario.html', contexto)


def actualizarComentarios(request):
    try:
        if request.method == "POST":
            #Obtener la instancia de producto a modificar
            p =  Comentarios.objects.get(pk = request.POST["id"])
            c =  Cliente.objects.get(pk = request.POST["cliente"])
            p.cliente = c
            p.tipo = request.POST["tipo"]
            p.desc = request.POST["desc"]
           
            p.save()
            messages.success(request, "Producto actualizado correctamente!!")
        else:
            messages.warning(request, "Usted no ha enviado datos...")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarComentarios')


def eliminarComentarios(request, id):
    try:
        p = Comentarios.objects.get(pk = id)
        p.delete()
        messages.success(request, "Producto eliminado correctamente!!")
    except IntegrityError:
        messages.warning(request, "No puede eliminar este producto porque otros registros están relacionados con él....")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarBeneficiario')

#--------------------TIPOS DE SERVICIOS----------------------------------------


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


def formularioEditarTiposdeServcios(request, id):
    p = TiposdeServicios.objects.get(pk = id)
    contexto = { "TipoServ": p }
    return render(request, 'transportes/login/editarTiposdeServicios.html', contexto)


def actualizarTiposdeServicios(request):
    try:
        if request.method == "POST":
            #Obtener la instancia de producto a modificar
            p =  TiposdeServicios.objects.get(pk = request.POST["id"])
            
            p.nombre = request.POST["nombre"]
            p.tipo_serv = request.POST["tipo_serv"]
            p.save()
            messages.success(request, "Producto actualizado correctamente!!")
        else:
            messages.warning(request, "Usted no ha enviado datos...")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarTiposdeServicios')


def eliminarTiposdeServicios(request, id):
    try:
        p = TiposdeServicios.objects.get(pk = id)
        p.delete()
        messages.success(request, "Producto eliminado correctamente!!")
    except IntegrityError:
        messages.warning(request, "No puede eliminar este producto porque otros registros están relacionados con él....")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarTiposdeServicios')

#--------------------SERVICIOS----------------------------------------

def listarServicios(request):
    s = Servicios.objects.all()
    contextoS = {'datosS': s}

    return render(request, 'transportes/login/listarServicios.html', contextoS)

def registrarServicios(request):
    u = TiposdeServicios.objects.all()
    contexto = {'TipoServ': u}
    return render(request, 'transportes/login/registrarServicios.html',contexto)

def guardarServicios(request):
    try:
        u =  TiposdeServicios.objects.get(pk = request.POST["tipo_serv"])

        if request.method == "POST":
            q = Servicios(nombre = request.POST["nombre"],tipo_serv = u)
            q.save()

            messages.success(request, "Trabajador guardado exitosamente")
        else:
            messages.warning(request, "No se han enviado datos...")

    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarServicios')


def formularioEditarServicios(request, id):
    p = Servicios.objects.get(pk = id)
    c = TiposdeServicios.objects.all()
    contexto = { "servicios": p, "tipo_serv":c }
    return render(request, 'transportes/login/editarServicios.html', contexto)


def actualizarServicios(request):
    try:
        if request.method == "POST":
            #Obtener la instancia de producto a modificar
            p =  Servicios.objects.get(pk = request.POST["id"])
            c =  TiposdeServicios.objects.get(pk = request.POST["tipo_serv"])
            p.tipo_serv = c
            p.nombre = request.POST["nombre"]
           

            p.save()
            messages.success(request, "Producto actualizado correctamente!!")
        else:
            messages.warning(request, "Usted no ha enviado datos...")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarServicios')


def eliminarServicios(request, id):
    try:
        p =  Servicios.objects.get(pk = id)
        p.delete()
        messages.success(request, "Producto eliminado correctamente!!")
    except IntegrityError:
        messages.warning(request, "No puede eliminar este producto porque otros registros están relacionados con él....")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarBeneficiario')


#--------------------PETICIONES----------------------------------------
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