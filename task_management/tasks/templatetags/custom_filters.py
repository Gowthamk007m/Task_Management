from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def add_class(field, css_class):
    """Add a CSS class to a form field."""
    return field.as_widget(attrs={"class": css_class})

@register.filter
def sort_by(queryset, order_by):
    """Sort a queryset by the given field."""
    if order_by.startswith('-'):
        return sorted(queryset, key=lambda x: getattr(x, order_by[1:]), reverse=True)
    else:
        return sorted(queryset, key=lambda x: getattr(x, order_by))

@register.filter
def first_item(queryset):
    """Return the first item of a queryset or list."""
    if queryset:
        return queryset[0]
    return None

@register.filter
def slice_items(queryset, slice_str):
    """Slice a queryset or list."""
    start, end = map(int, slice_str.split(':'))
    return queryset[start:end]

@register.filter
def default_if_none(value, default=""):
    """Return default value if the provided value is None."""
    if value is None:
        return default
    return value

@register.filter
def truncate_chars(value, max_length):
    """Truncate text to a maximum number of characters."""
    if len(value) > max_length:
        return f"{value[:max_length]}..."
    return value

@register.simple_tag
def now(format_string):
    """Return the current time formatted."""
    from django.utils import timezone
    return timezone.now().strftime(format_string)