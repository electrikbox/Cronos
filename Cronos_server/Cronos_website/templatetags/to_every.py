from django import template

register = template.Library()

@register.filter
def to_every(value):
    return value.replace("*","every")
