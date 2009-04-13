from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from twitterpate.models import Post

class PostForm(ModelForm):
    message = forms.CharField(label='message', widget=forms.Textarea, error_messages={'required': 'Please enter a message.'}, max_length=255)
    class Meta:
        model = Post

