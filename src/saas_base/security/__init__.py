import typing as t
import logging
from rest_framework.request import Request
from saas.drf.errors import BadRequest
from .rules import Rule

logger = logging.getLogger(__name__)


def check_security_rules(security_rules: t.List[Rule], request: Request):
    for rule in security_rules:
        if rule.bad_request(request):
            rule_name = rule.__class__.__name__
            logger.warning(f"Bad request: [{rule_name}].")
            raise BadRequest()
