from rest_framework import serializers
from .models import Topic, Folder, Document

# TODO: look into serializers.ModelSerializer and whether it will default to
# the validation settings given here


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'path', 'name', 'folder', 'topics', 'contents']
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

# Doesn't include the topic's subjects, only gives the listings.
class TopicListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'short_desc', 'full_desc']

# Doesn't include the folder's contents, only gives the listings.
class FolderListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'path', 'name', 'parent', 'topics']