from modeltranslation.admin import TranslationAdmin
from django.contrib import admin
from . import models


@admin.register(models.Post)
class PostAdmin(TranslationAdmin):
    list_display = ("title", "user", "created_at")


@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")


@admin.register(models.Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ("pk","text", "user", "post")


@admin.register(models.CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ("pk","user", "comment", "created_at")
    

@admin.register(models.Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("pk","user", "text", "created_at")

@admin.register(models.StoryView)
class StoryViewAdmin(admin.ModelAdmin):
    list_display = ("pk","story", "viewer", "viewed_at")