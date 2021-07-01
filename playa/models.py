from django.db import models

# Create your models here.
class Usuarios(models.Model):
    id_UsuarioDNI = models.IntegerField(primary_key=True)
    edad = models.IntegerField()
    temperatura = models.FloatField()
    
    def __str__(self):
        return f'{self.id_UsuarioDNI}, °C {self.temperatura}'

class Estado(models.Model):
    estado = models.CharField(max_length=25)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.estado

class Grupos(models.Model):
    cantidadMaxima = models.IntegerField(default=8)
    estadoCantidad = models.IntegerField(default=0)
    activo = models.BooleanField(null=True, default=True)

    def __str__(self):
        return f'{self.id}, estado: {self.estadoCantidad}'

class GrupoUsuarios(models.Model):
    grupo = models.ForeignKey(Grupos, on_delete=models.CASCADE)
    usuarios = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    fechaIngreso = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return f'{self.usuarios} pertenece al grupo {self.grupo}'

class Trabajadores(models.Model):
    id_TrabajadoresDNI = models.IntegerField(primary_key=True)
    user = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=35)
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=50, null=True, blank=True)
    edad = models.IntegerField()
    celular = models.CharField(max_length=9)
    correo = models.EmailField(max_length=255, unique=True)
    imageUser = models.URLField(default='https://i.ibb.co/2tshgPv/andres-gevara.jpg',null=True, blank=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

class Playas(models.Model):
    nombre = models.CharField(max_length=35)
    ubicacion = models.CharField(max_length=50)
    imagePlay = models.URLField(default='https://i.ibb.co/dQn81QZ/playa-default.png',null=True,blank=True)
    estado = models.ForeignKey(Estado,on_delete=models.CASCADE)
    departamentos = models.CharField(max_length=45, null=True)

    def __str__(self):
        return self.nombre

class SubPlayas(models.Model):
    playa = models.ForeignKey(Playas, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=35)
    capacidad = models.IntegerField()
    estadoCapacidad = models.IntegerField()
    imgSubPlaya = models.URLField(default='https://i.ibb.co/dQn81QZ/playa-default.png',null=True)
    estado = models.ForeignKey(Estado,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre

class Sombrillas(models.Model):
    subPlaya = models.ForeignKey(SubPlayas, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.subPlaya} estado: {self.estado}'

class SombrillaGrupo(models.Model):
    grupo = models.ForeignKey(GrupoUsuarios, on_delete=models.CASCADE)
    sombrilla = models.ForeignKey(Sombrillas, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.grupo} y {self.sombrilla}'

class TiposEdificio(models.Model):
    nombreTE = models.CharField(max_length=30)

    def __str__(self):
        return self.nombreTE

class EdificiosInteres(models.Model):
    tipoEdificio = models.ForeignKey(TiposEdificio, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado,on_delete=models.CASCADE)
    nombreEI = models.CharField(max_length=35)
    descripcion = models.TextField(blank=True, null=True)
    direccion = models.CharField(max_length=60)
    contacto = models.CharField(max_length=9)

    def __str__(self):
        return self.nombreEI

class EdificiosPlaya(models.Model):
    nombreEI = models.ForeignKey(EdificiosInteres, on_delete=models.CASCADE)
    nombre = models.ForeignKey(Playas, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nombre} -> {self.nombreEI}'
        
class Areas(models.Model):
    edificioInteres = models.ForeignKey(EdificiosInteres, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=35)

    def __str__(self):
        return self.nombre

class AreasPlaya(models.Model):
    edificioPlaya = models.ForeignKey(EdificiosPlaya, on_delete=models.CASCADE)
    trabajador = models.ForeignKey(Trabajadores, on_delete=models.CASCADE)
    area = models.ForeignKey(Areas, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.area} de {self.edificioPlaya}'

class Objetos(models.Model):
    nombreEI = models.ForeignKey(EdificiosInteres, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=53)
    cantidad = models.IntegerField()
    alquilados = models.IntegerField()
    descripcion = models.TextField()
    imageObj = models.URLField(default='https://i.ibb.co/mFknmDH/objetos-default.jpg',null=True,blank=True)
    isActive = models.BooleanField(default=True, null=True)

    def __str__(self):
        return self.nombre

class EAlimentoBebida(models.Model):
    edificioInteres = models.ForeignKey(EdificiosInteres, on_delete=models.CASCADE)
    capacidad = models.IntegerField()
    estadoCapacidad = models.IntegerField()

    def __str__(self):
        return f'{self.edificioInteres}: {self.estadoCapacidad}'