from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Todo
from .serializers import RegisterSerializer, TodoSerializer, UserSerializer


class DefaultPagination(PageNumberPagination):
    """Default pagination for list endpoints."""
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


# PUBLIC_INTERFACE
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def health(request):
    """Health check endpoint to verify server availability.

    Returns:
        200 OK with message indicating server status.
    """
    return Response({"message": "Server is up!"})


class IsOwner(permissions.BasePermission):
    """Custom permission to only allow owners of a todo to access it."""

    def has_object_permission(self, request, view, obj):
        return getattr(obj, "owner_id", None) == getattr(request.user, "id", None)


class TodoViewSet(viewsets.ModelViewSet):
    """CRUD operations for Todo items.

    Requires authentication. All objects are filtered to the authenticated user's ownership.

    List and filtering:
    - Optional query params:
        - is_completed: true/false to filter by completion status
        - search: substring search in title or description
    """
    serializer_class = TodoSerializer
    pagination_class = DefaultPagination
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        qs = Todo.objects.filter(owner=self.request.user)
        is_completed = self.request.query_params.get("is_completed")
        search = self.request.query_params.get("search")
        if is_completed is not None:
            if is_completed.lower() in ("true", "1", "yes"):
                qs = qs.filter(is_completed=True)
            elif is_completed.lower() in ("false", "0", "no"):
                qs = qs.filter(is_completed=False)
        if search:
            qs = qs.filter(models.Q(title__icontains=search) | models.Q(description__icontains=search))
        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"], url_path="toggle", permission_classes=[permissions.IsAuthenticated, IsOwner])
    def toggle(self, request, pk=None):
        """Toggle completion state for a todo."""
        todo = self.get_object()
        todo.is_completed = not todo.is_completed
        todo.save(update_fields=["is_completed", "updated_at"])
        return Response(self.get_serializer(todo).data)


# Authentication and user endpoints

# PUBLIC_INTERFACE
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@csrf_exempt
def register(request):
    """Register a new user.

    Body:
        username: string
        email: string (optional)
        password: string

    Returns:
        201 Created with user object, or 400 on validation error.
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PUBLIC_INTERFACE
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@csrf_exempt
def login_view(request):
    """Login user with username and password, using session authentication.

    Body:
        username: string
        password: string

    Returns:
        200 OK with user info on success, 401 Unauthorized on failure.
    """
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    login(request, user)
    return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


# PUBLIC_INTERFACE
@api_view(["POST"])
def logout_view(request):
    """Logout current user (session)."""
    logout(request)
    return Response({"detail": "Logged out"}, status=status.HTTP_200_OK)


# PUBLIC_INTERFACE
@api_view(["GET"])
def me(request):
    """Return current authenticated user's profile."""
    return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
