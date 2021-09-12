import uuid

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Topic, Folder, Document
from .serializers import *

# Since we are using the rest framework, may want to see if we can use the mixins
# and APIView generics from DRF instead of manually typing these things out.
# TODO: check on use of Django REST Framework for view mixins.

class TopicListView(APIView):
    def get(self, request):
        topics = Topic.objects.values()
        serializer = TopicListingSerializer(topics, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TopicDetailView(APIView):
    def get(self, request, topic_id: uuid.UUID):
        try:
            t = Topic.objects.get(pk=topic_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TopicSerializer(t)
        return Response(serializer.data)

    def put(self, request, topic_id: uuid.UUID):
        try:
            t = Topic.objects.get(pk=topic_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = TopicSerializer(t, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, topic_id: uuid.UUID):
        try:
            t = Topic.objects.get(pk=topic_id)
        except ObjectDoesNotExist:
            # this isn't actually a problem, DELETE is idempotent and the
            # operation requested by the user has the result as the user would
            # expect, so just return 204.
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        t.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FolderListView(APIView):
    def get(self, request):
        folders = Folder.objects.all()

        # TOOD: To simplify, might want to pull out folder search into its own
        # view
        by_topic = request.query_params.get('topic')

        # TODO: allow multiple topic filters
        if by_topic:
            folders = folders.filter(topics__short_desc=by_topic)

        serializer = FolderListingSerializer(folders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FolderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FolderDetailView(APIView):
    def get(self, request, folder_id: uuid.UUID):
        try:
            f = Folder.objects.get(pk=folder_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = FolderSerializer(f)
        return Response(serializer.data)

    def put(self, request, folder_id: uuid.UUID):
        try:
            f = Folder.objects.get(pk=folder_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = FolderSerializer(f, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, folder_id: uuid.UUID):
        try:
            f = Folder.objects.get(pk=folder_id)
        except ObjectDoesNotExist:
            # this isn't actually a problem, DELETE is idempotent and the
            # operation requested by the user has the result as the user would
            # expect, so just return 204.
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        f.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DocumentListView(APIView):
    def get(self, request):
        docs = Document.objects.all()

        # TODO: To simplify, might want to pull out doc search into its own
        # view
        by_folder = request.query_params.get('folder')
        by_topic = request.query_params.get('topic')

        # TODO: make folder filter match on ANY folder in the full path
        # TODO: allow folder filter to give a full path, or glob
        if by_folder is not None:
            if by_folder == '':
                docs = docs.filter(folder__isnull=True)
            else:
                docs = docs.filter(folder__name=by_folder)

        # TODO: allow multiple topic filters
        if by_topic:
            docs = docs.filter(topics__short_desc=by_topic)

        serializer = DocumentSerializer(docs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentDetailView(APIView):
    def get(self, request, doc_id: uuid.UUID):
        try:
            d = Document.objects.get(pk=doc_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = DocumentSerializer(d)
        return Response(serializer.data)

    def put(self, request, doc_id: uuid.UUID):
        try:
            d = Document.objects.get(pk=doc_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = DocumentSerializer(d, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, doc_id: uuid.UUID):
        try:
            d = Document.objects.get(pk=doc_id)
        except ObjectDoesNotExist:
            # this isn't actually a problem, DELETE is idempotent and the
            # operation requested by the user has the result as the user would
            # expect, so just return 204.
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        d.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
