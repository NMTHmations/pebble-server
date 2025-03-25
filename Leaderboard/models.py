from django.db import models
from django.core.validators import FileExtensionValidator


def user_directory_path(instance, filename):
    # If the instance is new and doesn't have an ID yet, assign a temporary unique ID
    if not instance.pk:
        return f"uploads/temp/{filename}"
    return f"uploads/{instance.id}/{filename}"

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255,null=False)
    max_velocity = models.FloatField(null=False)
    distance = models.FloatField(null=False)
    video_source = models.FileField(upload_to=user_directory_path,null=True,validators=[FileExtensionValidator(['mp4'])])
    created_at = models.DateTimeField(null=True,auto_now=True)