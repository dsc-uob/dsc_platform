from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, \
    PermissionsMixin

from core import utils


class UserManager(BaseUserManager):
    """Manage user model"""

    def create_user(self, email, username, password, **extra_fields):
        """Creating and returning a new user."""
        if not email:
            raise ValueError('No email address.')
        if not username or utils.not_valid_username(username):
            raise ValueError('No valid username.')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password, **extra_fields):
        """Creating and returning superuser."""
        user = self.create_user(email, username, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        user.save(using=self._db)
        return user

    def create_staff_user(self, email, username, password, **extra_fields):
        """Creating and returning staff user."""
        user = self.create_user(email, username, password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User model class."""
    STAGES = (
        (-1, 'Illiterate'),
        (0, 'Graduate'),
        (1, 'First'),
        (2, 'Second'),
        (3, 'Third'),
        (4, 'Forth'),
        (5, 'Fifth'),
        (6, 'Sixth'),
    )
    GENDERS = [
        (0, 'Male'),
        (1, 'Female'),
    ]

    # Personal Information
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True)
    gender = models.IntegerField(choices=GENDERS, null=True)
    stage = models.IntegerField(choices=STAGES, null=True)
    bio = models.TextField(null=True)
    photo = models.ImageField(null=True, upload_to=utils.user_image_file_path)

    # Contact Information
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)

    # Important Information
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', ]

    def __str__(self):
        return f"{self.username} ({self.email})"


class Post(models.Model):
    """The model class of post."""
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}: {self.title}"


class Comment(models.Model):
    """The model class of comments."""
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}: {self.body}"


class Image(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
    )
    image = models.ImageField(upload_to=utils.upload_image_file_path)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.image.path}"
