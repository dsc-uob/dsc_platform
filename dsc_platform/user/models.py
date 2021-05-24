from django.db import models
from django.contrib.auth.models import BaseUserManager, \
    PermissionsMixin, AbstractBaseUser
from . import utils


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


# The genders of members
genders = (
    ('F', 'Female'),
    ('M', 'Male')
)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(
        max_length=15, null=True, blank=True, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=genders)

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'email', 'gender']
    objects = UserManager()
