from rest_framework import serializers
from .models import Topic

# TODO: look into serializers.ModelSerializer and whether it will default to
# the validation settings given here

class TopicSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    short_desc = serializers.CharField(max_length=255)
    full_desc = serializers.CharField()

    def create(self, validated_data):
        """
        Create and return a new Topic instance from the validated data.
        """
        return Topic.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Topic instances with the validated data.
        """
        instance.short_desc = validated_data.get('short_desc', instance.short_desc)
        instance.long_desc = validated_data.get('long_desc', instance.long_desc)
        instance.save()
        return instance
    