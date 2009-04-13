import datetime

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string

from twitterpate.models import Post
from twitterpate.forms import PostForm

def show_all(request, form=PostForm):
    template_name = 'all.html'
    context = {}
    message = ''
    per_page = 5
    page = int(request.GET.get('page', '1'))

    try:
        all_tweets = Post.objects.filter(posted=True).order_by('-post_date', '-id')
    except ObjectDoesNotExist:
	all_tweets = None

    if request.method == 'POST':
        form = form(request.POST)
        if form.is_valid():
	    message = form.cleaned_data['message']
            form.save()
    else:
        form = form()
   
    context['form'] = form
    context['message'] = message

    for tweet in all_tweets:
	tweet.post_date = datetime.datetime(tweet.post_date.year, tweet.post_date.month, tweet.post_date.day)
	tweet.post_date = tweet.post_date.strftime("%m-%d-%Y")

    total_entries = all_tweets.count()
    total_pages = (total_entries/per_page)+1
    context['page_range'] = range(1, total_pages+1)

    offset = (page * per_page) - per_page
    limit = offset + per_page
    all_tweets = all_tweets[offset:limit]
    context['tweet_list'] = all_tweets

    return render_to_response(template_name, context, context_instance=RequestContext(request))

def show_id(request, id, form=PostForm):
    """
    """
    template_name = 'single.html'
    context = {}

    try:
        tweet = Post.objects.get(pk=id, posted=True)
        tweet.post_date = datetime.datetime(tweet.post_date.year, tweet.post_date.month, tweet.post_date.day)
        tweet.post_date = tweet.post_date.strftime("%m-%d-%Y")
    except ObjectDoesNotExist:
        tweet = None
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = form(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            form.save()
    else:
        form = form()

    context['form'] = form
    context['tweet'] = tweet
    return render_to_response(template_name, context, context_instance=RequestContext(request))


