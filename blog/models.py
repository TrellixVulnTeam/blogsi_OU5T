from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
#from ckeditor.fields import RichTextField

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextUploadingField()
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # Change to String obj. for simple reading into Admin panel
    def __str__(self):
        return self.title

    # Return full URL als String from rout and make redirect bei created new post
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
