from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    # доступ только для пользователей из группы "manager"
    def has_permission(self, request, view):
        return request.user.groups.filter(name='manager').exists()

class IsClient(BasePermission):
    # доступ только для пользователей из группы "client"
    def has_permission(self, request, view):
        return request.user.groups.filter(name='client').exists()