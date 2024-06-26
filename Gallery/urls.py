from django.urls import path
from Gallery import views


app_name = 'gallery'


urlpatterns = [

    # 기본 URL
    path('', views.picture_list, name='list'),                         # 메인 페이지
    path('<int:picture_id>/', views.picture_detail, name='detail'),    # 상세 페이지

    # Comment 관련 URL
    path('<int:picture_id>/create_comment/', views.create_comment, name='create_comment'),                     # 댓글 생성
    path('/<int:picture_id>/<int:comment_id>/delete_comment/', views.delete_comment, name='delete_comment'),   # 댓글 삭제

    # Love 관련 URL
    path('<int:picture_id>/create_love/', views.create_love, name='create_love'),     # 좋아요 (추가 <-> 제거)


###########################################################################################################################

    # Picture 관련 URL
    path('<int:picture_id>/update_picture/', views.update_picture, name='update'),
    path('<int:picture_id>/delete_picture/', views.delete_picture, name='delete'),


    path('new_register/', views.new_register, name='new_register'),
    path('create/', views.create, name='create'),
    path('search/', views.search, name='search'),
]


# Media 폴더 저장 경로 설정
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)