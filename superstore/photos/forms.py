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
            Like.objects.filter(to_toy_id=self.instance.id) \
                .delete()  # one-to-many
            Comment.objects.filter(to_toy_id=self.instance.id) \
                .delete()  # one-to-many
            self.instance.delete()

        return self.instance
