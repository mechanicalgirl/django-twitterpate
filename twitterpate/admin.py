import os, sys

from django.contrib import admin

import twitterpate.twitterpost
from twitterpate.models import Post

class PostAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.approved: twitterpost.main()
    list_filter = ('approved',)
    ordering = ('submit_date',)
    list_display = ('message', 'submit_date', 'approved', 'posted', 'post_date', 'twitter_id')

