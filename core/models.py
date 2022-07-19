from lib2to3.pytree import Base
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext as _

# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        It creates a user, sets the password, and saves the user to the database

        :param email: The email address of the user
        :param password: The password to use for this user
        :return: A user object.
        """
        if not email:
            raise ValueError(_("User must have an email address"))

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        It creates a user, sets the is_staff and is_superuser attributes to True, and saves the user
        
        :param email: This is the only required field for creating a user and it must be unique
        :param password: The password to use for this user
        :return: The user object.
        """
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
