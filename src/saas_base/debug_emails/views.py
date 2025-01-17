from django.http import HttpResponse, Http404
from ..mail import get_mail_provider
from ..settings import saas_settings


def view_signup_code(request, suffix: str):
    provider = get_mail_provider()
    context = {
        'code': 'ABCD',
        'site': saas_settings.SITE,
    }
    text_message, html_message = provider.render_message('signup_code', context)
    if suffix == 'txt':
        return HttpResponse(text_message, content_type='text/plain')
    elif suffix == 'html':
        return HttpResponse(html_message, content_type='text/html')
    else:
        raise Http404


def view_reset_password(request, suffix: str):
    provider = get_mail_provider()
    context = {
        'code': 'ABCD',
        'site': saas_settings.SITE,
        'user': 'Alice',
    }
    text_message, html_message = provider.render_message('reset_password', context)
    if suffix == 'txt':
        return HttpResponse(text_message, content_type='text/plain')
    elif suffix == 'html':
        return HttpResponse(html_message, content_type='text/html')
    else:
        raise Http404
