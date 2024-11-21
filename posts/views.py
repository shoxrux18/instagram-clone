from django.db.models import F,Count
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from . import models, serializers
from .permissions import CreatorOnlyPermission
from .tasks import create_story_view


class PostListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        posts = models.Post.objects.select_related('user').annotate(like_count=Count("like"))
        serializer = serializers.PostSerializer(
            posts, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.PostEditSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)


class PostRetrieveUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [CreatorOnlyPermission()]

    def get(self, request, pk):
        post = get_object_or_404(models.Post, pk=pk)
        serializer = serializers.PostDetailSerializer(
            post, context={"request": request}
        )
        return Response(serializer.data)

    def patch(self, request, pk):
        post = get_object_or_404(models.Post, pk=pk)
        self.check_object_permissions(request, post)
        serializer = serializers.PostEditSerializer(
            post, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PostLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(models.Post.objects.exclude(user=request.user), pk=pk)
        if models.Like.objects.filter(user=request.user, post=post).exists():
            return Response(status=200)
        models.Like.objects.create(user=request.user, post=post)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        like = get_object_or_404(models.Like, user=request.user, post__pk=pk)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostCommentListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        post = get_object_or_404(models.Post, pk=pk)
        comment = post.comments.filter(comment__isnull=True).select_related("user")
        serializer = serializers.PostCommentListSerializer(
            comment, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request, pk):
        post = get_object_or_404(models.Post, pk=pk)
        serializer = serializers.PostCommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class CommentDeleteView(APIView):
    permission_classes = [CreatorOnlyPermission]

    def delete(self,request,pk):
        comment = get_object_or_404(models.Comment,pk=pk)
        self.check_object_permissions(request, comment)       
        comment.delete()
        return Response(status=204)
        


class CommentReplyCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        comment = get_object_or_404(models.Comment, pk=pk)
        serializer = serializers.PostCommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, comment=comment,post=comment.post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentLikeView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [CreatorOnlyPermission()]

    def post(self,request,pk):
        comment = get_object_or_404(models.Comment,pk=pk)
        comment_like = models.CommentLike.objects.filter(user=request.user,comment=comment).first()
        if not comment_like:
            models.CommentLike.objects.create(comment=comment,user=request.user)
            comment.like_number = F('like_number') + 1
            comment.save()
            return Response(status=201)
        return Response(status=400)

    
    def delete(self,request,pk):
        comment_like = get_object_or_404(models.CommentLike,pk=pk)
        self.check_object_permissions(request,comment_like)
        comment = comment_like.comment
        comment_like.delete()
        comment.like_number = F('like_number') - 1
        comment.save()
        return Response(status=204)
        

class StoryListCreateView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.StoryListCreateSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("pk")
        return models.Story.objects.filter(user=user_id)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StoryDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,pk):
        story=get_object_or_404(models.Story,pk=pk)
        if story.user != request.user:            
            create_story_view.delay(story.pk, request.user.pk)            
        serializer = serializers.StoryListCreateSerializer(story,context={"request": request})
        return Response(serializer.data,status=201)


class StoryViewersList(APIView):
    permission_classes = [CreatorOnlyPermission]

    def get(self, request, pk):
        story = get_object_or_404(models.Story, pk=pk)
        self.check_object_permissions(request, story)
        storyviewers = models.StoryView.objects.filter(story=story)
        serializer = serializers.StoryViewersListSerializer(storyviewers, many=True, context={"request": request})
        return Response(serializer.data, status=200)
