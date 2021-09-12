import uuid

from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser

from .models import Topic
from .serializers import TopicSerializer

# Create your views here.
class TopicListView(View):
    def get(self, request):
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = TopicSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class TopicDetailView(View):
    def get(self, request, topic_id: uuid.UUID):
        try:
            t = Topic.objects.get(pk=topic_id)
        except ObjectDoesNotExist:
            return JsonResponse(status=404, data={'error': 'No topic with the requested ID exists'})

        serializer = TopicSerializer(t)
        return JsonResponse(serializer.data)

    def put(self, request, topic_id: uuid.UUID):
        try:
            t = Topic.objects.get(pk=topic_id)
        except ObjectDoesNotExist:
            return JsonResponse(status=404, data={'error': 'No topic with the requested ID exists'})
        
        data = JSONParser().parse(request)
        serializer = TopicSerializer(t, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, topic_id: uuid.UUID):
        try:
            t = Topic.objects.get(pk=topic_id)
        except ObjectDoesNotExist:
            # this isn't actually a problem, DELETE is idempotent and the
            # operation requested by the user has the result as the user would
            # expect, so just return 204.
            return JsonResponse(status=204)
        
        t.delete()
        return JsonResponse(status=204)
