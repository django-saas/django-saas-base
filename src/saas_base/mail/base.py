import typing as t
from django.template import loader
from abc import ABCMeta, abstractmethod


class BaseMailProvider(metaclass=ABCMeta):
    name: str = "base"

    def __init__(self, **options):
        self.default_from_email = options.pop('default_from_email', None)
        self.options = options

    @abstractmethod
    def send_mail(
            self,
            subject: str,
            recipients: t.List[str],
            text_message: str,
            html_message: t.Optional[str] = None,
            from_email: t.Optional[str] = None,
            headers: t.Optional[t.Dict[str, str]] = None,
            reply_to: t.Optional[str] = None,
            fail_silently: bool = False):
        pass

    def render_message(
            self,
            request,
            template_id: str,
            context: t.Dict[str, t.Any],
            using: t.Optional[str] = None) -> t.Tuple[str, str]:
        text: str = loader.render_to_string(
            f"saas_emails/{template_id}.text",
            context, request, using=using
        )
        html: str = loader.render_to_string(
            f"saas_emails/{template_id}.text",
            context, request, using=using
        )
        return text, html
