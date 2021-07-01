from django.contrib import admin
from .models import *

class UsuariosAdmin(admin.ModelAdmin):
    list_display = ['id_UsuarioDNI','temperatura']
    search_fields = ['id_UsuarioDNI']
    list_filter = ['edad']

class EstadoAdmin(admin.ModelAdmin):
    list_display = ['estado','descripcion']
    search_fields = ['estado']

class GrupoAdmin(admin.ModelAdmin):
    list_display = ['id','cantidadMaxima','estadoCantidad','activo']
    search_fields = ['id','estadoCantidad']
    list_filter = ['activo']

class GrupoUsuariosAdmin(admin.ModelAdmin):
    search_fields = ['grupo']
    list_filter = ['fechaIngreso']

class TrabajadoresAdmin(admin.ModelAdmin):
    search_fields = ['nombre','apellido', 'celular', 'correo']
    list_filter = ['isActive']

class PlayasAdmin(admin.ModelAdmin):
    list_display = ['nombre','estado','departamentos']
    search_fields = ['nombre']
    list_filter = ['estado']

class SubPlayasAdmin(admin.ModelAdmin):
    list_display = ['playa', 'nombre', 'capacidad', 'estadoCapacidad', 'estado']
    search_fields = ['playa', 'nombre']
    list_filter = ['estado']

class SombrillasAdmin(admin.ModelAdmin):
    list_display = ['subPlaya', 'estado']
    list_filter = ['estado']

class SombrillaGrupoAdmin(admin.ModelAdmin):
    list_display = ['grupo', 'sombrilla']

class TiposEdificioAdmin(admin.ModelAdmin):
    search_fields = ['nombreTE']

class EdificiosInteresAdmin(admin.ModelAdmin):
    list_display = ['nombreEI', 'descripcion', 'estado']
    search_fields = ['nombreEI']
    list_filter = ['estado']

class AreasAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'edificioInteres']
    search_fields = ['nombre']

class ObjetosAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cantidad', 'alquilados', 'isActive']
    search_fields = ['nombre']
    list_filter = ['isActive']

class EAlimentoBebidaAdmin(admin.ModelAdmin):
    list_display = ['edificioInteres', 'capacidad', 'estadoCapacidad']
    list_filter = ['edificioInteres']

admin.site.register(Usuarios, UsuariosAdmin)
admin.site.register(Estado, EstadoAdmin)
admin.site.register(Grupos, GrupoAdmin)
admin.site.register(GrupoUsuarios, GrupoUsuariosAdmin)
admin.site.register(Trabajadores, TrabajadoresAdmin)
admin.site.register(Playas,PlayasAdmin)
admin.site.register(SubPlayas,SubPlayasAdmin)
admin.site.register(Sombrillas,SombrillasAdmin)
admin.site.register(SombrillaGrupo,SombrillaGrupoAdmin)
admin.site.register(TiposEdificio,TiposEdificioAdmin)
admin.site.register(EdificiosInteres,EdificiosInteresAdmin)
admin.site.register(EdificiosPlaya)
admin.site.register(Areas,AreasAdmin)
admin.site.register(AreasPlaya)
admin.site.register(Objetos,ObjetosAdmin)
admin.site.register(EAlimentoBebida,EAlimentoBebidaAdmin)

