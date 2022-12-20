import os

from django import forms

from superstore.common.models import Like, Comment
from superstore.photos.models import Toy
from superstore.core.form_mixins import DisabledFormMixin


class PhotoBaseForm(forms.ModelForm):
    class Meta:
        model = Toy
        exclude = ('toy_publication_date', 'slug', 'user')


class ToyCreateForm(PhotoBaseForm):
    pass


class ToyEditForm(PhotoBaseForm):
    pass


class ToyDeleteForm(DisabledFormMixin, PhotoBaseForm):
    disabled_fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        if commit:
            image_path = self.instance.toy_photo.path
            Like.objects.filter(to_toy_id=self.instance.id) \
                .delete()
            Comment.objects.filter(to_toy_id=self.instance.id) \
                .delete()
            self.instance.delete()
            os.remove(image_path)

        return self.instance

    class Meta:
        model = Toy
        fields = ()
