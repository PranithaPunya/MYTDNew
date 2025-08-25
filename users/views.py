from rest_framework import viewsets

from .models import UserProfile
from .serializers import UserProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().order_by('id')
    serializer_class = UserProfileSerializer
    permission_classes = []
    lookup_field = 'id'
