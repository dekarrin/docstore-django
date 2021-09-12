import uuid

from django.http import JsonResponse, HttpResponseNotFound
from django.http.response import HttpResponse, HttpResponseNotAllowed, HttpResponseServerError
from django.views import View
from django.core.exceptions import ObjectDoesNotExist


from . import util
from .models import Topic

# Create your views here.
class TopicView(View):

    def put(self, request, topic_id: uuid.UUID=None):
        if topic_id is None:
            return JsonResponse(status=405, data={'error': 'Method PUT not allowed at this resource'})

        payload = request.read()
        try:
            parsed = util.deserialize_models(payload, expect_single_object=True, default_id=str(topic_id))
        except util.ModelParseError as e:
            return JsonResponse(status=400, data={'error': "Body does not contain a valid Topic: {!s}".format(e)})

        # deserialize_models will have ensured that there is only one item here:
        for deserialized_object in parsed:
            deserialized_object.id = topic_id
            deserialized_object.save()

        # success
        return JsonResponse(status=204)
        

    def get(self, request, topic_id: uuid.UUID=None):
        if topic_id is None:
            json_data = util.serialize_models(Topic.objects.all())
            return HttpResponse(json_data, content_type="application/json")

        try:
            t = Topic.objects.get(id=topic_id)
        except ObjectDoesNotExist:
            return JsonResponse(status=404, data={'error': 'The requested topic does not exist'})
        
        json_data = util.serialize_models(t)
        # Not sure how to get JsonResponse to accept Model directly; it seems to
        # want a dict but django's core JSON serialize() func does not
        # produce that.
        # TODO: look into above, also check Django REST framework instead of manual implementation
        return HttpResponse(json_data, content_type="application/json")