from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import get_user_model



from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.template.loader import render_to_string

from NewsPaper.utils import get_external_url

from NewsPaper.models import Author


@receiver(user_signed_up, dispatch_uid="some.unique.string.id.for.allauth.user_signed_up_views")
def user_signed_up_(request, user, **kwargs):
    external_url = get_external_url(request, '/news/')

    message_text = render_to_string('mail/hello.html', { 'post_url': external_url, })
    
    recipients = [user.email]
    if recipients:
        send_mail('Добро пожаловать на портал',
                            message_text,
                            settings.EMAIL_HOST_USER,
                            recipients,
                            html_message=message_text
                        )


@login_required
def be_author(request):
    user = request.user
    if not Author.objects.filter(user=user).exists():
        author = Author(user=user)
        author.save()

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
