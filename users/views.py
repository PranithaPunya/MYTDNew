from rest_framework import viewsets
from users.permissions import IsAdminRole
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().order_by('id')
    serializer_class = UserProfileSerializer
    permission_classes = []
    lookup_field = 'id'

class AdminOnlyAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request):
        # Only admin users can access this
        return Response({"message": "Hello, Admin!"})
    
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        print(f"Attempting to authenticate user with email: {email}")
        user = authenticate(username=email, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        print(f"Logging out user: {user}")
        user.auth_token.delete()
        return Response(
            {"message": "Logged out successfully"}, status=status.HTTP_200_OK
        )