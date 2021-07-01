from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *

class UsuariosSerializer(serializers.ModelSerializer):

    id_UsuarioDNI = serializers.IntegerField(validators = [MinValueValidator(10000000, message='El DNI no puede tener menos de 8 digitos'),MaxValueValidator(99999999,message='El DNI no puede tener mas de 8 digitos')])
    edad = serializers.IntegerField(validators = [MinValueValidator(0,message='No puedes ser menor a 0'),MaxValueValidator(75,message='No puedes ingresar si eres mayor de 75')])
    temperatura = serializers.FloatField( validators = [MinValueValidator(36.1,message='Su temperatura es muy baja, DIRIJASE AL HOSPITAL'),MaxValueValidator(37.2,message='Usted tiene fiebre, DIRIJASE AL HOSPITAL')])

    class Meta:
        model = Usuarios
        fields = '__all__'

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = '__all__'

class GruposSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    cantidadMaxima = serializers.IntegerField(validators = [MinValueValidator(2,message='El grupo puede ser de 2 minimo'), MaxValueValidator(22,message='El grupo puede ser maximo de 22 personas')], default=20)
    estadoCantidad = serializers.IntegerField(validators = [MinValueValidator(0,message='El estado no puede ser menor a 0'), MaxValueValidator(22,message='El grupo puede ser maximo de 22 personas')],default=0)
    activo = serializers.BooleanField(allow_null=True,default=True)

    class Meta:
        model = Grupos
        fields = '__all__'

    def validate_estadoCantidad(self,value):
        if value == None:
            return value
        elif value > int(self.context['cantidadMaxima']):
            raise serializers.ValidationError('Error, el estado no puede ser mayor al maximo!!')
        return value

class GrupoUsuariosSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = GrupoUsuarios
        fields = '__all__'
    
    def to_representation(self,instance):
        return {
            'id': instance.id,
            'grupo': instance.grupo.estadoCantidad,
            'usuarios': instance.usuarios.id_UsuarioDNI,
            'fechaIngreso': instance.fechaIngreso
        }

class TrabajadoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajadores
        fields = '__all__'

    def to_representation(self,instance):
        return {
            'id_TrabajadoresDNI': instance.id_TrabajadoresDNI,
            'user': instance.user,
            'password': instance.password,
            'nombre': instance.nombre,
            'apellido': instance.apellido,
            'edad': instance.edad,
            'celular': instance.celular,
            'correo': instance.correo,
            'imageUser': instance.imageUser,
            'isActive': instance.isActive
        }

    def validate_id_TrabajadoresDNI(self,value):
        if value < 10000000 or value > 99999999:
            raise serializers.ValidationError('Error, el DNI ingresado no es valido!!')
        return value

    def validate_password(self,value):
        if self.context['nombre'] in value:
            raise serializers.ValidationError('Error, la contraceña no puede contener su nombre!!')
        elif self.context['user'] in value:
            raise serializers.ValidationError('Error, la contraceña no puede contener su Usuario!!')
        return value

    def validate_edad(self,value):
        if value < 18:
            raise serializers.ValidationError('Error, el trabajador debe ser mayor de edad!!')
        elif value > 70:
            raise serializers.ValidationError('Error, el trabajador no puede ser mayor de 70!!')
        return value

    def validate_celular(self,value):
        if value.isdigit():
            v = int(value)
            if v < 899999999:
                raise serializers.ValidationError('Error, el numero de celular ingresado no es valido!!')
        else:
            raise serializers.ValidationError('Error, debes ingresar un numero!!')
        return value

    def create(self,validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(TrabajadoresSerializer, self).create(validated_data)

    def update(self,instance,validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(TrabajadoresSerializer,self).update(instance,validated_data)

class PlayasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playas
        fields = '__all__'
    
    def to_representation(self,instance):
        return {
            'id': instance.id,
            'nombre': instance.nombre,
            'ubicacion': instance.ubicacion,
            'imagePlay': instance.imagePlay or '',
            'estado': instance.estado.estado,
            'departamentos': instance.departamentos
        }

class SubPlayasSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubPlayas
        fields = '__all__'

    def to_representation(self,instance):
        return {
            'id': instance.id,
            'nombre': instance.nombre,
            'capacidad': instance.capacidad,
            'estadoCapacidad': instance.estadoCapacidad,
            'playa': instance.playa.nombre,
            'imgSubPlaya': instance.imgSubPlaya,
            'estado': instance.estado.estado
        }

    def validate_estadoCapacidad(self,value):
        if value > int(self.context['capacidad']):
            raise serializers.ValidationError('Error, el estado de capacidad no puede ser mayor la capacidad!!')
        return value

class SombrillasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sombrillas
        fields = '__all__'

    def to_representation(self,instance):
        return {
            'id': instance.id,
            'subPlaya': instance.subPlaya.nombre,
            'estado': instance.estado.estado
        }

class SombrillaGrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SombrillaGrupo
        fields = '__all__'

class TiposEdificioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiposEdificio
        fields = '__all__'

class EdificiosInteresSerializer(serializers.ModelSerializer):
    class Meta:
        model = EdificiosInteres
        fields = '__all__'

    def to_representation(self,instance):
        return {
            'id': instance.id,
            'nombreEI': instance.nombreEI,
            'descripcion': instance.descripcion,
            'direccion': instance.direccion,
            'contacto': instance.contacto,
            'tipoEdificio': instance.tipoEdificio.nombreTE,
            'estado': instance.estado.estado
        }

    def validate_contacto(self,value):
        if value.isdigit():
            v = int(value)
            if v < 899999999:
                raise serializers.ValidationError('Error, el numero de celular ingresado no es valido!!')
        else:
            raise serializers.ValidationError('Error, debes ingresar un numero!!')
        return value

class EdificiosPlayaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EdificiosPlaya
        fields = '__all__'

    def to_representation(self,instance):
        return {
            'id': instance.id,
            'nombreEI': instance.nombreEI.nombreEI,
            'nombre': instance.nombre.nombre
        }

class AreasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Areas
        fields = '__all__'

    def to_representation(self,instance):
        return {
            'id': instance.id,
            'nombre': instance.nombre,
            'edificioInteres': instance.edificioInteres.nombreEI
        }

class AreasPlayaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreasPlaya
        fields = '__all__'

    def to_representation(self,instance):
        return {
            'id': instance.id,
            'edificioPlaya': instance.edificioPlaya.nombreEI.nombreEI,
            'trabajador': instance.trabajador.nombre,
            'area': instance.area.nombre
        }

class ObjetosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objetos
        fields = '__all__'

    def to_representation(self,instance):
        return {
            'id': instance.id,
            'nombre': instance.nombre,
            'cantidad': instance.cantidad,
            'alquilados': instance.alquilados,
            'descripcion': instance.descripcion,
            'imageObj': instance.imageObj,
            'isActive': instance.isActive,
            'nombreEI': instance.nombreEI.nombreEI
        }

    def validate_alquilados(self,value):
        if value > int(self.context['cantidad']):
            raise serializers.ValidationError('Error, este dato no se puede guardar, ya que, es mayor a las existencias.')
        return value

class EAlimentoBebidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EAlimentoBebida
        fields = '__all__'

    def to_representation(self,instance):
        return {
            'id': instance.id,
            'capacidad': instance.capacidad,
            'estadoCapacidad': instance.estadoCapacidad,
            'edificioInteres': instance.edificioInteres.nombreEI
        }

    def validate_estadoCapacidad(self,value):
        if value > int(self.context['capacidad']):
            raise serializers.ValidationError('Error, ya no entran mas personas!!')
        return value

class EdificioInteresPlaya(serializers.ModelSerializer):
    nombreEI = EdificiosInteresSerializer()
    nombre = PlayasSerializer()
    class Meta:
        model = EdificiosPlaya
        fields = '__all__'