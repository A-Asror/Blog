from rest_framework import serializers

from base.serializers.serializers import BaseSerializer
from .models import User, UserProfile, University, Faculty, Friends, Education


class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=128, min_length=8, write_only=True)
    password2 = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['password1', 'password2', 'username', 'email', 'last_name', 'first_name']

    def create(self, validated_data):
        password = validated_data.pop('password')
        return User.objects.create_user(password=password, **validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, min_length=8)


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    last_name = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    # dob = serializers.DateField(required=False)
    # gender = serializers.CharField(required=False)
    # photo = serializers.ImageField(required=False)
    # permission = serializers.IntegerField(required=False)
    # phone = serializers.CharField(required=False)
    # about = serializers.CharField(required=False)
    # age = serializers.IntegerField(required=False)
    # links = serializers.JSONField(required=False)
    old_password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=False)
    password1 = serializers.CharField(max_length=128, min_length=8, write_only=True, required=False)
    password2 = serializers.CharField(max_length=128, min_length=8, write_only=True, required=False)

    def update(self, instance, validated_data):
        return BaseSerializer(self.context).update(instance, validated_data)

    def to_representation(self, instance):
        data = super(ProfileSerializer, self).to_representation(instance)
        if self.context.get('sub_class', True):
            data = {'id': instance.pk, 'photo': f'http://localhost:8000{instance.profile.photo.url}', 'username': instance.username}
            return data
        # data['id'] = instance.user.pk
        # print(instance.user.education.university)
        try:
            data['university'] = instance.user.education.university.university
            data['faculty'] = instance.user.education.faculty.faculty
            data['username'] = instance.user.username
            data['email'] = instance.user.email
            data['first_name'] = instance.user.email
            data['last_name'] = instance.user.last_name
            data['followers'] = instance.user.friends.followers.count()
            data['following'] = instance.user.friends.following.count()
        except  Exception:
            data['university'] = instance.user.education.university
            data['faculty'] = instance.user.education.faculty
        return BaseSerializer(self.context).to_representation(data)

    class Meta:
        model = UserProfile
        exclude = ['user']
    #     # fields = '__all__'


class UniversitySerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        return BaseSerializer(self.context).update(instance, validated_data)

    class Meta:
        model = University
        fields = '__all__'


class FacultySerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        return BaseSerializer(self.context).update(instance, validated_data)

    class Meta:
        model = Faculty
        fields = '__all__'


class IDFriendsSerializer(serializers.Serializer):
    follow = serializers.IntegerField(required=False)
    unfollow = serializers.IntegerField(required=False)
    remove = serializers.IntegerField(required=False)


class FriendsSerializer(serializers.ModelSerializer):
    followers = ProfileSerializer(required=False, many=True)
    following = ProfileSerializer(required=False, many=True)

    def update(self, instance, validated_data):
        return BaseSerializer(self.context).update(instance, validated_data)

    def to_representation(self, instance):
        data = super(FriendsSerializer, self).to_representation(instance)
        return data

    class Meta:
        model = Friends
        fields = '__all__'


class EducationSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        return BaseSerializer(self.context).update(instance, validated_data)

    class Meta:
        model = Education
        fields = '__all__'


# class UserSerializer(BaseSerializer, serializers.ModelSerializer):
#     password = serializers.CharField(
#         max_length=128,
#         min_length=8,
#         write_only=True)
#
#     class Meta:
#         model = User
#         fields = ('email', 'username', 'age', 'photo', 'gender', 'university', 'faculty', 'password')
#
#     def update(self, instance, validated_data):
#         password = validated_data.pop('password', None)
#         for key, value in validated_data.items():
#             print(key, value)
#             setattr(instance, key, value)
#         if password is not None:
#             instance.set_password(password)
#         instance.save()
#
#         return instance
#
#
# class UpdateSerializer(BaseSerializer, serializers.Serializer):
#     username = serializers.CharField(required=False)
#     faculty = serializers.CharField(required=False)
#     age = serializers.IntegerField(required=False)
#     # photo = serializers.ImageField(required=False)
#     gender = serializers.CharField(required=True)
#     university = serializers.CharField(required=True)
#
#     # class Meta:
#     #     model = User
#     #     fields = ['username', 'faculty', 'age', 'photo', 'gender', 'university']
#
#     def update(self, instance, validated_data):
#         print(instance)
#         for key, value in validated_data.items():
#             print(key, value)
#             setattr(instance, key, value)
#         instance.save()
#         return instance
#
# class UserProfileSerializer(BaseSerializer, serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#
#     def update(self, instance, validated_data):
#         for key, value in validated_data.items():
#             setattr(instance, key, value)
#         instance.save()
#         return instance
#
#     class Meta:
#         model = UserProfile
#         # fields = '__all__'
#         # exclude = ['password']
#         fields = ['user', 'followers', 'following']
#
#
# class RefreshSerializer(BaseSerializer, serializers.Serializer):
#     access = serializers.CharField()
#     refresh = serializers.CharField()
#
#
# class AllUserSerializers(BaseSerializer, serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'
#
#
# class FallowerSerializer(BaseSerializer, serializers.Serializer):
#     favorite_id = serializers.IntegerField()
