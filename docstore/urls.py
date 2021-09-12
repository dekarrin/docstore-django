from django.urls import path

from .views import TopicView

urlpatterns = [
    path('topics/', TopicView.as_view()),
    path('topics/<uuid:topic_id>', TopicView.as_view()),
]
