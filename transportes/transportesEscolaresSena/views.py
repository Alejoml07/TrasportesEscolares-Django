from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse 

#Mensaje tipo cookie temporales 
from django.contrib import messages

#Gestion de errores de base de datos 
from django.db import IntegrityError

from .models import Cliente,Beneficiarios,Comentarios,TiposdeServicios,Servicios,Peticiones,Proveedores, Vehiculo

from django.db.models import Q

from django.core.paginator import Paginator


# Create your views here.

def index(request):
    login = request.session.get('logueo', False)
    if login:
        return render(request, 'transportes/index.html')
    else:
        messages.warning(request, "Inicie sesión primero...")
        return redirect('transportes:loginFormulario')

def loginFormulario(request):
        return render(request, 'transportes/login/login.html')


def login(request):
    if request.method == "POST":
        try:
            user = request.POST["usuario"]
            passw = request.POST["clave"]

            q = Cliente.objects.get(usuario = user, clave = passw)
            # crear la sesión
            request.session["logueo"] = [q.nombre, q.apellido, q.rol, q.id, q.get_rol_display()]

            messages.success(request, "Bienvenido!!")
            return redirect('transportes:index')     

        except Cliente.DoesNotExist:
            messages.error(request, "Usuario o contraseña incorrectos...")
            return redirect('transportes:loginFormulario')
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect('transportes:loginFormulario')
    else:
        messages.warning(request, "Usted no ha enviado datos...")
        return redirect('transportes:loginFormulario')

def logout(request):
    try:
        del request.session["logueo"]
        messages.success(request, "Sesión cerrada correctamente!!")
        return redirect('transportes:index')
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect('transportes:index')

def listarUsuario(request):
     #Obtener la sesión
    login = request.session.get('logueo', False)

    if login and (login[2] == "A" or login[2] == "C"):
        q = Cliente.objects.all()
        paginator = Paginator(q, 3) # Mostrar 3 registros por página...
        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        q = paginator.get_page(page_number)
        contexto = {'datos': q}
        return render(request, 'transportes/login/usuarios/listarUsuario.html', contexto)
    else:
        if login and (login[2] != "A" and login[2] != "C"):
            messages.warning(request, "Usted no tiene autorización para acceder al módulo...")
            return redirect('transportes:index')
        else:
            messages.warning(request, "Inicie sesión primero...")
            return redirect('transportes:loginFormulario')


def registrarUsuario(request):
    return render(request, 'transportes/login/usuarios/registrarUsuario.html')

def guardarUsuario(request):
    try:
        if request.method == "POST":
            q = Cliente(nombre = request.POST["nombre"],apellido = request.POST["apellido"],correo = request.POST["correo"],direccion = request.POST["direccion"],documento = request.POST["documento"],fecha_nacimiento = request.POST["fecha_nacimiento"])
            q.save()

            messages.success(request, "Usuario guardado exitosamente")
        else:
            messages.warning(request, "No se han enviado datos...")

    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarUsuario')


def formularioEditar(request, id):
    p = Cliente.objects.get(pk = id)
    contexto = { "cliente": p }
    return render(request, 'transportes/login/usuarios/editarUsuario.html', contexto)


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
            messages.success(request, "Usuario actualizado correctamente!!")
        else:
            messages.warning(request, "Usted no ha enviado datos...")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarUsuario')


def eliminarUsuario(request, id):
    try:
        p =  Cliente.objects.get(pk = id)
        p.delete()
        messages.success(request, "Usuario eliminado correctamente!!")
    except IntegrityError:
        messages.warning(request, "No puede eliminar este producto porque otros registros están relacionados con él....")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarUsuario')

def buscarProducto(request):
    
    if request.method == "POST":
        dato = request.POST["buscar"]
        q = Cliente.objects.filter( Q(nombre__icontains = dato))
        
        paginator = Paginator(q, 3) # Mostrar 3 registros por página...

        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        q = paginator.get_page(page_number)
        
        contexto = { "datos": q }
        return render(request, 'transportes/login/usuarios/listar_Usuario_ajax.html', contexto)
    else:
        messages.error(request, "Error no envió datos...")
        return redirect('transportes:listarUsuario')
    


