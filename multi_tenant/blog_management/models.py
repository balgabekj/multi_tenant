from django.db import models
from users.models import CustomUser

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')  # User sending the message
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')  # User receiving the message
    content = models.TextField()  # The body of the message
    timestamp = models.DateTimeField(auto_now_add=True)  # When the message was sent
    is_read = models.BooleanField(default=False)  # To mark whether the message has been read by the recipient

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username} at {self.timestamp}"

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')  # The user who receives the notification
    message = models.CharField(max_length=255)  # Short message describing the notification
    is_read = models.BooleanField(default=False)  # Marks if the notification has been read
    timestamp = models.DateTimeField(auto_now_add=True)  # When the notification was created

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message}"

class BlogPost(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blog_posts')  # Admin or renter who writes the post
    title = models.CharField(max_length=255)  # Title of the blog post
    content = models.TextField()  # The body/content of the blog post
    created_at = models.DateTimeField(auto_now_add=True)  # When the blog post was created
    updated_at = models.DateTimeField(auto_now=True)  # When the blog post was last updated
    is_published = models.BooleanField(default=False)  # Whether the post is published or not

    def __str__(self):
        return f"Blog Post: {self.title} by {self.author.username}"

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')  # The blog post being commented on
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')  # User who made the comment
    content = models.TextField()  # The content of the comment
    timestamp = models.DateTimeField(auto_now_add=True)  # When the comment was posted

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"


