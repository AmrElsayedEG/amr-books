from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView, ListAPIView
from users.models import User
from users.serializers import UserSerializer, ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class RetrieveUpdateUserProfileAPIView(RetrieveUpdateAPIView):
    queryset = User
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        # Get current user profile
        return self.request.user
    
class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        try:
            user = self.serializer_class(data=self.request.data, context={'request' : self.request})
            user.is_valid(raise_exception=True)
            user.update(user.validated_data)
            return Response(
                {
                    "success" : "Password changed successfully"
                }, status=status.HTTP_200_OK
            )
        except:
            return Response(
                {
                    "error" : "Something went wrong, Please try again later"
                }, status=400
            )