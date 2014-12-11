from django import forms
from django.contrib.admin import widgets        
from django.contrib.comments.forms import CommentForm                            
from models import MPTTComment

class MPTTCommentForm(CommentForm):
    parent = forms.ModelChoiceField(queryset=MPTTComment.objects.all(), required=False, widget=forms.HiddenInput)
    is_anonymous = forms.BooleanField(required=False, label="Hide commenter's name")

    def get_comment_model(self):
        # Use our custom comment model instead of the built-in one.
        return MPTTComment

    def get_comment_create_data(self):
        # Use the data of the superclass, and add in the parent field field
        data = super(MPTTCommentForm, self).get_comment_create_data()
        data['parent'] = self.cleaned_data['parent']
        data['is_anonymous'] = self.cleaned_data['is_anonymous']
        return data
