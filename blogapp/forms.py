from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    comment = forms.CharField(label='', widget=forms.Textarea(
        attrs={"rows": 5,
               "cols": 20,
               'class': "form-control",
               'placeholder': 'Type your comment'}))

    class Meta:
        model = Comment
        fields = ["comment", ]
