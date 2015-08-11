from django import template

register = template.Library()

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

@register.filter(name='negate')
def negate(val):
    try:
        if isinstance(val, str):
            return -num(val)
        else:
            return -val
    except ValueError:
        return val

@register.filter(name='format')
def format(val):
    try:
        if isinstance(val, float):
            return '%g' % val
        elif isinstance(val, str):
            return format(num(val))
        else:
            return str(val)
    except ValueError:
        return val

@register.filter(name='decorate')
def addcss(value):
    return value.as_widget(attrs={'class': 'form-control', 'placeholder': value.label})
