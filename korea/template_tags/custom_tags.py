from django import template
from django.template.defaulttags import register
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def get_item(dictionary, key):

    return dictionary.get(key)
