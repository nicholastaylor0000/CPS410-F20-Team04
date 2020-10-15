from .models import Museum, Group
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from user.decorators import confirmation_required

def museum_admin(view):
    @confirmation_required
    def wrapper(request, pk, *args, **kwargs):
        museum = get_object_or_404(Museum, id=pk)
        if request.user in museum.admins.all():
            return view(request, museum, *args, **kwargs)
        else:
            raise PermissionDenied(f'you are not an admin of {museum.name}')
    return wrapper

def group_admin(view):
    @confirmation_required
    def wrapper(request, pk, *args, **kwargs):
        group = get_object_or_404(Group, id=pk)
        if (request.user in group.leaders.all() 
            or request.user in group.museum.admins.all()):
            return view(request, group, *args, **kwargs)
        else:
            raise PermissionDenied(f'you are not an admin of {group.name}')
    return wrapper