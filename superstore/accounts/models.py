from enum import Enum

from django.db import models
from django.contrib.auth import models as auth_models
from django.core import validators

# Create your models here.
from superstore.core.validators import validate_only_letters


class ChoicesEnumMixin:
    @classmethod
    def choices(cls):
        return [(x.name, x.value) for x in cls]

    @classmethod
    def max_len(cls):
        return max(len(name) for name, _ in cls.choices())


class Gender(ChoicesEnumMixin, Enum):
    male = 'Male'
    female = 'Female'
    diverse = 'Diverse'


class AppUser(auth_models.AbstractUser):
    MIN_LEN_FIRST_NAME = 2
    MAX_LEN_FIRST_NAME = 30
    MIN_LEN_LAST_NAME = 2
    MAX_LEN_LAST_NAME = 30

    first_name = models.CharField(
        max_length=MAX_LEN_FIRST_NAME,
        blank=True,
        validators=(
            validators.MinLengthValidator(MIN_LEN_FIRST_NAME),
            validate_only_letters,
        )
    )

    last_name = models.CharField(
        max_length=MAX_LEN_LAST_NAME,
        blank=True,
        validators=(
            validators.MinLengthValidator(MIN_LEN_LAST_NAME),
            validate_only_letters,

        )
    )

    email = models.EmailField(unique=True,)

    profile_picture = models.URLField(
        blank=True,
    )

    gender = models.CharField(
        choices=Gender.choices(),
        max_length=Gender.max_len(),
        blank=True,
    )

    phone_number = models.IntegerField(
        blank=True,
    )

