import uuid

from django.http import JsonResponse, HttpResponseNotFound
from django.http.response import HttpResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize

from .models import Topic

# Create your views here.
class TopicView(View):

    def get(self, request, topic_id: uuid.UUID):
        try:
            t = Topic.objects.get(id=topic_id)
        except ObjectDoesNotExist:
            return JsonResponse(data={'error': 'The requested topic does not exist'}, status=404)
        json_data = serialize('json', t)

        # Not sure how to get JsonResponse to accept Model directly; it seems to
        # want a dict but django's core JSON serialize() func does not
        # produce that.
        # TODO: look into above, also check Django REST framework instead of manual implementation
        return HttpResponse(json_data, content_type="application/json")
