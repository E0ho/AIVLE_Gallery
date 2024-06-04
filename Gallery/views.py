import base64

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages

from Gallery.models import Picture, Comment, Love
from GalleryUser.models import User
from .forms import *


def gallery_list(request):
    gallery_list = Picture.objects.all()
    context = {'gallery_li': gallery_list}
    return render(request, 'gallery/gallery.html', context)


def detail(request, picture_id):
    if picture_id is not None:
        picture = get_object_or_404(Picture, picture_id=picture_id)
        image_data = base64.b64encode(picture.image).decode()
        return render(request, "detail.html",
                      {"picture": picture, 'img': image_data})


def delete_post(request, picture_id):
    picture = get_object_or_404(Picture, picture_id=picture_id)
    if request.user == picture.user_id:
        picture.delete()
        return redirect('gallery:index')
    else:
        messages.warning(request, "권한이 없습니다.")
        return redirect('gallery:detail', picture_id=picture_id)


def update_post(request, picture_id):
    picture = get_object_or_404(Picture, pk=picture_id)
    image = picture.image
    if request.user == picture.user_id:
        if request.method == 'POST':
            form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                picture.title = form.cleaned_data['title']
                picture.image = form.cleaned_data['image'].read()
                picture.content = form.cleaned_data['content']
                picture.user_id = request.user
                picture.save()
                return redirect('gallery:index')
            else:
                picture.title = form.cleaned_data['title']
                picture.image = image
                picture.content = form.cleaned_data['content']
                picture.user_id = request.user
                picture.save()
                return redirect('gallery:index')
        else:
            form = ImageUploadForm(initial={'title': picture.title, 'content': picture.content, 'image': picture.image})
            return render(request, 'update_post.html', {'form': form})
    else:
        messages.warning(request, "권한이 없습니다.")
        return redirect('gallery:detail', picture_id=picture_id)


def create_love(request, picture_id):
    picture = get_object_or_404(Picture, picture_id=picture_id)
    user = get_object_or_404(User, pk=request.user)
    love = Love.objects.filter(user_id=user, picture_id=picture)
    if love:
        love.delete()
    else:
        love = Love(user_id=user, picture_id=picture, created_at=timezone.now())
        love.save()
    return redirect('gallery:detail', picture_id=picture.picture_id)


def create_comment(request, picture_id):
    picture = get_object_or_404(Picture, pk=picture_id)
    user = get_object_or_404(User, pk=request.user)
    comment = Comment(user_id=user, picture_id=picture, content=request.POST.get('content'),
                      created_at=timezone.now())
    comment.save()
    return redirect('gallery:detail', picture_id=picture.picture_id)


def delete_comment(request, comment_id, picture_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.user_id:
        comment.delete()
        return redirect('gallery:detail', picture_id=picture_id)
    else:
        messages.warning(request, "권한이 없습니다.")
        return redirect('gallery:detail', picture_id=picture_id)


def update_comment(request, comment_id, picture_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.user_id:
        pass
    else:
        messages.warning(request, "권한이 없습니다.")
        return redirect('gallery:detail', picture_id=picture_id)


def new_register(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = Picture(
                title=form.cleaned_data['title'],
                image=form.cleaned_data['image'].read(),
                content=form.cleaned_data['content'],
                user_id=request.user
            )
            image_instance.save()
            return redirect('gallery:index')
    else:
        form = ImageUploadForm()
    return render(request, 'gallery/new_register.html', {'form': form})


def create(request):
    picture = Picture(
        title=request.POST.get('title'),
        image=request.POST.get('image'),
        content=request.POST.get('content'),
        created_at=request.POST.get('created_at'),
        user_id=request.user
    )
    picture.save()

    return redirect('gallery:index')


def search(request):
    q = Picture.objects.filter(title__contains=request.GET.get('search'))
    context = {'gallery_li': q}
    print(q)
    return render(request, 'gallery/gallery.html', context)
