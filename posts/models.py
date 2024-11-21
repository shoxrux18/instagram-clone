from django.conf import settings
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        related_query_name="post",
    )
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/")
    content = models.TextField()
    is_public = models.BooleanField(default=False)
    show_likes = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    comment = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="replies",
        related_query_name="reply",
        null=True,
        blank=True
    )
    text = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        related_query_name="comment",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        related_query_name="comment",
    )
    like_number = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.post.title}"
    

class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes",
        related_query_name="like",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes",
        related_query_name="like",
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "post"], name="unique_like")
        ]

    def __str__(self):
        return f"{self.user.email} - {self.post.title}"


class CommentLike(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comment_likes",
        related_query_name="comment_like",
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="comment_likes",
        related_query_name="comment_like",
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "comment"], name="unique_comment_like")
        ]

    def __str__(self):
        return f"{self.user.email} - {self.comment.text}"
    

class Story(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stories",
        related_query_name="story",
    )    
    image = models.ImageField(upload_to="images/")
    text = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    
class StoryView(models.Model):
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name="storyviews",
        related_query_name="storyview",
    )
    viewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="storyviews",
        related_query_name="storyview",
    )
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["story", "viewer"], name="unique_story_view")
        ]
    