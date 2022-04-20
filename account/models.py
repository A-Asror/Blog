from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if email is None:
            raise TypeError("Users must have a email.")

        if password is None:
            raise TypeError("Both password fields must be filled")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


Gender = [
    ('Male', 'Male'),
    ('Female', 'Female')
]


Permissions = (
    (0, _("SuperAdmin")),
    (1, _("Admin")),
    (2, _("Manager")),
    (3, _("User")),
)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return f'ID: {self.pk}, username: {self.username}'


class University(models.Model):
    university = models.TextField(max_length=1000)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'ID: {self.pk}, username: {self.university}'


class Faculty(models.Model):
    faculty = models.TextField(max_length=1000)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'ID: {self.pk}, username: {self.faculty}'


class Friends(models.Model):
    user = models.OneToOneField(User, related_name="friends", on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='cast', blank=True)
    following = models.ManyToManyField(User, related_name='fast', blank=True)

    def __str__(self):
        return f'ID: {self.pk}, username: {self.user.username}'


class Education(models.Model):
    user = models.OneToOneField(User, related_name="education", on_delete=models.CASCADE)
    university = models.ForeignKey(University, related_name='univer', on_delete=models.SET_NULL, null=True)
    faculty = models.ForeignKey(Faculty, related_name='facultet', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'ID: {self.pk}, username: {self.user.username}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=Gender, max_length=10, blank=True, null=True)
    photo = models.ImageField(upload_to='profiles/%Y/%m/%d/', blank=True, null=True)
    permission = models.IntegerField(choices=Permissions, default=3)
    phone = models.CharField(max_length=40, null=True, blank=True, unique=True)
    about = models.TextField(max_length=7000, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    links = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f'ID: {self.pk}, username: {self.user.username}'


class Jwt(models.Model):
    user = models.OneToOneField(User, related_name="jwt", on_delete=models.CASCADE)
    access = models.TextField()
    refresh = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'ID: {self.pk}, username: {self.user.username}'