#-------------------------BENEFICIARIO--------------------------------------------


def listarBeneficiario(request):
    login = request.session.get('logueo', False)

    if login and (login[2] == "A" or login[2] == "C"):
        b = Beneficiarios.objects.all()
        paginator = Paginator(b, 3) # Mostrar 3 registros por página...

        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        b = paginator.get_page(page_number)
        contextob = {'datosB': b}

        return render(request, 'transportes/login/beneficiarios/listarBeneficiario.html', contextob)
    else:
        if login and (login[2] != "A" and login[2] != "C"):
            messages.warning(request, "Usted no tiene autorización para acceder al módulo...")
            return redirect('transportes:index')
        else:
            messages.warning(request, "Inicie sesión primero...")
            return redirect('transportes:loginFormulario')

def registrarBeneficiario(request):
    u = Cliente.objects.all()
    contexto = {'cli': u}
    return render(request, 'transportes/login/beneficiarios/registrarBeneficiario.html', contexto)

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

            messages.success(request, "Beneficiario guardado exitosamente")
        else:
            messages.warning(request, "No se han enviado datos...")

    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarBeneficiario')

def formularioEditarBeneficiario(request, id):
    p = Beneficiarios.objects.get(pk = id)
    c = Cliente.objects.all()
    contexto = { "beneficiario": p, "cli":c }
    return render(request, 'transportes/login/beneficiarios/editarBeneficiario.html', contexto)


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
            messages.success(request, "Beneficiario actualizado correctamente!!")
        else:
            messages.warning(request, "Usted no ha enviado datos...")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarBeneficiario')


def eliminarBeneficiario(request, id):
    try:
        p =  Beneficiarios.objects.get(pk = id)
        p.delete()
        messages.success(request, "Beneficiario eliminado correctamente!!")
    except IntegrityError:
        messages.warning(request, "No puede eliminar este producto porque otros registros están relacionados con él....")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarBeneficiario')

def buscarBeneficiario(request):
    
    if request.method == "POST":
        dato = request.POST["buscar"]
        q = Beneficiarios.objects.filter( Q(nombre__icontains = dato))
        
        paginator = Paginator(q, 3) # Mostrar 3 registros por página...

        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        q = paginator.get_page(page_number)
        
        contexto = { "datosB": q }
        return render(request, 'transportes/login/beneficiarios/listar_Beneficiario_ajax.html', contexto)
    else:
        messages.error(request, "Error no envió datos...")
        return redirect('transportes:listarBeneficiario')

#--------------------COMENTARIOS----------------------------------------
def listarComentarios(request):
    login = request.session.get('logueo', False)

    if login:
        c = Comentarios.objects.all()
        paginator = Paginator(c, 3) # Mostrar 3 registros por página...

        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        c = paginator.get_page(page_number)
        contextoC = {'datosC': c}

        return render(request, 'transportes/login/comentarios/listarComentarios.html', contextoC)
    else:
        messages.warning(request, "Inicie sesión primero...")
        return redirect('transportes:loginFormulario')

def registrarComentarios(request):
    u = Cliente.objects.all()
    p = Proveedores.objects.all()
    contexto = {'cli': u, 'proveedores':p}
    return render(request, 'transportes/login/comentarios/registrarComentarios.html',contexto)

def guardarComentarios(request):
    try:
        if request.method == "POST":
            u =  Cliente.objects.get(pk = request.POST["cliente"])
            p =  Proveedores.objects.get(pk = request.POST["Proveedores"])

            q = Comentarios(
                cliente = u,
                proveedores = p,
                tipo = request.POST["tipo"],
                desc = request.POST["desc"])
            q.save()

            messages.success(request, "Comentario guardado exitosamente")
        else:
            messages.warning(request, "No se han enviado datos...")

    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarComentarios')

def formularioEditarComentarios(request, id):
    p = Comentarios.objects.get(pk = id)
    c = Cliente.objects.all()
    contexto = { "beneficiario": p, "cli":c }
    return render(request, 'transportes/login/comentarios/editarComentario.html', contexto)


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
            messages.success(request, "Comentario actualizado correctamente!!")
        else:
            messages.warning(request, "Usted no ha enviado datos...")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarComentarios')


