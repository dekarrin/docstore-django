import uuid

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Topic, Folder, Document
from .serializers import TopicSerializer, FolderSerializer, DocumentSerializer

# Since we are using the rest framework, may want to see if we can use the mixins
# and APIView generics from DRF instead of manually typing these things out.
# TODO: check on use of Django REST Framework for view mixins.

class TopicListView(APIView):
    def get(self, request):
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
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
        serializer = FolderSerializer(folders, many=True)
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
