# не подключается модуль..

# from allauth.account.signals import user_signed_up
# from django.dispatch import receiver
# from django.template.loader import render_to_string
# from django.conf import settings
# from django.core.mail import send_mail

# from NewsPaper.urls import get_external_url


# @receiver(user_signed_up, dispatch_uid="some.unique.string.id.for.allauth.user_signed_up")
# def user_signed_up_(request, user, **kwargs):
#     external_url = get_external_url(request, '/news/')

#     message_text = render_to_string('mail/hello.html', { 'post_url': external_url, })
    
#     recipients = [user.email]
#     if recipients:
#         send_mail('Добро пожаловать на портал',
#                             message_text,
#                             settings.EMAIL_HOST_USER,
#                             recipients,
#                             html_message=message_text
#                         )