def eliminarComentarios(request, id):
    try:
        p = Comentarios.objects.get(pk = id)
        p.delete()
        messages.success(request, "Comentario eliminado correctamente!!")
    except IntegrityError:
        messages.warning(request, "No puede eliminar este producto porque otros registros están relacionados con él....")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarComentarios')

def buscarComentarios(request):
    
    if request.method == "POST":
        dato = request.POST["buscar"]
        q = Comentarios.objects.filter( Q(tipo__icontains = dato))
        
        paginator = Paginator(q, 3) # Mostrar 3 registros por página...

        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        q = paginator.get_page(page_number)
        
        contexto = { "datosC": q }
        return render(request, 'transportes/login/comentarios/listar_Comentarios_ajax.html', contexto)
    else:
        messages.error(request, "Error no envió datos...")
        return redirect('transportes:listarComentarios')

#--------------------TIPOS DE SERVICIOS----------------------------------------


def listarTiposdeServicios(request):
    t = TiposdeServicios.objects.all()
    paginator = Paginator(t, 3) # Mostrar 3 registros por página...

    page_number = request.GET.get('page')
    #Sobreescribir la salida de la consulta.......
    t = paginator.get_page(page_number)
    contextoT = {'datosT': t}

    return render(request, 'transportes/login/tipodeservicios/listarTiposdeServicios.html', contextoT)

def registrarTiposdeServicios(request):
    return render(request, 'transportes/login/tipodeservicios/registrarTiposdeServicios.html')

def guardarTiposdeServicios(request):
    try:
        if request.method == "POST":
            q = TiposdeServicios(nombre = request.POST["nombre"],caracteristicas = request.POST["caracteristicas"])
            q.save()

            messages.success(request, "Tipo de servicio guardado exitosamente")
        else:
            messages.warning(request, "No se han enviado datos...")

    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarTiposdeServicios')


def formularioEditarTiposdeServcios(request, id):
    p = TiposdeServicios.objects.get(pk = id)
    contexto = { "TipoServ": p }
    return render(request, 'transportes/login/tipodeservicios/editarTiposdeServicios.html', contexto)


def actualizarTiposdeServicios(request):
    try:
        if request.method == "POST":
            #Obtener la instancia de producto a modificar
            p =  TiposdeServicios.objects.get(pk = request.POST["id"])
            
            p.nombre = request.POST["nombre"]
            p.tipo_serv = request.POST["tipo_serv"]
            p.save()
            messages.success(request, "Tipo de servicio actualizado correctamente!!")
        else:
            messages.warning(request, "Usted no ha enviado datos...")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarTiposdeServicios')


def eliminarTiposdeServicios(request, id):
    try:
        p = TiposdeServicios.objects.get(pk = id)
        p.delete()
        messages.success(request, "Tipo de servicio eliminado correctamente!!")
    except IntegrityError:
        messages.warning(request, "No puede eliminar este producto porque otros registros están relacionados con él....")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarTiposdeServicios')

def buscarTiposdeServicios(request):
    
    if request.method == "POST":
        dato = request.POST["buscar"]
        q = TiposdeServicios.objects.filter( Q(nombre__icontains = dato))
        
        paginator = Paginator(q, 3) # Mostrar 3 registros por página...

        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        q = paginator.get_page(page_number)
        
        contexto = { "datosT": q }
        return render(request, 'transportes/login/tipodeservicios/listar_TiposdeServicios_ajax.html', contexto)
    else:
        messages.error(request, "Error no envió datos...")
        return redirect('transportes:listarTiposdeServicios')

#--------------------SERVICIOS----------------------------------------

def listarServicios(request):
    login = request.session.get('logueo', False)
    if login:
        s = Servicios.objects.all()
        paginator = Paginator(s, 3) # Mostrar 3 registros por página...

        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        s = paginator.get_page(page_number)
        contextoS = {'datosS': s}

        return render(request, 'transportes/login/servicios/listarServicios.html', contextoS)
    else:
        messages.warning(request, "Inicie sesión primero...")
        return redirect('transportes:loginFormulario')

