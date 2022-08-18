from django import template
register = template.Library()


@register.filter
def to_int(value):
    if int(value) == value * 1.0:
        return int(value)
    else:
        return value

@register.filter
def to_money(value):
    return '%s $' % str(value)


register.filter('to_int', to_int)
register.filter('to_money', to_money)
