from rest_framework import serializers, exceptions
# class Serialize
from base.serializers.serializers import BaseSerializer
from account.serializers import ProfileSerializer
from .models import Category, PhotoPost, VideoPost, Photos, Article, Comments, SubComments


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ['created_at']
        # fields = '__all__'


class MetaDataSerializer(serializers.Serializer):
    views = serializers.BooleanField(required=False, default=False)
    likes = serializers.BooleanField(required=False, default=False)
    dislikes = serializers.BooleanField(required=False, default=False)
    id_video = serializers.IntegerField(required=False)
    id_photo = serializers.IntegerField(required=False)
    id_article = serializers.IntegerField(required=False)
    id_comment = serializers.IntegerField(required=False)
    id_sub_comment = serializers.IntegerField(required=False)


class VideoPostSerialize(serializers.ModelSerializer):
    author = ProfileSerializer(required=False)
    category = CategorySerializer(required=False)
    category_id = serializers.IntegerField(required=False)

    def update(self, instance, validated_data):
        return BaseSerializer(self.context).update(instance, validated_data)

    def to_representation(self, instance):
        data = super(VideoPostSerialize, self).to_representation(instance)
        del data['category_id']
        return BaseSerializer(self.context).to_representation(data)

    def create(self, validated_data):
        return BaseSerializer(self.context).create(validated_data)

    class Meta:
        model = VideoPost
        fields = '__all__'


class PhotoPostSerialize(serializers.ModelSerializer):
    author = ProfileSerializer(required=False)
    category = CategorySerializer(required=False)
    category_id = serializers.IntegerField(required=False)

    def update(self, instance, validated_data):
        return BaseSerializer(self.context).update(instance, validated_data)

    def to_representation(self, instance):
        data = super(PhotoPostSerialize, self).to_representation(instance)
        # data.pop('category_id', None)
        del data['category_id']
        return BaseSerializer(self.context).to_representation(data)

    def create(self, validated_data):
        return BaseSerializer(self.context).create(validated_data)

    class Meta:
        model = PhotoPost
        # fields = ['author', 'category', 'category_id', 'title', 'description', 'photo', 'views', 'likes', 'dislikes', 'is_active', 'is_comment_status']
        fields = '__all__'


class ArticleSerialize(serializers.ModelSerializer):
    author = ProfileSerializer(required=False)
    category = CategorySerializer(required=False)
    category_id = serializers.IntegerField(required=False)
    # photo = PhotoPostSerialize(required=False)

    def update(self, instance, validated_data):
        return BaseSerializer(self.context).update(instance, validated_data)

    def to_representation(self, instance):
        data = super(ArticleSerialize, self).to_representation(instance)
        del data['category_id']
        return BaseSerializer(self.context).to_representation(data)

    def create(self, validated_data):
        return BaseSerializer(self.context).create(validated_data)

    class Meta:
        model = Article
        fields = '__all__'


class PhotosSerialize(serializers.ModelSerializer):
    article = ArticleSerialize(required=False)

    def update(self, instance, validated_data):
        return BaseSerializer(self.context).update(instance, validated_data)

    def to_representation(self, instance):
        data = super(PhotosSerialize, self).to_representation(instance)
        del data['article']
        return data
        # return BaseSerializer(self.context).to_representation(data)

    class Meta:
        model = Photos
        # fields = '__all__'
        exclude = ['article']


class SubCommentsSerialize(serializers.ModelSerializer):
    author = ProfileSerializer(required=False)
    comment_id = serializers.IntegerField(required=False)

    def update(self, instance, validated_data):
        return BaseSerializer(self.context).update(instance, validated_data)

    def to_representation(self, instance):
        data = super(SubCommentsSerialize, self).to_representation(instance)
        del data['comment_id']
        return BaseSerializer(self.context).to_representation(data)

    def create(self, validated_data):
        return BaseSerializer(self.context).create(validated_data)

    class Meta:
        model = SubComments
        fields = '__all__'


class CommentsSerialize(serializers.ModelSerializer):
    author = ProfileSerializer(required=False)
    comment_id = serializers.IntegerField(required=False)
    author_id = serializers.IntegerField(required=False)
    video_post_id = serializers.IntegerField(required=False)
    photo_post_id = serializers.IntegerField(required=False)
    article_post_id = serializers.IntegerField(required=False)

    def update(self, instance, validated_data):
        return BaseSerializer(self.context).update(instance, validated_data)

    def del_null_data(self, data):
        list_keys = ['photo_post', 'video_post', 'article_post']
        for key in list_keys:
            data.pop(key) if data.get(key, None) is None else None
        return data

    def to_representation(self, instance):
        data = super(CommentsSerialize, self).to_representation(instance)
        del data['author_id'], data['video_post_id'], data['photo_post_id'], data['article_post_id']
        data = self.del_null_data(data)
        #  is None else  data.pop('article_post') if data.pop('article_post') is None else None
        sub_comment = SubComments.objects.filter(comment=instance)
        if sub_comment.exists():
            data['sub_comment'] = SubCommentsSerialize(sub_comment, many=True).data
        return BaseSerializer(self.context).to_representation(data)

    def create(self, validated_data):
        dict_keys = {'video_post_id': VideoPost, 'photo_post_id': PhotoPost, 'article_post_id': Article}
        for key in dict_keys.keys():
            pk = validated_data.get(key, None)
            if pk is not None:
                obj = dict_keys.get(key).objects.get(pk=pk)
                if obj.is_active and obj.is_comment_status and obj.is_active_admin and obj.is_comment_status_admin:
                    return BaseSerializer(self.context).create(validated_data)
        raise exceptions.ValidationError("error comment_status false, not saved.", code=200)

    class Meta:
        model = Comments
        fields = '__all__'
