from django import template

from .. import app_settings
from .. import forms

register = template.Library()


@register.simple_tag
def payzen_form(payment_request, auto_submit=False):
    """TODO docstring."""
    if auto_submit:
        template_used = "django_pypayzen/auto_submit_form.html"
    else:
        template_used = "django_pypayzen/form.html"
    payment_request.update()
    t = template.loader.get_template(template_used)
    return t.render(template.Context({
        "form": forms.PaymentRequestForm(instance=payment_request),
        "payzen_submit_url": app_settings.PAYZEN_REQUEST_URL
    }))
