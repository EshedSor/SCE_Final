from rest_framework import permissions
from .models import Group, GroupMessage

class IsGroupMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Group):
            return request.user in obj.members.all()
        elif isinstance(obj, GroupMessage):
            return request.user in obj.group.members.all()
        return False