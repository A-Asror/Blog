from django.db import models
from account.models import User, UserProfile


class Category(models.Model):
    category = models.TextField(max_length=1000)
    created_at = models.DateField(auto_now_add=True)


class VideoPost(models.Model):
    author = models.ForeignKey(User, related_name='author_video', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=5000, blank=True, null=True)
    video = models.FileField(upload_to='video/%Y/%m/%d/')
    views = models.BigIntegerField(default=0, blank=True)
    likes = models.BigIntegerField(default=0, blank=True)
    dislikes = models.BigIntegerField(default=0, blank=True)
    plays_count = models.IntegerField(default=0, blank=True)
    category = models.ForeignKey(Category, related_name='category_video', on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    is_comment_status = models.BooleanField(default=True)
    is_active_admin = models.BooleanField(default=True)
    is_comment_status_admin = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PhotoPost(models.Model):
    author = models.ForeignKey(User, related_name='author_photo', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=5000, blank=True, null=True)
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True, null=True)
    views = models.BigIntegerField(default=0, blank=True)
    likes = models.BigIntegerField(default=0, blank=True)
    dislikes = models.BigIntegerField(default=0, blank=True)
    category = models.ForeignKey(Category, related_name='category_photo', on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    is_comment_status = models.BooleanField(default=True)
    is_active_admin = models.BooleanField(default=True)
    is_comment_status_admin = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Photos(models.Model):
    article = models.ForeignKey('Article', related_name='article_photo', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='post_photos/%Y/%m/%d/')


# class Videos(models.Model):
#     video = models.FileField(upload_to='post_photos/%Y/%m/%d/')


class Article(models.Model):
    author = models.ForeignKey(User, related_name='article', on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, related_name='category_article', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=500)
    article = models.TextField(max_length=5000)
    video = models.FileField(upload_to='article_videos/%Y/%m/%d/')
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    plays_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_comment_status = models.BooleanField(default=True)
    is_active_admin = models.BooleanField(default=True)
    is_comment_status_admin = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}, {self.title}'


class Comments(models.Model):
    video_post = models.ForeignKey(VideoPost, related_name='video_post', on_delete=models.CASCADE, blank=True, null=True)
    photo_post = models.ForeignKey(PhotoPost, related_name='photo_post', on_delete=models.CASCADE, blank=True, null=True)
    article_post = models.ForeignKey(Article, related_name='article_post', on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(User, related_name='author_comment', on_delete=models.CASCADE)
    content = models.TextField(max_length=2500)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    # date_posted = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)


class SubComments(models.Model):
    comment = models.ForeignKey(Comments, related_name='sub_comment', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='author_sub_comment', on_delete=models.CASCADE)
    content = models.TextField(max_length=2500)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    # date_posted = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
