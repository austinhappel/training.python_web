from django.db import models
from taggit.managers import TaggableManager


# Create your models here.
class BlogPost(models.Model):
    """BlogPost"""

    title = models.CharField(max_length=255)
    content = models.TextField(null=True)
    tags = TaggableManager()

    def __unicode__(self):
        return self.title
