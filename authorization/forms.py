from django import forms
from .models import (
    Post,
    Review,
)


class ChangeGroupForm(forms.Form):
    GROUPS = (
        ('CE', 'Content Editor'),
        ('ME', 'Meta Editor'),
        ('PC', 'Post Creator'),
        ('RC', 'Review Creator'),
        ('SU', 'Special User')
    )
    group = forms.ChoiceField(
        choices=GROUPS,
        label= 'Groups',
        widget= forms.widgets.RadioSelect
    )


class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
         'title', 'content', 'author'
        ]