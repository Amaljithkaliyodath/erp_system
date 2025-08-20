from rest_framework import generics, permissions, status
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render

User = get_user_model()

# --- Frontend Pages ---
def login_page(request):
    return render(request, "login.html")

def dashboard_page(request):
    return render(request, "dashboard.html")

# --- API Views ---
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UserListCreateDeleteUpdateView(
    generics.ListCreateAPIView,
    generics.DestroyAPIView,
    generics.UpdateAPIView
):
    """
    - Admin: can view all users, add new users, edit, delete users
    - Manager: can view employees only (read-only)
    - Employee: can only see self
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "Admin":
            return User.objects.all()
        elif user.role == "Manager":
            return User.objects.exclude(role="Admin")
        else:
            return User.objects.filter(id=user.id)

    def create(self, request, *args, **kwargs):
        if request.user.role != "Admin":
            return Response({"detail": "Only Admins can add users."}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.user.role != "Admin":
            return Response({"detail": "Only Admins can update users."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.role != "Admin":
            return Response({"detail": "Only Admins can delete users."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
