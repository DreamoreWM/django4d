from rest_framework import permissions

class IsResponsable(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Responsable').exists()

class CanUpdateIntervention(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.employee or request.user.groups.filter(name='Responsable').exists()