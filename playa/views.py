from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
import datetime


class UsuariosViewSet(viewsets.ModelViewSet):
    serializer_class = UsuariosSerializer
    queryset = UsuariosSerializer.Meta.model.objects.all()
    
    def create(self,request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            gru = GruposSerializer.Meta.model.objects.filter(activo = True).first()
            if gru == None:
                return Response({'mensaje': 'No hay grupos abiertos!!'}, status = status.HTTP_400_BAD_REQUEST)
            else:
                now = datetime.datetime.now()
                temp = gru.estadoCantidad
                #relGru = GrupoUsuariosSerializer.Meta.model.objects.create()
                ss = GruposSerializer(gru)
                if int(gru.cantidadMaxima) > int(temp):
                    ss.Meta.model.objects.update(estadoCantidad = temp + 1)
                    if int(gru.cantidadMaxima) == int(temp)+1:
                        ss.Meta.model.objects.update(activo = False)
                else:
                    return Response({'mensaje': 'No se puede crear el usuario, el grupo esta lleno!!'}, status = status.HTTP_400_BAD_REQUEST)
            serializer.save()
            ngu = GrupoUsuariosSerializer.Meta.model(grupo_id=gru.id,usuarios_id=int(request.data['id_UsuarioDNI']),fechaIngreso=now)
            ngu.save()
            return Response({'mensaje': 'Usuario creado correctamente!'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        gru = GruposSerializer.Meta.model.objects.filter(activo = True).first()
        if gru == None:
            return Response({'mensaje': 'No hay grupos abiertos!!'}, status = status.HTTP_400_BAD_REQUEST)
        else:
            temp = gru.estadoCantidad
            ss = GruposSerializer(gru)
            ss.Meta.model.objects.update(estadoCantidad=temp-1)
            instance = self.get_object()
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class EstadoViewSet(viewsets.ModelViewSet):
    serializer_class = EstadoSerializer
    queryset = EstadoSerializer.Meta.model.objects.all()

class GruposViewSet(viewsets.ModelViewSet):
    serializer_class = GruposSerializer
    # queryset = GruposSerializer.Meta.model.objects.all()
    def get_queryset(self,pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.exclude(activo=None)
        return self.get_serializer().Meta.model.objects.filter(id = pk,activo = True).first()

    def create(self,request):
        serializer = self.serializer_class(data = request.data, context = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Grupo creado correctamente!'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,context = request.data ,partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

class GrupoUsuariosViewSet(viewsets.ModelViewSet):
    serializer_class = GrupoUsuariosSerializer
    queryset = GrupoUsuariosSerializer.Meta.model.objects.all()

class TrabajadoresViewSet(viewsets.ModelViewSet):
    serializer_class = TrabajadoresSerializer
    # queryset = TrabajadoresSerializer.Meta.model.objects.all()
    def get_queryset(self,pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(isActive = True)
        return self.get_serializer().Meta.model.objects.filter(id_TrabajadoresDNI = pk, isActive = True)

    def create(self,request):
        serializer = self.serializer_class(data = request.data, context = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Trabajador creado correctamente!'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

#    def update(self,request,pk=None):
#        if self.get_queryset(pk):
#            trab_serializer = self.serializer_class(self.get_queryset(pk), data = request.data, context = request.data)
#            if trab_serializer.is_valid():
#                trab_serializer.save()
#                return Response(trab_serializer.data, status = status.HTTP_200_OK)
#            return Response(trab_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,context = request.data ,partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

class PlayasViewSet(viewsets.ModelViewSet):
    serializer_class = PlayasSerializer
    queryset = PlayasSerializer.Meta.model.objects.all()

class SubPlayasViewSet(viewsets.ModelViewSet):
    serializer_class = SubPlayasSerializer
    queryset = SubPlayasSerializer.Meta.model.objects.all()

    def create(self,request):
        serializer = self.serializer_class(data = request.data, context = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'SubPlaya creada correctamente!!'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,context = request.data ,partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

class SombrillasViewSet(viewsets.ModelViewSet):
    serializer_class = SombrillasSerializer
    queryset = SombrillasSerializer.Meta.model.objects.all()

class SombrillaGrupoViewSet(viewsets.ModelViewSet):
    serializer_class = SombrillaGrupoSerializer
    queryset = SombrillaGrupoSerializer.Meta.model.objects.all()

class TiposEdificioViewSet(viewsets.ModelViewSet):
    serializer_class = TiposEdificioSerializer
    queryset = TiposEdificioSerializer.Meta.model.objects.all()

class EdificiosInteresViewSet(viewsets.ModelViewSet):
    serializer_class = EdificiosInteresSerializer
    queryset = EdificiosInteresSerializer.Meta.model.objects.all()

class EdificiosPlayaViewSet(viewsets.ModelViewSet):
    serializer_class = EdificiosPlayaSerializer
    queryset = EdificiosPlayaSerializer.Meta.model.objects.all()

class AreasViewSet(viewsets.ModelViewSet):
    serializer_class = AreasSerializer
    queryset = AreasSerializer.Meta.model.objects.all()

class AreasPlayaViewSet(viewsets.ModelViewSet):
    serializer_class = AreasPlayaSerializer
    queryset = AreasPlayaSerializer.Meta.model.objects.all()

class ObjetosViewSet(viewsets.ModelViewSet):
    serializer_class = ObjetosSerializer
    # queryset = ObjetosSerializer.Meta.model.objects.all()

    def get_queryset(self,pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(isActive = True)
        return self.get_serializer().Meta.model.objects.filter(id=pk, isActive = True).first()
    
    def create(self,request):
        serializer = self.serializer_class(data = request.data, context = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Objeto creado correctamente!'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,context = request.data ,partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

class EAlimentoBebidaViewSet(viewsets.ModelViewSet):
    serializer_class = EAlimentoBebidaSerializer
    queryset = EAlimentoBebidaSerializer.Meta.model.objects.all()

    def create(self,request):
        serializer = self.serializer_class(data = request.data, context = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Edificio Alimento Bebida creado correctamente!'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,context = request.data ,partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

class EdificioInteresListAPIVie(generics.RetrieveAPIView):
    serializer_class = EdificioInteresPlaya

    def get_queryset(self):
        return EdificiosPlaya.objects.all()