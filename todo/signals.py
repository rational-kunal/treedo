from .models import Todo
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Todo)
def falsify_parent_todo(sender, instance, **kwargs):
    if not instance.is_complete and instance.parent_todo:
        parent = instance.parent_todo
        parent.is_complete = False
        parent.save()
