from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import BlogPost, Comment, Message, Notification
from .forms import BlogPostForm, BlogPostCreateForm, BlogPostUpdateForm, CommentForm, MessageForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from users.models import CustomUser

# BlogPost views

def blogpost_list(request):
    blog_posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'blogpost_list.html', {'blog_posts': blog_posts})


def blogpost_detail(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)
    comments = blog_post.comments.all()  # Получаем все комментарии для поста

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blog_post = blog_post
            comment.user = request.user
            comment.save()

            Notification.objects.create(
                user=blog_post.author,
                message=f"New comment on your post '{blog_post.title}' by {request.user.username}",
            )

            return redirect('blogpost_detail', pk=pk)
    else:
        comment_form = CommentForm()

    return render(request, 'blogpost_detail.html', {
        'blog_post': blog_post,
        'comments': comments,
        'comment_form': comment_form,
    })

@login_required
def blogpost_create(request):
    if request.method == 'POST':
        form = BlogPostCreateForm(request.POST)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('blogpost_detail', pk=blog_post.pk)
    else:
        form = BlogPostCreateForm()
    return render(request, 'blogpost_form.html', {'form': form})

@login_required
def blogpost_update(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)
    if blog_post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == 'POST':
        form = BlogPostUpdateForm(request.POST, instance=blog_post)
        if form.is_valid():
            form.save()
            return redirect('blogpost_detail', pk=blog_post.pk)
    else:
        form = BlogPostUpdateForm(instance=blog_post)
    return render(request, 'blogpost_form.html', {'form': form})

@login_required
def blogpost_delete(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)
    if blog_post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")
    
    if request.method == 'POST':
        blog_post.delete()
        return redirect('blogpost_list')
    return render(request, 'blogpost_confirm_delete.html', {'blog_post': blog_post})


@login_required
def toggle_publish_status(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)
    if blog_post.author != request.user:
        return HttpResponseForbidden("You are not allowed to publish/unpublish this post.")

    blog_post.is_published = not blog_post.is_published
    blog_post.save()
    return redirect('blogpost_detail', pk=pk)

# Message views
@login_required
def inbox(request):
        received_messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
        return render(request, 'inbox.html', {'received_messages': received_messages})

@login_required
def sent_messages(request):
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'sent_messages.html', {'sent_messages': sent_messages})

@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if message.sender != request.user and message.recipient != request.user:
        return redirect('inbox')

    if request.user == message.recipient and not message.is_read:
        message.is_read = True
        message.save()

    return render(request, 'message_detail.html', {'message': message})


@login_required
def send_message(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()

            Notification.objects.create(
                user=message.recipient,
                message=f"You have received a new message from {request.user.username}",
            )
                
            return redirect('sent_messages')
    else:
        form = MessageForm()

    return render(request, 'send_message.html', {'form': form})


# Notification views

@login_required
def notification_list(request):
    notifications = request.user.notifications.all().order_by('-timestamp')
    return render(request, 'notification_list.html', {'notifications': notifications})

@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notification_list')

@login_required
def mark_all_as_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect('notification_list')

@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.delete()
    return redirect('notification_list')


