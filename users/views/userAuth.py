from rest_framework.generics import CreateAPIView
from users.models import User
from users.serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterAPIView(CreateAPIView):
    queryset = User
    serializer_class = RegisterSerializer

    def create(self, request):
        user = super().create(request)
        return Response({
            "success" : "User has been created"
        }, status = status.HTTP_201_CREATED)
    

class LoginAPIView(CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Get User Token
        refresh = RefreshToken.for_user(user)

        # Return Customized Response
        return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.pk,
                'role' : user.get_role_display()
        }, status=status.HTTP_200_OK)