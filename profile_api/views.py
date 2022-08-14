from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from profile_api import serializers
from rest_framework import viewsets
from profile_api import models, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

class HelloApiView(APIView):
    """API View de prueba"""

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Devuelve una respuesta de prueba"""
        an_apiview = [
            'Usamos las funciones de APIView para devolver datos',
            'Usamos las funciones de APIView para devolver errores',
            'Usamos las funciones de APIView para devolver datos y errores'
        ]
        return Response({'message': 'Hola!', 'an_apiview': an_apiview})
    
    def post(self, request):
        """Devuelve una respuesta de prueba"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hola {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        """Manipula una entrada en la base de datos"""
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Manipula una actualizacion parcial en la base de datos"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Elimina una entrada en la base de datos"""
        return Response({'method': 'DELETE'})

class HelloViewSet(viewsets.ViewSet):
    """test api viewset"""

    serializer_class = serializers.HelloSerializer
    
    def list(self, request):
        """ Mensaje de hola"""
        a_viewset = [
            'Usamos las funciones de viewsets para devolver datos',
            'Usamos las funciones de viewsets para devolver errores',
            'Usamos las funciones de viewsets para devolver datos y errores'
        ]
        return Response({'message': 'Hola!', 'a_viewset': a_viewset})
    
    def create(self, request):
        """ Crea un nuevo registro"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hola {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """ Devuelve un registro especifico"""
        return Response({'http_method': 'GET'})
    
    def update(self, request, pk=None):
        """ Actualiza un registro especifico"""
        return Response({'http_method': 'PUT'})
    
    def partial_update(self, request, pk=None):
        """ Actualiza un registro especifico"""
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """ Elimina un registro especifico"""
        return Response({'http_method': 'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """ Devuelve y permite crear/actualizar/eliminar usuarios """
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

class UserLoginApiView(ObtainAuthToken):
    """ Devuelve un token de acceso para un usuario """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    
class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """ Devuelve y permite crear/actualizar/eliminar items de un feed de perfil """
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus, 
        IsAuthenticated
    )

    def perform_create(self, serializer):
        """Setea el perfil para el usuario logeado"""
        serializer.save(user_profile=self.request.user)