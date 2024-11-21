from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from . import models, serializers

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer



class AccountListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        users = User.objects.exclude(pk=request.user.pk).prefetch_related("posts")
        serializer = serializers.AccountListSerializer(
            users, many=True, context={"request": request}
        )
        return Response(serializer.data)


class AccountDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if (
            user.is_public
            or models.AccountConnection.objects.filter(
                follower=request.user, following=user, is_request_accepted=True
            ).exists()
        ):
            serializer = serializers.AccountSerializer(
                user, context={"request": request}
            )
        else:
            serializer = serializers.AccountPreviewSerializer(
                user, context={"request": request}
            )
        return Response(serializer.data)


class FollowCreateOrDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,pk):
        user = get_object_or_404(User,pk=pk)
        if user == request.user:
            return Response(status=400)
        if not models.AccountConnection.objects.filter(follower=request.user,following=user).exists():
            models.AccountConnection.objects.create(follower=request.user,following=user,is_request_accepted=False)
            return Response(status=201)
        return Response(status=200) 
    
    def delete(self,request,pk):        
        connection = get_object_or_404(models.AccountConnection,pk=pk)
        if (connection.follower==request.user or connection.following==request.user) and connection.is_request_accepted:
            connection.delete()
            return Response(status=204)
        return Response(status=403)


class FollowRequestUpdateOrDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        connection = get_object_or_404(models.AccountConnection, pk=pk)
        if connection.following == request.user and not connection.is_request_accepted:
            serializer = serializers.FollowRequestAcceptSerializer(
                connection, data=request.data
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=200)
        return Response(status=403)

    def delete(self, request, pk):
        connection = get_object_or_404(models.AccountConnection, pk=pk)
        if (connection.following == request.user or connection.follower == request.user) and not connection.is_request_accepted:
            connection.delete()
            return Response(status=204)
        return Response(status=403)


class RequestListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        lst_requests = models.AccountConnection.objects.filter(
            following=request.user, is_request_accepted=False
        )
        serializer = serializers.RequestListSerializer(lst_requests, many=True)
        return Response(serializer.data)


class FollowerListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        user = get_object_or_404(User, pk=pk) if pk else request.user
        qs = models.AccountConnection.objects.filter(
            following=user, is_request_accepted=True
        )
        serializer = serializers.FollowerListSerializer(qs, many=True)
        return Response(serializer.data)


class FollowingListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        user = get_object_or_404(User, pk=pk) if pk else request.user
        qs = models.AccountConnection.objects.filter(
            follower=user, is_request_accepted=True
        )
        serializer = serializers.FollowingListSerializer(qs, many=True)
        return Response(serializer.data)