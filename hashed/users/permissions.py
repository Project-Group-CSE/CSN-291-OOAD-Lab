from rest_framework import permissions


class isOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a credential to view and edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    #has pin permission
# class IsPinAuthenticated(permissions.BasePermission):
#     """
#     Custom permission to check if the PIN has been authenticated.
#     """

#     def __init__(self):
#         self.pin_authenticated = False  # Initialize the flag as False

#     def has_permission(self, request, view):
#         # You can implement your PIN authentication logic here.
#         # For example, you might check if the PIN is provided in the request and matches the user's PIN.
#         user = request.user
#         if 'pin' in request.data and request.data['pin'] == user.hashed_pin:
#             self.pin_authenticated = True  # Set the flag to True if PIN is authenticated
#             return True
#         return False