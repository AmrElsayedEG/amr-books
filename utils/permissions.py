from rest_framework.permissions import BasePermission
from utils import UserRoleChoices

class isAdminUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.role == UserRoleChoices.ADMIN)
    
class isVisitorUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.role == UserRoleChoices.VISITOR)
    
class canUpdateBooks(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return bool(request.user.role == UserRoleChoices.ADMIN)