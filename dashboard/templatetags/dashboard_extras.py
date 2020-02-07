from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def display_state(obj):
    iconStr = '<i class="fas fa-exclamation-circle text-warning"></i>'
    if obj.is_active():
        iconStr = '<i class="fas fa-check-circle text-success"></i>'
    something = '<a class="btn btn-sm btn-default" data-toggle="tooltip" data-placement="top" title="%s">%s</a>' % (
        obj.get_state_display(), iconStr)
    return mark_safe(something)
