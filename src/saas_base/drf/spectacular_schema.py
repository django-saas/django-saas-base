from drf_spectacular.authentication import SessionScheme as _SessionScheme
from drf_spectacular.extensions import OpenApiSerializerFieldExtension


class SessionScheme(_SessionScheme):
    target_class = 'saas_base.drf.authentication.SessionAuthentication'


class ChoiceFieldFix(OpenApiSerializerFieldExtension):
    target_class = 'saas_base.drf.serializers.ChoiceField'

    def map_serializer_field(self, auto_schema, direction):
        choices = list(self.target.choices.values())
        return {'type': 'string', 'enum': choices}
