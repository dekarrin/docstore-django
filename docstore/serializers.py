from rest_framework import serializers
from .models import Topic, Folder, Document

# TODO: look into serializers.ModelSerializer and whether it will default to
# the validation settings given here


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'path', 'name', 'folder', 'topics']
        extra_kwargs = {'topics': {'required': False}}


class FolderSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Folder
        fields = ['id', 'path', 'name', 'parent', 'topics', 'documents']
        extra_kwargs = {
            'topics': {'required': False},
            'documents': {'required': False},
        }


class TopicSerializer(serializers.ModelSerializer):
    folders = FolderSerializer(many=True, read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Topic
        fields = ['id', 'short_desc', 'full_desc', 'folders', 'documents']
        extra_kwargs = {
            'folders': {'required': False},
            'documents': {'required': False}
        }