def registrarServicios(request):
    u = TiposdeServicios.objects.all()
    contexto = {'TipoServ': u}
    return render(request, 'transportes/login/servicios/registrarServicios.html',contexto)

def guardarServicios(request):
    try:
        u =  TiposdeServicios.objects.get(pk = request.POST["tipo_serv"])

        if request.method == "POST":
            q = Servicios(nombre = request.POST["nombre"],tipo_serv = u)
            q.save()

            messages.success(request, "Servicio guardado exitosamente")
        else:
            messages.warning(request, "No se han enviado datos...")

    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarServicios')


def formularioEditarServicios(request, id):
    p = Servicios.objects.get(pk = id)
    c = TiposdeServicios.objects.all()
    contexto = { "servicios": p, "tipo_serv":c }
    return render(request, 'transportes/login/servicios/editarServicios.html', contexto)


def actualizarServicios(request):
    try:
        if request.method == "POST":
            #Obtener la instancia de producto a modificar
            p =  Servicios.objects.get(pk = request.POST["id"])
            c =  TiposdeServicios.objects.get(pk = request.POST["tipo_serv"])
            p.tipo_serv = c
            p.nombre = request.POST["nombre"]
           

            p.save()
            messages.success(request, "Servicio actualizado correctamente!!")
        else:
            messages.warning(request, "Usted no ha enviado datos...")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarServicios')


def eliminarServicios(request, id):
    try:
        p =  Servicios.objects.get(pk = id)
        p.delete()
        messages.success(request, "Servicio eliminado correctamente!!")
    except IntegrityError:
        messages.warning(request, "No puede eliminar este producto porque otros registros están relacionados con él....")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarServicios')

def buscarServicios(request):
    
    if request.method == "POST":
        dato = request.POST["buscar"]
        q = Servicios.objects.filter( Q(nombre__icontains = dato))
        
        paginator = Paginator(q, 3) # Mostrar 3 registros por página...

        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        q = paginator.get_page(page_number)
        
        contexto = { "datosS": q }
        return render(request, 'transportes/login/servicios/listar_Servicios_ajax.html', contexto)
    else:
        messages.error(request, "Error no envió datos...")
        return redirect('transportes:listarServicios')



#--------------------PETICIONES----------------------------------------
def listarPeticiones(request):
    login = request.session.get('logueo', False)

    if login and (login[2] == "A" or login[2] == "C"):
        p = Peticiones.objects.all()
        paginator = Paginator(p, 3) # Mostrar 3 registros por página...

        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        p = paginator.get_page(page_number)
        contextoP = {'datosP': p}

        return render(request, 'transportes/login/peticiones/listarPeticiones.html', contextoP)
    else:
        if login and (login[2] != "A" and login[2] != "C"):
            messages.warning(request, "Usted no tiene autorización para acceder al módulo...")
            return redirect('transportes:index')
        else:
            messages.warning(request, "Inicie sesión primero...")
            return redirect('transportes:loginFormulario')

def registrarPeticiones(request):
    c = Cliente.objects.all()
    s = Servicios.objects.all()
    contexto = {'cli':c,'servicios':s}
    return render(request, 'transportes/login/peticiones/registrarPeticiones.html',contexto)

def guardarPeticiones(request):
    try:
        c =  Cliente.objects.get(pk = request.POST["cliente"])
        s =  Servicios.objects.get(pk = request.POST["servicios"])


        if request.method == "POST":
            q = Peticiones(
                cliente = c,
                servicios = s,
                direccion = request.POST["direccion"],
                colegio = request.POST["colegio"],
                horario = request.POST["horario"],
                comentario_add = request.POST["comentario_add"])
            q.save()

            messages.success(request, "Peticion guardado exitosamente")
        else:
            messages.warning(request, "No se han enviado datos...")

    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarPeticiones')


def formularioEditarPeticiones(request, id):
    p = Peticiones.objects.get(pk = id)
    s = Servicios.objects.all()
    c = Cliente.objects.all()
    contexto = { "peticiones": p, "cli":c, 'servicios':s }
    return render(request, 'transportes/login/peticiones/editarPeticiones.html', contexto)


