from __future__ import unicode_literals

from django.db import models
#from django.utils.text import slugify
from taggit.managers import TaggableManager
from autoslug import AutoSlugField

# Create your models here.
class Profile(models.Model):
    # Required fields
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    location = models.CharField(max_length=120)
    spotlight = models.CharField(max_length=120)
    image = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
    tags = TaggableManager()
    slug = AutoSlugField(
        populate_from='get_full_name',
        # slugify=lambda value: value.replace(' ', '-'),
        unique=True,
        blank=True,
        null=True
    )

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    def get_image_url(self):
        if self.image:
            return self.image.url
        else:
            return '/media/anon.jpg'

    def get_full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

