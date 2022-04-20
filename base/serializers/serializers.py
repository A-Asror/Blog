from rest_framework import serializers
from rest_framework import exceptions


class BaseSerializer:
    validated_data = None
    instance = None
    # many_data = None
    # foreign_data = None
    # add = False
    # remove = False

    def __init__(self, context):
        self.context = context
        self.request = self.context.get('request', None)
        self.many_data = self.context.get('many', False)
        self.foreign_data = self.context.get('foreign', False)

    def update(self, instance, validated_data):
        self.validated_data = validated_data
        self.instance = instance
        if self.many_data:
            return self.update_many_field()
        if self.foreign_data:
            self.update_foreign_key_field()
        if 'password' in validated_data:
            self.update_password()
        if not self.many_data:
            return self.__update()

    def posts(self, obj):
        if obj.__class__.__name__ in ['VideoPost', 'PhotoPost', 'Article']:
            if self.request.user.profile.permission >= 3:
                self.validated_data.pop('is_comment_status_admin', False)
                self.validated_data.pop('is_active_admin', False)

    def __update(self):
        instances = self.context.get('instance', False)
        self.posts(self.instance)
        for key, value in self.validated_data.items():
            if hasattr(self.instance, key):
                setattr(self.instance, key, value)
            elif instances:
                for meta_instance in instances:
                    self.posts(meta_instance)
                    if hasattr(meta_instance, key):
                        setattr(meta_instance, key, value)
        self.instance.save()
        [meta_instance.save() for meta_instance in instances] if instances else None
        return self.instance

    def update_password(self):
        self.request.user.set_password(self.validated_data['password'])
        self.request.user.save()

    def update_many_field(self):
        list_follow = ['follower', 'follow']
        list_unfollow_or_remove = ['unfollow', 'follower', 'remove', 'unfollow']
        # list_remove = ['remove', 'unfollow']
        key1 = self.many_data['key1']
        key2 = self.many_data['key2']
        list_keys = [key1, key2]
        if key1['follow_or_unfollow'] in list_follow and key2['follow_or_unfollow'] in list_follow:
            for creating in list_keys:
                creating['cast_or_fast'].add(creating['user'])
            [creating['cast_or_fast'].add(creating['user']) for creating in list_keys]
        elif key1['follow_or_unfollow'] in list_unfollow_or_remove and key2['follow_or_unfollow'] in list_unfollow_or_remove:
            [removing['cast_or_fast'].remove(removing['user']) for removing in list_keys]
        return key1['user']
        # [removing['cast_or_fast'].remove(removing['user']) for removing in list_keys] if self.remove else [creating['cast_or_fast'].add(creating['user']) for creating in list_keys] if self.add else None
        # elif key1['follow_or_unfollow'] in list_remove and key2['follow_or_unfollow'] in list_remove:
        #     [removing['cast_or_fast'].remove(removing['user']) for removing in list_keys]
        # model = list_data[0]
        # field_set = list_data[1]
        # str_field = list_data[2]
        # for key, value in self.many_data.items():
        # if list_pk_data:
        #     for pk_data in list_pk_data:
        #         filter_data = list_data[0].objects.filter(pk=pk_data.pk)
        #         if filter_data.exists():
        #             field_set = list_data[1]
        #             filter_data_get = filter_data.get()
        #             stock_check = field_set.filter(pk=filter_data_get.pk)
        #             print(stock_check)
        #             field_set.remove(filter_data_get) if stock_check.exists() else field_set.add(filter_data_get)

    def update_foreign_key_field(self):
        for list_field in self.foreign_data:
            field = list_field[3]
            pk = self.validated_data.pop(field, False)
            if pk:
                model = list_field[0]
                data = model.objects.filter(pk=self.validated_data.get('id', None))
                if data.exists():
                    data = data.get()
                    model.objects.filter(**list_field[1]).update(**{field: data})

    def to_representation(self, data):
        return data

    def post_created(self, validated_data, obj):
        # keys = ['is_active', 'is_comment_status', 'is_active_admin', 'is_comment_status_admin']
        if obj.__name__ in ['VideoPost', 'PhotoPost', 'Article']:
            for key in ['is_active', 'is_comment_status', 'is_active_admin', 'is_comment_status_admin']:
                validated_data[key] = True

    def create(self, validated_data):
        model = self.context.get('create', False)
        author = self.context.get('author', False)
        key = self.context.get('key', None)
        self.post_created(validated_data, model)

        if model and author and key is not None and self.request:
            validated_data['author_id'] = author
            validated_data[key] = self.request.content_data
            return model.objects.create(**validated_data)
        elif model and author:
            if validated_data.get('article_post_id', False) or validated_data.get('article_post_id', False) or validated_data.get('video_post_id', False) or validated_data.get('comment_id', False):
                validated_data['author_id'] = author
                return model.objects.create(**validated_data)
        raise exceptions.ValidationError(detail='not all data is present')
