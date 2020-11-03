from django.template.defaultfilters import register


@register.filter(name='percentage')
def percentage(fraction):
    try:
        return "%.2f%%" % (float(fraction) * 100)
    except ValueError:
        return ''
