from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import HeroSlide, Event, GalleryImage, Seva


MODELS_WITH_IMAGES = [
    HeroSlide,
    Event,
    GalleryImage,
    Seva,
]


for model in MODELS_WITH_IMAGES:

    @receiver(post_delete, sender=model)
    def delete_file_on_delete(sender, instance, **kwargs):
        """
        Delete file from R2 when object is deleted.
        """
        image = getattr(instance, "image", None)

        if image:
            image.delete(save=False)


    @receiver(pre_save, sender=model)
    def delete_old_file_on_change(sender, instance, **kwargs):
        """
        Delete old file from R2 when image is replaced.
        """
        if not instance.pk:
            return

        try:
            old_instance = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            return

        old_file = getattr(old_instance, "image", None)
        new_file = getattr(instance, "image", None)

        if old_file and old_file != new_file:
            old_file.delete(save=False)