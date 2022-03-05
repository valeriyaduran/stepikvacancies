from django import template
register = template.Library()


@register.filter()
def salary(value):
    return '{:,}'.format(value).replace(',', ' ')
