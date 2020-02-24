from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def display_state(obj):
    state = obj.get_state_display()
    if obj.is_active():
        result = '<span class="badge badge-success badge-pill">%s</span>' % (
            state)
    elif obj.is_inactive():
        result = '<span class="badge badge-danger badge-pill">%s</span>' % (
            state)
    else:
        result = '<span class="badge badge-warning badge-pill">%s</span>' % (
            state)
    return mark_safe(result)


@register.filter
def display_course_type(obj):
    course_type = obj.course_type
    course_type_display = obj.get_course_type_display()
    if course_type == 0:
        result = '<span class="badge badge-success badge-pill">%s</span>' % (
            course_type_display)
    else:
        result = '<span class="badge badge-danger badge-pill">%s</span>' % (
            course_type_display)
    return mark_safe(result)
