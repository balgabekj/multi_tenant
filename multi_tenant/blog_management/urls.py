from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogpost_list, name='blogpost_list'),
    path('<int:pk>/', views.blogpost_detail, name='blogpost_detail'),
    path('new/', views.blogpost_create, name='blogpost_create'),
    path('<int:pk>/edit/', views.blogpost_update, name='blogpost_update'),
    path('<int:pk>/delete/', views.blogpost_delete, name='blogpost_delete'),
    path('<int:pk>/toggle_publish/', views.toggle_publish_status, name='toggle_publish'),
    path('inbox/', views.inbox, name='inbox'),
    path('sent/', views.sent_messages, name='sent_messages'),
    path('message/<int:pk>/', views.message_detail, name='message_detail'),
    path('send/', views.send_message, name='send_message'),
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/mark-as-read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('notifications/mark-all-as-read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('notifications/delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('analytics/', views.analytics_view, name='analytics'),

]
