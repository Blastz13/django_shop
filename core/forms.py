from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['email', 'name', 'text']

        widgets = {
            "email": forms.EmailInput(),
            "name": forms.TextInput(),
            "text": forms.Textarea(attrs={"id":"message", "cols":"40", "rows":"10"})
        }