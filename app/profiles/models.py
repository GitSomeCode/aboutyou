from __future__ import unicode_literals

from django.db import models
from taggit.managers import TaggableManager

# Create your models here.
class Profile(models.Model):
	first_name = models.CharField(max_length=70)
	last_name = models.CharField(max_length=70)
	location = models.CharField(max_length=120)
	spotlight = models.CharField(max_length=120)
	image = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
	tags = TaggableManager()

	def __unicode__(self):
		return self.first_name + ' ' + self.last_name

	def get_image_url(self):
		if self.image:
			return self.image.url
		else:
			return '/media/anon.jpg'

