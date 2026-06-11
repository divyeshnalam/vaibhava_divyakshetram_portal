from django.urls import path
from .views import (
    HomeAPIView, AboutAPIView, EventListAPIView,
    NewsListAPIView, GalleryAPIView, SevaListAPIView,
    ContactSubmissionCreateView,
)

urlpatterns = [
    path("home/",    HomeAPIView.as_view(),               name="api-home"),
    path("about/",   AboutAPIView.as_view(),              name="api-about"),
    path("events/",  EventListAPIView.as_view(),          name="api-events"),
    path("news/",    NewsListAPIView.as_view(),            name="api-news"),
    path("gallery/", GalleryAPIView.as_view(),            name="api-gallery"),
    path("sevas/",   SevaListAPIView.as_view(),            name="api-sevas"),
    path("contact/", ContactSubmissionCreateView.as_view(), name="api-contact"),
]