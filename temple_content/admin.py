from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ExportMixin

from .models import (
    TempleInformation, HeroSlide, Sloka, Event,
    NewsAnnouncement, GalleryCategory, GalleryImage,
    Seva, ContactSubmission,
)


def image_preview(obj, field_name="image", width=120):
    img = getattr(obj, field_name, None)
    if img:
        return format_html(
            '<img src="{}" width="{}" style="border-radius:4px;object-fit:cover;" />',
            img.url, width,
        )
    return "—"

image_preview.short_description = "Preview"


# ── TempleInformation ─────────────────────────────────────

@admin.register(TempleInformation)
class TempleInformationAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Temple Name",   {"fields": ("temple_name_en", "temple_name_te")}),
        ("History",       {"fields": ("history_en", "history_te")}),
        ("Address",       {"fields": ("address_en", "address_te")}),
        ("Contact Details", {"fields": ("phone_number", "email", "google_maps_link")}),
    )

    def has_add_permission(self, request):
        return not TempleInformation.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ── HeroSlide ─────────────────────────────────────────────

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display   = ("title_en", "title_te", "display_order", "is_active", "slide_preview")
    list_editable  = ("display_order", "is_active")
    list_filter    = ("is_active",)
    search_fields  = ("title_en", "title_te", "subtitle_en", "subtitle_te")
    ordering       = ("display_order",)
    readonly_fields = ("slide_preview",)
    fieldsets = (
        ("Titles",          {"fields": ("title_en", "title_te")}),
        ("Subtitles",       {"fields": ("subtitle_en", "subtitle_te")}),
        ("Image & Display", {"fields": ("image", "slide_preview", "display_order", "is_active")}),
    )

    def slide_preview(self, obj):
        return image_preview(obj, "image", width=160)
    slide_preview.short_description = "Image Preview"


# ── Sloka ─────────────────────────────────────────────────

@admin.register(Sloka)
class SlokaAdmin(admin.ModelAdmin):
    list_display  = ("title_en", "title_te", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    list_filter   = ("is_active",)
    search_fields = ("title_en", "title_te", "content_en", "content_te")
    ordering      = ("display_order",)
    fieldsets = (
        ("Titles",  {"fields": ("title_en", "title_te")}),
        ("Content", {"fields": ("content_en", "content_te")}),
        ("Display", {"fields": ("display_order", "is_active")}),
    )


# ── Event ─────────────────────────────────────────────────

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display   = ("title_en", "event_date", "event_time", "is_featured", "is_published", "event_image_preview")
    list_editable  = ("is_featured", "is_published")
    list_filter    = ("is_featured", "is_published", "event_date")
    search_fields  = ("title_en", "title_te", "description_en", "description_te")
    ordering       = ("-event_date",)
    date_hierarchy = "event_date"
    readonly_fields = ("created_at", "event_image_preview")
    fieldsets = (
        ("Titles",       {"fields": ("title_en", "title_te")}),
        ("Description",  {"fields": ("description_en", "description_te")}),
        ("Significance", {"fields": ("significance_en", "significance_te"), "classes": ("collapse",)}),
        ("Date & Time",  {"fields": ("event_date", "event_time")}),
        ("Image",        {"fields": ("image", "event_image_preview")}),
        ("Visibility",   {"fields": ("is_featured", "is_published")}),
    )

    def event_image_preview(self, obj):
        return image_preview(obj, "image", width=160)
    event_image_preview.short_description = "Image Preview"


# ── NewsAnnouncement ──────────────────────────────────────

@admin.register(NewsAnnouncement)
class NewsAnnouncementAdmin(admin.ModelAdmin):
    list_display   = ("title_en", "publish_date", "expiry_date", "is_pinned", "is_published")
    list_editable  = ("is_pinned", "is_published")
    list_filter    = ("is_pinned", "is_published", "publish_date")
    search_fields  = ("title_en", "title_te", "content_en", "content_te")
    ordering       = ("-is_pinned", "-publish_date")
    date_hierarchy = "publish_date"
    fieldsets = (
        ("Titles",              {"fields": ("title_en", "title_te")}),
        ("Content",             {"fields": ("content_en", "content_te")}),
        ("Dates & Visibility",  {"fields": ("publish_date", "expiry_date", "is_pinned", "is_published")}),
    )


# ── GalleryCategory ───────────────────────────────────────

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display  = ("name_en", "name_te", "display_order")
    list_editable = ("display_order",)
    search_fields = ("name_en", "name_te")
    ordering      = ("display_order",)


# ── GalleryImage ──────────────────────────────────────────

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display   = ("gallery_image_preview", "category", "caption_en", "display_order", "is_active")
    list_editable  = ("display_order", "is_active")
    list_filter    = ("category", "is_active")
    search_fields  = ("caption_en", "caption_te", "category__name_en")
    ordering       = ("display_order",)
    readonly_fields = ("gallery_image_preview",)
    fieldsets = (
        ("Image",    {"fields": ("category", "image", "gallery_image_preview")}),
        ("Captions", {"fields": ("caption_en", "caption_te")}),
        ("Display",  {"fields": ("display_order", "is_active")}),
    )

    def gallery_image_preview(self, obj):
        return image_preview(obj, "image", width=140)
    gallery_image_preview.short_description = "Preview"


# ── Seva ──────────────────────────────────────────────────

@admin.register(Seva)
class SevaAdmin(admin.ModelAdmin):
    list_display   = ("name_en", "name_te", "display_order", "is_active", "seva_image_preview")
    list_editable  = ("display_order", "is_active")
    list_filter    = ("is_active",)
    search_fields  = ("name_en", "name_te", "description_en", "description_te")
    ordering       = ("display_order",)
    readonly_fields = ("seva_image_preview",)
    fieldsets = (
        ("Names",       {"fields": ("name_en", "name_te")}),
        ("Description", {"fields": ("description_en", "description_te")}),
        ("Image & Display", {"fields": ("image", "seva_image_preview", "display_order", "is_active")}),
    )

    def seva_image_preview(self, obj):
        return image_preview(obj, "image", width=140)
    seva_image_preview.short_description = "Image Preview"


# ── ContactSubmission ─────────────────────────────────────

class ContactSubmissionResource(resources.ModelResource):
    class Meta:
        model = ContactSubmission
        fields = ("id", "name", "phone_number", "email", "subject", "message", "submitted_at", "is_resolved")
        export_order = fields


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(ExportMixin, admin.ModelAdmin):
    resource_classes = [ContactSubmissionResource]
    list_display    = ("name", "email", "phone_number", "subject", "submitted_at", "is_resolved")
    list_editable   = ("is_resolved",)
    list_filter     = ("is_resolved", "submitted_at")
    search_fields   = ("name", "email", "phone_number", "subject", "message")
    ordering        = ("-submitted_at",)
    date_hierarchy  = "submitted_at"
    readonly_fields = ("name", "phone_number", "email", "subject", "message", "submitted_at")
    fieldsets = (
        ("Sender",  {"fields": ("name", "phone_number", "email")}),
        ("Message", {"fields": ("subject", "message")}),
        ("Meta",    {"fields": ("submitted_at", "is_resolved")}),
    )

    def has_add_permission(self, request):
        return False