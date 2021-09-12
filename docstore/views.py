import uuid

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Topic
from .serializers import TopicSerializer

# Create your views here.
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
