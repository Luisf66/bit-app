from django import template

register = template.Library()

@register.filter
def is_select(field):
    return field.field.widget.__class__.__name__ in ('Select', 'ModelChoiceField', 'SelectWidget')

@register.filter  
def widget_type(field):
    return field.field.widget.__class__.__name__