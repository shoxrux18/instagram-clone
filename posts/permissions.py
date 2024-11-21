from rest_framework.permissions import BasePermission


class CreatorOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
