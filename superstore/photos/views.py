from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse


from superstore.core.utils import is_owner
from superstore.photos.forms import ToyCreateForm, ToyEditForm, ToyDeleteForm
from superstore.photos.models import Toy


def get_post_photo_form(request, form, success_url, template_path, pk=None):

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(success_url)

    context = {
        'form': form,
        'pk': pk,
    }

    return render(request, template_path, context)


@login_required
def add_photo(request):
    if request.method == 'GET':
        form = ToyCreateForm()
    else:
        form = ToyCreateForm(request.POST, request.FILES)
        if form.is_valid():
            toy = form.save(commit=False)
            toy.user = request.user
            toy.save()
            form.save_m2m()
            return redirect('details photo', pk=toy.pk)
    context = {
        'form': form,
    }
    return render(request, 'photos/photo-add-page.html', context,)


def details_photo(request, pk):
    toy = Toy.objects.get(pk=pk)
    likes = toy.like_set.all()
    comments = toy.comment_set.all()

    user_like_toys = Toy.objects.filter(pk=pk, user_id=request.user.pk)
    context = {
        "toy": toy,
        "likes": likes,
        "comments": comments,
        'has_user_liked_toy': user_like_toys,
        'likes_count': toy.like_set.count(),
        'is_owner': request.user == toy.user,
    }
    return render(request, 'photos/photo-details-page.html', context)


def edit_photo(request, pk):
    toy = Toy.objects.filter(pk=pk).get()

    if not is_owner(request, toy):
        return redirect('index')

    return get_post_photo_form(
        request,
        ToyEditForm(request.POST or None, instance=toy),
        success_url=reverse('index'),
        template_path='photos/photo-edit-page.html',
        pk=pk,
    )


def delete_photo(request, pk):
    toy = Toy.objects.filter(pk=pk) \
        .get()
    return get_post_photo_form(
        request,
        ToyDeleteForm(request.POST or None, instance=toy),
        success_url=reverse('index'),
        template_path='photos/photo-delete-page.html',
        pk=pk,
    )


