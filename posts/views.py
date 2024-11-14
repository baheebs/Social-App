from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .models import Post, Like
from .serializers import UserSerializer, PostSerializer, LikeSerializer, PostListSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Custom permissions based on the action.
        - Allow any user to access `create` (user registration).
        - Require authentication for all other actions.
        """
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        """
        Ensure users can only update their own data.
        """
        user = self.get_object()
        if user != request.user:
            return Response({"detail": "You do not have permission to update this user."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Ensure users can only partially update their own data.
        """
        user = self.get_object()
        if user != request.user:
            return Response({"detail": "You do not have permission to update this user."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Ensure users can only delete their own account.
        """
        user = self.get_object()
        if user != request.user:
            return Response({"detail": "You do not have permission to delete this user."},
                            status=status.HTTP_403_FORBIDDEN)
        user.delete()
        return Response({"detail": "User account deleted successfully."},
                        status=status.HTTP_204_NO_CONTENT)

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def list(self, request):
        posts = Post.objects.filter(is_published=True).exclude(created_by=request.user)
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="basic-list")
    def basic_list(self, request, *args, **kwargs):
        """
                Return all posts created by the authenticated user.
                """
        # Filter posts created by the authenticated user
        queryset = self.queryset.filter(created_by=request.user)
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="published-posts")
    def published_posts(self, request):
        """
        Custom endpoint: List all published posts created by the authenticated user.
        """
        posts = Post.objects.filter(is_published=True, created_by=request.user)
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

class PublishUnpublishPostView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def update(self, request, pk=None):
        try:
            post = Post.objects.get(id=pk, created_by=request.user)
            post.is_published = not post.is_published
            post.save()
            return Response({'status': 'published' if post.is_published else 'unpublished'})
        except Post.DoesNotExist:
            return Response({'error': 'Post not found or unauthorized'}, status=404)

class LikeUnlikeView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """
        Like a post only if it is published.
        """
        try:
            post = Post.objects.get(id=pk)
            if not post.is_published:
                return Response({'error': 'You can only like published posts.'}, status=400)

            Like.objects.get_or_create(post=post, user=request.user)
            return Response({'status': 'liked'})
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=404)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        """
        Unlike a post only if it is published.
        """
        try:
            post = Post.objects.get(id=pk)
            if not post.is_published:
                return Response({'error': 'You can only unlike published posts.'}, status=400)

            Like.objects.filter(post=post, user=request.user).delete()
            return Response({'status': 'unliked'})
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=404)
