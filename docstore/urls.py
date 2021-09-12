from django.urls import path

from .views import TopicListView, TopicDetailView

urlpatterns = [
    path('topics/', TopicListView.as_view()),
    path('topics/<uuid:topic_id>', TopicDetailView.as_view()),
]
