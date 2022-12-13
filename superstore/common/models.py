from django.db import models
from django.contrib.auth import get_user_model

from superstore.photos.models import Toy

UserModel = get_user_model()


class Comment(models.Model):
    MAX_TEXT_LEN = 300

    text = models.TextField(max_length=MAX_TEXT_LEN, null=False, blank=False)
    publication_date_and_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    to_toy = models.ForeignKey(Toy, on_delete=models.CASCADE, null=False, blank=True)
    user = models.ForeignKey(UserModel, on_delete=models.RESTRICT,)

    class Meta:
        ordering = ["-publication_date_and_time"]

    def __str__(self):
        return self.text


class Like(models.Model):
    to_toy = models.ForeignKey(Toy, on_delete=models.CASCADE, null=False, blank=True)
    user = models.ForeignKey(UserModel, on_delete=models.RESTRICT,)
