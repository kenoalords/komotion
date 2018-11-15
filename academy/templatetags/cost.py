from django import template

register = template.Library()

def cost_int(value):
    return int(value)

register.filter('cost_int', cost_int)
