# In your app's templatetags folder, create a file filters.py
from django import template

register = template.Library()

@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})