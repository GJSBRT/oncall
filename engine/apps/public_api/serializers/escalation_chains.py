from rest_framework import serializers

from apps.alerts.models import EscalationChain
from common.api_helpers.custom_fields import TeamPrimaryKeyRelatedField
from common.api_helpers.mixins import EagerLoadingMixin
from common.api_helpers.utils import CurrentOrganizationDefault


class EscalationChainSerializer(EagerLoadingMixin, serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="public_primary_key")
    organization = serializers.HiddenField(default=CurrentOrganizationDefault())
    team_id = TeamPrimaryKeyRelatedField(required=False, allow_null=True, source="team")

    SELECT_RELATED = ["organization", "team"]

    class Meta:
        model = EscalationChain
        fields = (
            "id",
            "name",
            "organization",
            "team_id",
        )
