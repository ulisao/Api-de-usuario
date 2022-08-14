from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Permite a los usuarios actualizar su propio perfil"""

    def has_object_permission(self, request, view, obj):
        """Devuelve True si el usuario autenticado es el propietario del perfil"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id

class UpdateOwnStatus(permissions.BasePermission):
    """Permite a los usuarios actualizar su propio status"""

    def has_object_permission(self, request, view, obj):
        """Devuelve True si el usuario autenticado es el propietario del status"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile.id == request.user.id