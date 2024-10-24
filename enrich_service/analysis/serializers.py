from rest_framework import serializers
from analysis.models import BatchProfilePayload

class ContactBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchProfilePayload
        fields = "__all__"

class ResponseContactBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchProfilePayload
        fields = ["migrationId","tableName","recordId","uuid"]