from rest_framework import permissions


class isOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a credential to view and edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
