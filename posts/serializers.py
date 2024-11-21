from rest_framework import serializers
from django.contrib.auth import get_user_model
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
        )

class PostSerializer(serializers.ModelSerializer):
    # number_of_likes = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Post
        fields = (
            "id",
            "title",
            "image",
            "is_public",
            # "number_of_likes",
            "user"
        )

    def get_number_of_likes(self, obj: models.Post):
        return obj.like_count


class PostDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    number_of_likes = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Post
        fields = (
            "id",
            "title",
            "image",
            "content",
            "number_of_likes",
            "updated_at",
            "created_at",
            "user",
        )

    def get_number_of_likes(self, obj: models.Post):
        if obj.show_likes:
            return models.Like.objects.filter(post=obj).count()


class PostEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ("title", "image", "content", "is_public", "show_likes")


class PostCommentListSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user = UserSerializer()

    class Meta:
        model = models.Comment
        fields = ("pk","text", "user","like_number","replies")
    
    def get_replies(self,obj):
        return PostCommentListSerializer(obj.replies.all(),many=True).data
    


class PostCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ("text",)


class StoryListCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = models.Story
        fields = ("user","image","text")

    
class StoryViewersListSerializer(serializers.ModelSerializer):
    viewer = serializers.SerializerMethodField()
    class Meta:
        model = models.StoryView
        fields = ("viewer","viewed_at")

    def get_viewer(self,obj):
        return obj.viewer.email