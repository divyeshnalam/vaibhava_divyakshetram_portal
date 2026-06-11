from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .models import (
    TempleInformation, HeroSlide, Sloka, Event,
    NewsAnnouncement, GalleryCategory, GalleryImage,
    Seva, ContactSubmission,
)
from .serializers import (
    TempleInformationSerializer, HeroSlideSerializer, SlokaSerializer,
    EventSerializer, NewsAnnouncementSerializer, GalleryCategorySerializer,
    SevaSerializer, ContactSubmissionSerializer,
)

from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse


# GET /api/home/
class HomeAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        hero_slides     = HeroSlide.objects.filter(is_active=True).order_by("display_order")
        slokas          = Sloka.objects.filter(is_active=True).order_by("display_order")
        featured_events = Event.objects.filter(is_published=True, is_featured=True).order_by("-event_date")[:5]
        pinned_news     = NewsAnnouncement.objects.filter(is_published=True, is_pinned=True).order_by("-publish_date")[:5]

        return Response({
            "hero_slides":      HeroSlideSerializer(hero_slides, many=True, context={"request": request}).data,
            "slokas":           SlokaSerializer(slokas, many=True).data,
            "featured_events":  EventSerializer(featured_events, many=True, context={"request": request}).data,
            "pinned_news":      NewsAnnouncementSerializer(pinned_news, many=True).data,
        })


# GET /api/about/
class AboutAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        temple_info = TempleInformation.objects.first()
        slokas      = Sloka.objects.filter(is_active=True).order_by("display_order")

        return Response({
            "temple_information": TempleInformationSerializer(temple_info).data if temple_info else None,
            "slokas":             SlokaSerializer(slokas, many=True).data,
        })


# GET /api/events/
class EventListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(is_published=True).order_by("-event_date")

    def get_serializer_context(self):
        return {"request": self.request}


# GET /api/news/
class NewsListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = NewsAnnouncementSerializer

    def get_queryset(self):
        return NewsAnnouncement.objects.filter(is_published=True).order_by("-is_pinned", "-publish_date")


# GET /api/gallery/
class GalleryAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = GalleryCategorySerializer

    def get_queryset(self):
        return GalleryCategory.objects.prefetch_related("images").order_by("display_order")

    def get_serializer_context(self):
        return {"request": self.request}


# GET /api/sevas/
class SevaListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SevaSerializer

    def get_queryset(self):
        return Seva.objects.filter(is_active=True).order_by("display_order")

    def get_serializer_context(self):
        return {"request": self.request}


# POST /api/contact/
class ContactSubmissionCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ContactSubmissionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Your message has been received. We will get back to you shortly."},
            status=status.HTTP_201_CREATED,
        )
        

@staff_member_required
def dashboard_counts(request):
    return JsonResponse({
        "temple_information":   TempleInformation.objects.count(),
        "hero_slides":          HeroSlide.objects.count(),
        "slokas":               Sloka.objects.count(),
        "events":               Event.objects.count(),
        "news_announcements":   NewsAnnouncement.objects.count(),
        "gallery_categories":   GalleryCategory.objects.count(),
        "gallery_images":       GalleryImage.objects.count(),
        "sevas":                Seva.objects.count(),
        "contact_submissions":  ContactSubmission.objects.count(),
    })