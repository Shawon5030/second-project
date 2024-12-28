from django import template
from app.models import SiteSettings, Customer_model

register = template.Library()

@register.simple_tag
def get_site_logo():
    try:
        settings = SiteSettings.objects.first()
        if settings and settings.logo:
            return settings.logo.url
    except SiteSettings.DoesNotExist:
        return ''
    return ''

@register.simple_tag(takes_context=True)
def profile_pic(context):
    request = context['request']
    try:
        customer = Customer_model.objects.filter(user=request.user).first()
        if customer.signature:
            return customer.signature.url
    except Customer_model.DoesNotExist:
        return ''
    return ''

@register.simple_tag(takes_context=True)
def get_profile_image(context):
    request = context['request']
    try:
        customer = Customer_model.objects.get(user=request.user)
        if customer.profile_image:
            return customer.profile_image.url
    except Customer_model.DoesNotExist:
        return ''
    return ''

@register.filter
def add_class(field, css):
    return field.as_widget(attrs={"class": css})