def actualizarPeticiones(request):
    try:
        if request.method == "POST":
            #Obtener la instancia de producto a modificar
            p =  Peticiones.objects.get(pk = request.POST["id"])
            s = Servicios.objects.get(pk = request.POST["servicios"])
            c = Cliente.objects.get(pk = request.POST["cliente"])


            p.cliente = c
            p.servicios = s
            p.direccion = request.POST["direccion"]
            p.colegio = request.POST["colegio"]
            p.horario = request.POST["horario"]
            p.comentario_add = request.POST["comentario_add"]
           

            p.save()
            messages.success(request, "Peticion actualizado correctamente!!")
        else:
            messages.warning(request, "Usted no ha enviado datos...")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarPeticiones')


def eliminarPeticiones(request, id):
    try:
        p =  Peticiones.objects.get(pk = id)
        p.delete()
        messages.success(request, "Peticion eliminado correctamente!!")
    except IntegrityError:
        messages.warning(request, "No puede eliminar este producto porque otros registros están relacionados con él....")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarPeticiones')

def buscarPeticiones(request):
    
    if request.method == "POST":
        dato = request.POST["buscar"]
        q = Peticiones.objects.filter( Q(colegio__icontains = dato ) |Q(direccion__icontains = dato ))
        
        paginator = Paginator(q, 3) # Mostrar 3 registros por página...

        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        q = paginator.get_page(page_number)
        
        contexto = { "datosP": q }
        return render(request, 'transportes/login/peticiones/listar_Peticiones_ajax.html', contexto)
    else:
        messages.error(request, "Error no envió datos...")
        return redirect('transportes:listarPeticiones')


#--------------------PROVEEDORES----------------------------------------

def listarProveedores(request):
    login = request.session.get('logueo', False)

    if login and (login[2] == "A" or login[2] == "P"):
        r = Proveedores.objects.all()
        paginator = Paginator(r, 3) # Mostrar 3 registros por página...

        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        r = paginator.get_page(page_number)
        contextoR = {'datosR': r}

        return render(request, 'transportes/login/proveedores/listarProveedores.html', contextoR)
    else:
        if login and (login[2] != "A" and login[2] != "P"):
            messages.warning(request, "Usted no tiene autorización para acceder al módulo...")
            return redirect('transportes:index')
        else:
            messages.warning(request, "Inicie sesión primero...")
            return redirect('transportes:loginFormulario')


def registrarProveedores(request):
    return render(request, 'transportes/login/proveedores/registrarProveedores.html')

def guardarProveedores(request):
    try:
        if request.method == "POST":
            q = Proveedores(
                nombre = request.POST["nombre"],
                apellido = request.POST["apellido"],
                correo = request.POST["correo"],
                direccion = request.POST["direccion"],
                documento = request.POST["documento"],
                fecha_nacimiento = request.POST["fecha_nacimiento"],
                marca_veh = request.POST["marca_veh"],
                color_veh = request.POST["color_veh"],
                documentacion_veh = request.POST["documentacion_veh"])
            q.save()

            messages.success(request, "Proveedor guardado exitosamente")
        else:
            messages.warning(request, "No se han enviado datos...")

    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarProveedores')

def formularioEditarProveedores(request, id):
    p = Proveedores.objects.get(pk = id)
    contexto = { "proveedores": p }
    return render(request, 'transportes/login/proveedores/editarProveedores.html', contexto)


def actualizarProveedores(request):
    try:
        if request.method == "POST":
            #Obtener la instancia de producto a modificar
            p =  Proveedores.objects.get(pk = request.POST["id"])
            
            p.nombre = request.POST["nombre"]
            p.apellido = request.POST["apellido"]
            p.correo = request.POST["correo"]
            p.direccion = request.POST["direccion"]
            p.documento = request.POST["documento"]
            p.fecha_nacimiento = request.POST["fecha_nacimiento"]
            p.marca_veh = request.POST["marca_veh"]
            p.color_veh = request.POST["color_veh"]
            p.documentacion_veh = request.POST["documentacion_veh"]

            
            p.save()
            messages.success(request, "Proveedor actualizado correctamente!!")
        else:
            messages.warning(request, "Usted no ha enviado datos...")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarProveedores')


