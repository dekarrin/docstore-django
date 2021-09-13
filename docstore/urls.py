from django.urls import path

from .views import *

urlpatterns = [
    path('topics/', TopicListView.as_view()),
    path('topics/<uuid:topic_id>/', TopicDetailView.as_view()),
    path('folders/', FolderListView.as_view()),
    path('folders/<uuid:folder_id>/', FolderDetailView.as_view()),
    path('documents/', DocumentListView.as_view()),
    path('documents/<uuid:doc_id>/', DocumentDetailView.as_view()),
]
