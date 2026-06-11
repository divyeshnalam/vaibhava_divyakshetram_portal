from rest_framework import serializers
from .models import (
    TempleInformation, HeroSlide, Sloka, Event,
    NewsAnnouncement, GalleryCategory, GalleryImage,
    Seva, ContactSubmission,
)


class TempleInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TempleInformation
        fields = [
            "temple_name_en", "temple_name_te",
            "history_en", "history_te",
            "address_en", "address_te",
            "phone_number", "email", "google_maps_link",
        ]


class HeroSlideSerializer(serializers.ModelSerializer):
    class Meta:
        model  = HeroSlide
        fields = ["id", "title_en", "title_te", "subtitle_en", "subtitle_te", "image", "display_order"]


class SlokaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Sloka
        fields = ["id", "title_en", "title_te", "content_en", "content_te", "display_order"]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Event
        fields = [
            "id", "title_en", "title_te",
            "description_en", "description_te",
            "significance_en", "significance_te",
            "image", "event_date", "event_time",
            "is_featured", "created_at",
        ]


class NewsAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model  = NewsAnnouncement
        fields = [
            "id", "title_en", "title_te",
            "content_en", "content_te",
            "publish_date", "expiry_date", "is_pinned",
        ]


class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = GalleryImage
        fields = ["id", "image", "caption_en", "caption_te", "display_order"]


class GalleryCategorySerializer(serializers.ModelSerializer):
    images = GalleryImageSerializer(many=True, read_only=True)

    class Meta:
        model  = GalleryCategory
        fields = ["id", "name_en", "name_te", "display_order", "images"]


class SevaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Seva
        fields = ["id", "name_en", "name_te", "description_en", "description_te", "image", "display_order"]


class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ContactSubmission
        fields = ["name", "phone_number", "email", "subject", "message"]

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be blank.")
        return value.strip()

    def validate_subject(self, value):
        if not value.strip():
            raise serializers.ValidationError("Subject cannot be blank.")
        return value.strip()

    def validate_message(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message cannot be blank.")
        return value.strip()