from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager
from autoslug import AutoSlugField

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('email address'),
        unique=True,
        max_length=200
    )
    first_name = models.CharField(
        _('first name'),
        max_length=100,
        blank=True
    )
    last_name = models.CharField(
        _('last name'),
        max_length=100,
        blank=True
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        )
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        )
    )

    def get_full_name(self):
        return ('{0} {1}').format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'


class Spotlight(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Occupation(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Profile(models.Model):
    # Required fields
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    location = models.CharField(max_length=120)
    spotlight = models.ForeignKey(
            Spotlight,
            on_delete=models.CASCADE,
            related_name='profiles'
    )
    website = models.URLField(max_length=120)
    image = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
    tags = TaggableManager()

    # Optional fields
    bio = models.TextField(blank=True, null=True)
    school1 = models.CharField(max_length=150, blank=True, null=True)
    school2 = models.CharField(max_length=150, blank=True, null=True)
    occupations = models.ManyToManyField(
            Occupation,
            related_name='profiles'
    )

    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
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
