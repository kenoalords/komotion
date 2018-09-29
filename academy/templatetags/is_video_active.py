from django import template

register = template.Library()

def is_active(value, args):
    if value == args:
        return 'is-active'
    else:
        return None

register.filter('is_active', is_active)
