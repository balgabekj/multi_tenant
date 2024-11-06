from django.db import models
from users.models import CustomUser

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages') 
    content = models.TextField()  
    timestamp = models.DateTimeField(auto_now_add=True)  
    is_read = models.BooleanField(default=False)  

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username} at {self.timestamp}"

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications') 
    message = models.CharField(max_length=255)  
    is_read = models.BooleanField(default=False) 
    timestamp = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message}"

class BlogPost(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blog_posts') 
    content = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 
    is_published = models.BooleanField(default=False)  

    def __str__(self):
        return f"Blog Post: {self.title} by {self.author.username}"

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')  
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments') 
    content = models.TextField()  
    timestamp = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"


