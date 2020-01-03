from django.forms import ModelForm
from django.db import transaction
from .models import Comment

class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

    @transaction.atomic
    def save(self, _author, _submission):
        comment = super().save(commit=False)
        comment.author = _author
        comment.submission = _submission
        comment.save()
        return comment