from django import forms
from .models import BlogPost, Comment, Message

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['content', 'is_published']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your blog post content here...'}),
        }
        labels = {
            'content': 'Content',
            'is_published': 'Publish',
        }


class BlogPostCreateForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title','content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter post title'}),
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your blog post content here...'}),
        }
        labels = {
            'title': 'title',
            'content': 'Content',
        }

class BlogPostUpdateForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['content', 'is_published']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Update your blog post content here...'}),
        }
        labels = {
            'content': 'Content',
            'is_published': 'Publish',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment...'}),
        }
        labels = {
            'content': 'Comment',
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'content']
