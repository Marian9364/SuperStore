from django import forms

from superstore.common.models import Comment


class ToyCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'cols': 40,
                    'rows': 10,
                    'placeholder': 'Add comment...'
                },
            ),
        }


class SearchForm(forms.Form):
    toy_name = forms.CharField(
        max_length=40,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search by a toy name...'
            }
        )
    )