import typing as t
from ..mail import get_mail_provider


def send_notification_mail(
        subject: str,
        recipients: t.List[str],
        text_message: str,
        html_message: t.Optional[str] = None,
        from_email: t.Optional[str] = None,
        headers: t.Optional[t.Dict[str, str]] = None,
        reply_to: t.Optional[str] = None,
        fail_silently: bool = False):
    provider = get_mail_provider('notification', 'default')
    return provider.send_mail(
        subject,
        recipients,
        text_message,
        html_message,
        from_email=from_email,
        headers=headers,
        reply_to=reply_to,
        fail_silently=fail_silently,
    )


def render_email_message(
        request,
        template_id: str,
        context: t.Dict[str, t.Any],
        using: t.Optional[str] = None) -> t.Tuple[str, str]:
    provider = get_mail_provider('notification', 'default')
    return provider.render_message(request, template_id, context, using)
