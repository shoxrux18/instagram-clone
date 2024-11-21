from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from posts import serializers as posts_serializers
from . import models


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, data):
        tokens = super().validate(data)
        tokens["user"] = UserSerializer(self.user, context=self.context).data
        return tokens


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
        )


class AccountListSerializer(serializers.ModelSerializer):
    # connection = serializers.SerializerMethodField()
    posts = posts_serializers.PostSerializer(many=True)
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            # "connection",
            "posts"
            
        )

    def get_connection(self, obj):
        user = self.context["request"].user
        user_follows_obj = models.AccountConnection.objects.filter(
            follower=user, following=obj, is_request_accepted=True
        ).exists()
        obj_follows_user = models.AccountConnection.objects.filter(
            follower=obj, following=user, is_request_accepted=True
        ).exists()

        if user_follows_obj and obj_follows_user:
            return "You follow each other"
        elif user_follows_obj:
            return "You follow this user"
        elif obj_follows_user:
            return "This user follows you"
        else:
            return "There is no connection between you and this user"

    
class AccountPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
        )


class AccountSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "date_joined",
            "followers",
            "following",
        )

    def get_followers(self, obj: models.AccountConnection):
        return models.AccountConnection.objects.filter(
            following=obj, is_request_accepted=True
        ).count()

    def get_following(self, obj):
        return models.AccountConnection.objects.filter(
            follower=obj, is_request_accepted=True
        ).count()


class FollowRequestAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AccountConnection
        fields = ("is_request_accepted",)


class RequestListSerializer(serializers.ModelSerializer):
    follower_email = serializers.SerializerMethodField()

    class Meta:
        model = models.AccountConnection
        fields = ("follower_email",)

    def get_follower_email(self, obj: models.AccountConnection):
        return obj.follower.email


class FollowerListSerializer(serializers.ModelSerializer):
    follower = UserSerializer()

    class Meta:
        model = models.AccountConnection
        fields = (
            "pk",
            "follower",
        )


class FollowingListSerializer(serializers.ModelSerializer):
    following = UserSerializer()

    class Meta:
        model = models.AccountConnection
        fields = (
            "pk",
            "following",
        )
