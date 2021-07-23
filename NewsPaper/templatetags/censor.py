from django import template
import re
register = template.Library()


@register.filter(name='censor')
def censor(value):
    censor_words = ['fuck', 'shit', 'fool']
    re_str = '|'.join(censor_words)
    return re.sub(re_str, '###', value)