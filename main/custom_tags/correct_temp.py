from django import template

register = template.Library()

@register.filter
def correct_temps(product):
    print(product)
    pass
