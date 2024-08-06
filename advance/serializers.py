from rest_framework import serializers
from .models import Setting

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ['id', 'name', 'value', 'value_type']

    def to_representation(self, instance):
        """Converts the value field to its appropriate type based on value_type."""
        representation = super().to_representation(instance)
        value_type = representation['value_type']
        value = representation['value']

        if value_type == 'int':
            representation['value'] = int(value)
        elif value_type == 'bool':
            representation['value'] = value.lower() in ('true', '1')
        elif value_type == 'float':
            representation['value'] = float(value)
        elif value_type == 'json':
            import json
            representation['value'] = json.loads(value)

        return representation

    def validate(self, data):
        """Validates the value field based on the value_type."""
        value = data.get('value')
        value_type = data.get('value_type')

        if value_type == 'int':
            try:
                int(value)
            except ValueError:
                raise serializers.ValidationError({'value': 'Must be an integer.'})
        elif value_type == 'bool':
            if value.lower() not in ('true', 'false', '1', '0'):
                raise serializers.ValidationError({'value': 'Must be a boolean.'})
        elif value_type == 'float':
            try:
                float(value)
            except ValueError:
                raise serializers.ValidationError({'value': 'Must be a float.'})
        elif value_type == 'json':
            try:
                import json
                json.loads(value)
            except ValueError:
                raise serializers.ValidationError({'value': 'Must be valid JSON.'})

        return data
