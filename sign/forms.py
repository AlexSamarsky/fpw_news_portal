from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

from NewsPaper.models import Author


class BasicSignupForm(SignupForm):
    
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        # try:
        return user