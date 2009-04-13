from django.db import models
from django.http import Http404
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

class Post(models.Model):
    """
    """
    message = models.CharField("Message", max_length=255, unique=True)
    submit_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    posted = models.BooleanField(default=False)
    post_date = models.DateTimeField(null=True, blank=True, editable=False)
    twitter_id = models.IntegerField(null=True, blank=True, editable=False)

    class Meta:
        ordering = ['-post_date']