def eliminarProveedores(request, id):
    try:
        p =  Proveedores.objects.get(pk = id)
        p.delete()
        messages.success(request, "Proveedor eliminado correctamente!!")
    except IntegrityError:
        messages.warning(request, "No puede eliminar este producto porque otros registros están relacionados con él....")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarProveedores')

def buscarProveedores(request):
    
    if request.method == "POST":
        dato = request.POST["buscar"]
        q = Proveedores.objects.filter( Q(nombre__icontains = dato ) )
        
        paginator = Paginator(q, 3) # Mostrar 3 registros por página...

        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        q = paginator.get_page(page_number)
        
        contexto = { "datosR": q }
        return render(request, 'transportes/login/proveedores/listar_Proveedores_ajax.html', contexto)
    else:
        messages.error(request, "Error no envió datos...")
        return redirect('transportes:listarProveedores')
    
#--------------------VEHICULOS----------------------------------------


def listarVehiculo(request):
    login = request.session.get('logueo', False)

    if login and (login[2] == "A" or login[2] == "P"):
        b = Vehiculo.objects.all()
        paginator = Paginator(b, 3) # Mostrar 3 registros por página...

        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        v = paginator.get_page(page_number)
        contextob = {'datosV': v}

        return render(request, 'transportes/login/vehiculo/listarVehiculo.html', contextob)
    else:
        if login and (login[2] != "A" and login[2] != "P"):
            messages.warning(request, "Usted no tiene autorización para acceder al módulo...")
            return redirect('transportes:index')
        else:
            messages.warning(request, "Inicie sesión primero...")
            return redirect('transportes:loginFormulario')


def registrarVehiculo(request):
    u = Proveedores.objects.all()
    contexto = {'proveedores': u}
    return render(request, 'transportes/login/vehiculo/registrarVehiculo.html', contexto)

def guardarVehiculo(request):
    try:
        if request.method == "POST":
            u = Proveedores.objects.get(pk = request.POST["proveedor"])
            q = Vehiculo(
                proveedor = u,
                placa = request.POST["placa"],
                marca = request.POST["marca"],
                color = request.POST["color"],
                foto = request.POST["foto"])
            q.save()

            messages.success(request, "Vehiculo guardado exitosamente")
        else:
            messages.warning(request, "No se han enviado datos...")

    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarVehiculo')

def formularioEditarVehiculo(request, id):
    p = Vehiculo.objects.get(pk = id)
    c = Proveedores.objects.all()
    contexto = { "vehiculo": p, "proveedores":c }
    return render(request, 'transportes/login/vehiculo/editarVehiculo.html', contexto)


def actualizarVehiculo(request):
    try:
        if request.method == "POST":
            #Obtener la instancia de producto a modificar
            p =  Vehiculo.objects.get(pk = request.POST["id"])
            c =  Proveedores.objects.get(pk = request.POST["proveedor"])
            p.proveedor = c
            p.placa = request.POST["placa"]
            p.marca = request.POST["marca"]
            p.color = request.POST["color"]
            p.foto = request.POST["foto"]

            p.save()
            messages.success(request, "Vehiculo actualizado correctamente!!")
        else:
            messages.warning(request, "Usted no ha enviado datos...")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarVehiculo')


def eliminarVehiculo(request, id):
    try:
        p =Vehiculo.objects.get(pk = id)
        p.delete()
        messages.success(request, "Vehiculo eliminado correctamente!!")
    except IntegrityError:
        messages.warning(request, "No puede eliminar este producto porque otros registros están relacionados con él....")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarVehiculo')

def buscarVehiculo(request):
    
    if request.method == "POST":
        dato = request.POST["buscar"]
        q = Vehiculo.objects.filter( Q(id__icontains = dato))
        
        paginator = Paginator(q, 3) # Mostrar 3 registros por página...

        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        q = paginator.get_page(page_number)
        
        contexto = { "datosV": q }
        return render(request, 'transportes/login/vehiculo/listar_Vehiculo_ajax.html', contexto)
    else:
        messages.error(request, "Error no envió datos...")
        return redirect('transportes:listarVehiculo')