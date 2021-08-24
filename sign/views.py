from django.shortcuts import redirect, render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import get_user_model


@login_required
def be_author(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not user.groups.filter(pk=author_group.pk).exists():
        author_group.user_set.add(user)
    return redirect('/news/')

def permissions(request):

    permissions = set()
    # We create (but not persist) a temporary superuser and use it to game the
    # system and pull all permissions easily.
    tmp_superuser = get_user_model()(
        is_active=True,
        is_superuser=True
    )
    for backend in auth.get_backends():
        if hasattr(backend, "get_all_permissions"):
            permissions.update(backend.get_all_permissions(tmp_superuser))

    # Output unique list of permissions sorted by permission name.
    sorted_list_of_permissions = sorted(list(permissions))
    s = '<br>'.join(sorted_list_of_permissions)
    return HttpResponse(s)
