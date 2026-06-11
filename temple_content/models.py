from django.core.exceptions import ValidationError
from django.db import models
from auditlog.registry import auditlog


def validate_singleton(instance):
    model = instance.__class__
    if model.objects.exclude(pk=instance.pk).exists():
        raise ValidationError(
            f"Only one {model.__name__} record is allowed. "
            "Please edit the existing record instead of creating a new one."
        )


# ── 1. TempleInformation (singleton) ─────────────────────

class TempleInformation(models.Model):
    temple_name_en   = models.CharField(max_length=255, verbose_name="Temple Name (English)")
    temple_name_te   = models.CharField(max_length=255, verbose_name="Temple Name (Telugu)")
    history_en       = models.TextField(verbose_name="History (English)")
    history_te       = models.TextField(verbose_name="History (Telugu)")
    address_en       = models.TextField(verbose_name="Address (English)")
    address_te       = models.TextField(verbose_name="Address (Telugu)")
    phone_number     = models.CharField(max_length=20, verbose_name="Phone Number")
    email            = models.EmailField(verbose_name="Email Address")
    google_maps_link = models.URLField(max_length=500, blank=True, verbose_name="Google Maps Link")

    class Meta:
        verbose_name        = "Temple Information"
        verbose_name_plural = "Temple Information"

    def clean(self):
        validate_singleton(self)

    def __str__(self):
        return self.temple_name_en


# ── 2. HeroSlide ─────────────────────────────────────────

class HeroSlide(models.Model):
    title_en      = models.CharField(max_length=255, verbose_name="Title (English)")
    title_te      = models.CharField(max_length=255, verbose_name="Title (Telugu)")
    subtitle_en   = models.CharField(max_length=500, blank=True, verbose_name="Subtitle (English)")
    subtitle_te   = models.CharField(max_length=500, blank=True, verbose_name="Subtitle (Telugu)")
    image         = models.ImageField(upload_to="hero_slides/", verbose_name="Slide Image")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    is_active     = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        verbose_name        = "Hero Slide"
        verbose_name_plural = "Hero Slides"
        ordering            = ["display_order"]

    def __str__(self):
        return self.title_en


# ── 3. Sloka ─────────────────────────────────────────────

class Sloka(models.Model):
    title_en      = models.CharField(max_length=255, verbose_name="Title (English)")
    title_te      = models.CharField(max_length=255, verbose_name="Title (Telugu)")
    content_en    = models.TextField(verbose_name="Sloka Content (English)")
    content_te    = models.TextField(verbose_name="Sloka Content (Telugu)")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    is_active     = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        verbose_name        = "Sloka"
        verbose_name_plural = "Slokas"
        ordering            = ["display_order"]

    def __str__(self):
        return self.title_en


# ── 4. Event ─────────────────────────────────────────────

class Event(models.Model):
    title_en        = models.CharField(max_length=255, verbose_name="Title (English)")
    title_te        = models.CharField(max_length=255, verbose_name="Title (Telugu)")
    description_en  = models.TextField(verbose_name="Description (English)")
    description_te  = models.TextField(verbose_name="Description (Telugu)")
    significance_en = models.TextField(blank=True, verbose_name="Significance (English)")
    significance_te = models.TextField(blank=True, verbose_name="Significance (Telugu)")
    image           = models.ImageField(upload_to="events/", blank=True, null=True, verbose_name="Event Image")
    event_date      = models.DateField(verbose_name="Event Date")
    event_time      = models.TimeField(blank=True, null=True, verbose_name="Event Time")
    is_featured     = models.BooleanField(default=False, verbose_name="Featured")
    is_published    = models.BooleanField(default=False, verbose_name="Published")
    created_at      = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name        = "Event"
        verbose_name_plural = "Events"
        ordering            = ["-event_date"]

    def __str__(self):
        return self.title_en


# ── 5. NewsAnnouncement ───────────────────────────────────

class NewsAnnouncement(models.Model):
    title_en     = models.CharField(max_length=255, verbose_name="Title (English)")
    title_te     = models.CharField(max_length=255, verbose_name="Title (Telugu)")
    content_en   = models.TextField(verbose_name="Content (English)")
    content_te   = models.TextField(verbose_name="Content (Telugu)")
    publish_date = models.DateField(verbose_name="Publish Date")
    expiry_date  = models.DateField(blank=True, null=True, verbose_name="Expiry Date")
    is_pinned    = models.BooleanField(default=False, verbose_name="Pinned")
    is_published = models.BooleanField(default=False, verbose_name="Published")

    class Meta:
        verbose_name        = "News & Announcement"
        verbose_name_plural = "News & Announcements"
        ordering            = ["-is_pinned", "-publish_date"]

    def __str__(self):
        return self.title_en


# ── 6. GalleryCategory ───────────────────────────────────

class GalleryCategory(models.Model):
    name_en       = models.CharField(max_length=255, verbose_name="Category Name (English)")
    name_te       = models.CharField(max_length=255, verbose_name="Category Name (Telugu)")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")

    class Meta:
        verbose_name        = "Gallery Category"
        verbose_name_plural = "Gallery Categories"
        ordering            = ["display_order"]

    def __str__(self):
        return self.name_en


# ── 7. GalleryImage ──────────────────────────────────────

class GalleryImage(models.Model):
    category      = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, related_name="images", verbose_name="Category")
    image         = models.ImageField(upload_to="gallery/", verbose_name="Image")
    caption_en    = models.CharField(max_length=500, blank=True, verbose_name="Caption (English)")
    caption_te    = models.CharField(max_length=500, blank=True, verbose_name="Caption (Telugu)")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    is_active     = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        verbose_name        = "Gallery Image"
        verbose_name_plural = "Gallery Images"
        ordering            = ["display_order"]

    def __str__(self):
        return f"{self.category.name_en} – #{self.pk}"


# ── 8. Seva (strictly informational) ─────────────────────

class Seva(models.Model):
    name_en        = models.CharField(max_length=255, verbose_name="Seva Name (English)")
    name_te        = models.CharField(max_length=255, verbose_name="Seva Name (Telugu)")
    description_en = models.TextField(verbose_name="Description (English)")
    description_te = models.TextField(verbose_name="Description (Telugu)")
    image          = models.ImageField(upload_to="sevas/", blank=True, null=True, verbose_name="Seva Image")
    display_order  = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    is_active      = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        verbose_name        = "Seva"
        verbose_name_plural = "Sevas"
        ordering            = ["display_order"]

    def __str__(self):
        return self.name_en


# ── 9. ContactSubmission ─────────────────────────────────

class ContactSubmission(models.Model):
    name         = models.CharField(max_length=255, verbose_name="Full Name")
    phone_number = models.CharField(max_length=20, verbose_name="Phone Number")
    email        = models.EmailField(verbose_name="Email Address")
    subject      = models.CharField(max_length=255, verbose_name="Subject")
    message      = models.TextField(verbose_name="Message")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Submitted At")
    is_resolved  = models.BooleanField(default=False, verbose_name="Resolved")

    class Meta:
        verbose_name        = "Contact Submission"
        verbose_name_plural = "Contact Submissions"
        ordering            = ["-submitted_at"]

    def __str__(self):
        return f"{self.name} – {self.subject} ({self.submitted_at.date()})"


# ── Auditlog Registration ─────────────────────────────────

auditlog.register(TempleInformation)
auditlog.register(HeroSlide)
auditlog.register(Sloka)
auditlog.register(Event)
auditlog.register(NewsAnnouncement)
auditlog.register(GalleryCategory)
auditlog.register(GalleryImage)
auditlog.register(Seva)
auditlog.register(ContactSubmission)