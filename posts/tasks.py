from celery import shared_task
from .models import Story,StoryView
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model

@shared_task
def delete_expired_stories():
    """
    Deletes stories that were created more than 24 hours ago
    """
    expired_time = timedelta(hours=24)
    expired_stories = Story.objects.filter(created_at__lte=timezone.now() - expired_time)
    expired_stories.delete()

@shared_task
def create_story_view(story_id, user_id):    
    
    User = get_user_model()
    story = Story.objects.get(pk=story_id)
    user = User.objects.get(pk=user_id)
    
    StoryView.objects.get_or_create(story=story, viewer=user)