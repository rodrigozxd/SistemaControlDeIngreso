from django.db import router
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *
from . import views
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()

router.register(r'users', UsuariosViewSet)
router.register(r'states', EstadoViewSet)
router.register(r'groups', GruposViewSet, basename = 'GRUPOS')
router.register(r'groupUsers', GrupoUsuariosViewSet)
router.register(r'workers', TrabajadoresViewSet, basename = 'TRABAJADORES')
router.register(r'beaches', PlayasViewSet)
router.register(r'subbeaches', SubPlayasViewSet, basename = 'SUBPLAYAS')
router.register(r'umbrellas', SombrillasViewSet, basename = 'SOMBRILLAS')
router.register(r'umbrellaGroups', SombrillaGrupoViewSet)
router.register(r'typesBuilding', TiposEdificioViewSet)
router.register(r'buildingsInterest', EdificiosInteresViewSet)
router.register(r'beachBuilding', EdificiosPlayaViewSet)
router.register(r'areas', AreasViewSet)
router.register(r'areasBeach', AreasPlayaViewSet)
router.register(r'objects', ObjetosViewSet, basename = 'OBJETOS')
router.register(r'foodDirnksBuildings', EAlimentoBebidaViewSet)

urlpatterns = [
    path('listEdificioPlaya/<int:pk>/<int:nombreEI>', EdificioInteresListAPIVie.as_view(), name='listaEdificioPlaya'),
]

urlpatterns += router.urls 