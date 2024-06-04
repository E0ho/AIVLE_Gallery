from django.db import models
from GalleryUser.models import User


class Picture(models.Model):
    picture_id = models.AutoField(primary_key=True, blank=False, null=False, db_column='picture_id',
                                  auto_created=True)
    title = models.CharField(max_length=200, db_column='title')
    image = models.BinaryField(db_column='image',  editable=True)
    content = models.TextField(db_column='content', default='0')
    created_at = models.DateTimeField(auto_now=True, db_column='created_at')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'picture'


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True, blank=False, null=False, auto_created=True,
                                  db_column='comment_id')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    picture_id = models.ForeignKey(Picture, on_delete=models.CASCADE, db_column='picture_id')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    content = models.TextField(db_column='content', default='0')

    class Meta:
        db_table = 'comment'


class Love(models.Model):
    love_id = models.AutoField(primary_key=True, db_column='love_id')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    picture_id = models.ForeignKey(Picture, on_delete=models.CASCADE, db_column='picture_id')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'love'
