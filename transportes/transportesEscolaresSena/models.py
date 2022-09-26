from django.db import models

# Create your models here.

class Cliente(models.Model):
 
    nombre = models.CharField(max_length= 100)
    apellido = models.CharField(max_length= 100)
    correo = models.EmailField(max_length= 250, null=True, blank=True)
    direccion = models.CharField(max_length= 100)
    documento = models.IntegerField()
    fecha_nacimiento = models.DateTimeField()


    def __str__(self):
        return f" {self.nombre} "

class Beneficiarios (models.Model):
    cliente = models.ForeignKey(Cliente,on_delete = models.DO_NOTHING)
    nombre = models.CharField(max_length= 100)
    apellido = models.CharField(max_length= 100)
    documento = models.IntegerField()
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return f" {self.nombre} "


class Comentarios (models.Model):
    cliente = models.ForeignKey(Cliente,on_delete = models.DO_NOTHING)
    tipo = models.CharField(max_length= 100)
    desc = models.CharField(max_length= 1000)

    def __str__(self):
        return f"{self.cliente} {self.tipo}"


class TiposdeServicios (models.Model):
    nombre = models.CharField(max_length= 100)
    caracteristicas = models.CharField(max_length= 500)

    def __str__(self):
        return f" {self.nombre} "



class Servicios (models.Model):
    nombre = models.CharField(max_length= 100)
    tipo_serv = models.ForeignKey(TiposdeServicios,on_delete = models.DO_NOTHING)
    def __str__(self):
        return f" {self.nombre} "



class Peticiones(models.Model):
    cliente = models.ForeignKey(Cliente,on_delete = models.DO_NOTHING)
    servicios = models.ForeignKey(Servicios,on_delete = models.DO_NOTHING)
    direccion = models.CharField(max_length= 100)
    colegio = models.CharField(max_length= 200)
    horario = models.CharField(max_length= 100)
    comentario_add = models.CharField(max_length= 100, null=True,blank=True)

    def __str__(self):
        return f" {self.cliente},{self.servicios} "

    

class Proveedores(models.Model):
    nombre = models.CharField(max_length= 100)
    apellido = models.CharField(max_length= 100)
    correo = models.EmailField(max_length= 250, null=True, blank=True)
    direccion = models.CharField(max_length= 100)
    documento = models.IntegerField()
    fecha_nacimiento = models.DateTimeField()
    marca_veh = models.CharField(max_length= 100)
    color_veh = models.CharField(max_length= 100)
    documentacion_veh = models.BooleanField()
    def __str__(self):
        return f" {self.nombre} "



