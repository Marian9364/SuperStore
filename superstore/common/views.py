from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.decorators import login_required

from pyperclip import copy

from superstore.common.forms import ToyCommentForm, SearchForm
from superstore.common.models import Like
from superstore.photos.models import Toy
# Create your views here.

def apply_likes_count(toy):
    toy.likes_count = toy.like_set.count()
    return toy


def apply_user_liked_toy(toy):
    #TODO: fix this when current user authentication is available
    toy.is_liked_by_user = toy.likes_count > 0
    return toy


def index(request):
    comment_form = ToyCommentForm()
    search_form = SearchForm(request.GET)
    search_pattern = None
    if search_form.is_valid():
        search_pattern = search_form.cleaned_data['toy_name']

    toys = Toy.objects.all()
    if search_pattern:
        toys = toys.filter(toy_name__icontains=search_pattern)

    toys = [apply_likes_count(toy) for toy in toys]
    toys = [apply_user_liked_toy(toy) for toy in toys]

    context = {
        'toys': toys,
        'comment_form': comment_form,
        'search_form': search_form,
    }
    return render(request, 'common/home-page.html', context)


@login_required()
def like_toy(request, toy_id):
    toy = Toy.objects.get(id=toy_id)
    liked_object = Like.objects.filter(to_toy_id=toy_id, user=request.user)

    if liked_object:
        liked_object.delete()
    else:
        like = Like(to_toy=toy, user=request.user)
        like.save()

    return redirect(request.META['HTTP_REFERER'] + f'#photo-{toy_id}')


def copy_link_to_clipboard(request, toy_id):
    copy(request.META['HTTP_HOST'] + resolve_url('details photo', toy_id))

    return redirect(request.META['HTTP_REFERER'] + f'#{toy_id}')


@login_required()
def comment_toy(request, toy_id):
    if request.method == 'POST':
        toy = Toy.objects.filter(pk=toy_id).get()
        form = ToyCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.to_toy = toy
            comment.user = request.user
            comment.save()
        return redirect('index')


