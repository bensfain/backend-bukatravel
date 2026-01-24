from django.contrib.auth.forms import ReadOnlyPasswordHashWidget
from django.forms import (CharField, CheckboxInput, DateInput, FileInput,
                          RadioSelect, Select, SplitDateTimeWidget, Textarea,
                          TimeInput)
from django.forms.widgets import CheckboxSelectMultiple
from django.template import Library

register = Library()


@register.filter(name="addcls")
def addcls(field, css):
    if hasattr(field, "as_widget"):
        return field.as_widget(attrs={"class": css})
    return None


@register.filter(name="atribut")
def atribut(field_, attr_):
    if hasattr(field_, "as_widget"):
        attrs = {}
        attrs_from_str = attr_.split("|")
        for attr in attrs_from_str:
            k_, v_ = attr.split(":")
            attrs.update({k_: v_})
        return field_.as_widget(attrs=attrs)
    return None


@register.filter("is_select")
def is_select(field):
    if isinstance(field.field.widget, RadioSelect) or isinstance(
        field.field.widget, CheckboxSelectMultiple
    ):
        return False
    name = str(field.field.widget.__class__.__name__)
    isinstance_ = isinstance(field.field.widget, Select)
    return isinstance_ or name == "RelatedFieldWidgetWrapper"


@register.filter("is_date")
def is_date(field):
    return isinstance(field.field.widget, DateInput)


@register.filter("is_datetime")
def is_datetime(field):
    return isinstance(field.field.widget, SplitDateTimeWidget)


@register.filter("is_time")
def is_time(field):
    return isinstance(field.field.widget, TimeInput)


@register.filter("is_file")
def is_file(field):
    return isinstance(field.field.widget, FileInput)


@register.filter("is_char")
def is_char(field):
    return isinstance(field.field.widget, CharField)


@register.filter("is_textarea")
def is_textarea(field):
    return isinstance(field.field.widget, Textarea)


@register.filter("is_bool")
def is_bool(field):
    return isinstance(field.field.widget, CheckboxInput)


@register.filter("is_readonlypassword")
def is_readonlypassword(field):
    return isinstance(field.field.widget, ReadOnlyPasswordHashWidget)


@register.filter(name="get_filter_choices")
def get_filter_choices(spec, cl):
    if spec:
        return list(spec.choices(cl))
    return ()


@register.filter(name="lookup")
def lookup(value, arg):
    return value[arg]


@register.filter("is_required")
def is_required(field):
    required = str(field).find("required")
    if required > 0:
        return True
    return False
