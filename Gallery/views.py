import base64

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages

from Gallery.models import Picture, Comment, Love
from GalleryUser.models import User
from .forms import *


# 메인 페이지 (홈 - 갤러리 리스트)
def picture_list(request):

    # 모든 갤러리 리스트 가져오기
    picture_list = Picture.objects.all()

    context = {
        'picture_list': picture_list
        }

    # 홈 갤러리 (사진 게시글 리스트) 페이지 이동
    return render(request, 'gallery/gallery.html', context)


# 상세 페이지
def picture_detail(request, picture_id):

    # 특정 사진 정보 가져오기
    picture = get_object_or_404(Picture, picture_id=picture_id)
    image_data = base64.b64encode(picture.image).decode()

    context = {
        'picture': picture,
        'img': image_data
        }

    # 사진 게시글 상세 페이지 이동
    return render(request, "gallery/detail.html", context)


# 댓글 생성
def create_comment(request, picture_id):

    # 사진, 유저 정보 가져오기
    picture = get_object_or_404(Picture, pk=picture_id)
    user = get_object_or_404(User, pk=request.user)

    # 댓글 생성
    comment = Comment(user_id=user,
                      picture_id=picture,
                      content=request.POST.get('content'),
                      created_at=timezone.now())
    comment.save()

    # 해당 사진 게시글로 이동
    return redirect('gallery:detail', picture_id=picture.picture_id)


# 댓글 수정
def update_comment(request, picture_id, comment_id):

    # 사진, 댓글 정보 가져오기
    comment = get_object_or_404(Comment, pk=comment_id)
    picture = get_object_or_404(Picture, picture_id=picture_id)
    image_data = base64.b64encode(picture.image).decode()

    # 댓글 작성 유저가 현재 로그인한 유저인지 체크
    if request.user == comment.user_id:
        if request.method == 'POST':

            # 수정한 댓글 저장
            comment.content = request.POST.get('content')
            comment.save()
            return redirect('gallery:detail', picture_id=picture_id)

        else:

            # 댓글 불러오기
            context = {'picture': picture,
                       'img': image_data,
                       'comment': comment}
            return render(request, "gallery/update_comment.html", context)


# 댓글 삭제
def delete_comment(request, picture_id, comment_id):

    # 댓글 정보 가져오기
    comment = get_object_or_404(Comment, pk=comment_id)

    # 유저 아이디 일치 확인 후 댓글 삭제
    if request.user == comment.user_id:
        comment.delete()
        return redirect('gallery:detail', picture_id=picture_id)

    # 유저 아이디 불일치 (거절)
    else:
        messages.warning(request, "권한이 없습니다.")
        return redirect('gallery:detail', picture_id=picture_id)


# 사진 등록
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
            return redirect('gallery:list')
    else:
        form = ImageUploadForm()
    return render(request, 'gallery/new_register.html', {'form': form})


# 사진 수정
def update_picture(request, picture_id):

    # 해당 사진 불러오기
    picture = get_object_or_404(Picture, pk=picture_id)
    image = picture.image  # 이미지 정보

    # 유저 일치 확인
    if request.user == picture.user_id:

        # 데이터 전송 (POST 방식)
        if request.method == 'POST':
            form = ImageUploadForm(request.POST, request.FILES)

            # 이미지 수정이 있는 경우
            if form.is_valid():
                picture.title = form.cleaned_data['title']
                picture.image = form.cleaned_data['image'].read()
                picture.content = form.cleaned_data['content']
                picture.user_id = request.user
                picture.save()
                return redirect('gallery:detail', picture_id=picture_id)

            # 이미지 수정이 없는 경우
            else:
                picture.title = form.cleaned_data['title']
                picture.image = image
                picture.content = form.cleaned_data['content']
                picture.user_id = request.user
                picture.save()
                return redirect('gallery:detail', picture_id=picture_id)

        # URL 접근 (GET 방식)
        else:
            form = ImageUploadForm(
                initial={'title': picture.title, 'content': picture.content, 'image': picture.image})
            return render(request, 'update_post.html', {'form': form})

    # 유저 불일치
    else:
        messages.warning(request, "권한이 없습니다.")
        return redirect('gallery:detail', picture_id=picture_id)


# 사진 삭제
def delete_picture(request, picture_id):
    picture = get_object_or_404(Picture, picture_id=picture_id)
    if request.user == picture.user_id:
        picture.delete()
        return redirect('gallery:list')
    else:
        messages.warning(request, "권한이 없습니다.")
        return redirect('gallery:detail', picture_id=picture_id)


# 좋아요 추가 기능
def create_love(request, picture_id):

    # 사진, 유저 정보 가져오기
    picture = get_object_or_404(Picture, picture_id=picture_id)
    user = get_object_or_404(User, pk=request.user)

    # 해당 사진에 유저가 누른 좋아요 정보 가져오기
    love = Love.objects.filter(user_id=user, picture_id=picture)

    # 좋아요 있음 (-> 삭제)
    if love:
        love.delete()

    # 좋아요 없음 (-> 생성)
    else:
        love = Love(
            user_id=user,
            picture_id=picture,
            created_at=timezone.now()
            )
        love.save()

    # 상세 페이지로 이동
    return redirect('gallery:detail', picture_id=picture.picture_id)


# 게시글 검색
def search(request):
    q = Picture.objects.filter(title__contains=request.GET.get('search'))
    context = {'picture_list': q}
    print(q)
    return render(request, 'gallery/gallery.html', context)
