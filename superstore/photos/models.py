from django.db import models
from django.template.defaultfilters import slugify
from django.core.validators import MinLengthValidator
from django.contrib.auth import get_user_model

from superstore.photos.validators import validate_file_size

UserModel = get_user_model()


class Toy(models.Model):
    MAX_NAME_LEN = 30
    MIN_DESCRIPTION_LEN = 10
    MAX_DESCRIPTION_LEN = 150

    toy_name = models.CharField(
        max_length=MAX_NAME_LEN,
        null=False,
        blank=False,
    )

    toy_photo = models.ImageField(upload_to='images', validators=(validate_file_size,))

    toy_description = models.TextField(
        max_length=MAX_DESCRIPTION_LEN,
        validators=(
            MinLengthValidator(MIN_DESCRIPTION_LEN),
        ),
    )

    toy_age_restriction = models.PositiveIntegerField()

    toy_price = models.FloatField()

    toy_publication_date = models.DateField(auto_now=True)

    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True,
        editable=True,
    )

    user = models.ForeignKey(UserModel, on_delete=models.RESTRICT,)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f"{self.toy_name}---{self.id}")
            return super().save(*args, **kwargs)

    def __str__(self):
        return self.toy_name






