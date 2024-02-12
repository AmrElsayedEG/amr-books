from rest_framework import serializers
from users.models import User
import logging

logger = logging.getLogger(__name__)

class RegisterSerializer(serializers.ModelSerializer):
    
    error_msg = {
        'exists' : 'A user with this username already exists'
    }
    class Meta:
        model = User
        fields = ('username', 'phone_number', 'role', 'password')
        extra_kwargs = {'password' : {'write_only':False}}

    def validate(self, attrs):
        if User.objects.filter(username=attrs['username']).exists():
            logger.info(f'New user tried to register with existing username: {attrs["username"]}')
            raise serializers.ValidationError(self.error_msg['exists'])
        return attrs

    def create(self, validated_data):
        password = validated_data.get('password')

        user = super().create(validated_data)

        user.set_password(password)

        user.save()

        return user
    
class LoginSerializer(serializers.ModelSerializer):

    error_msg = {
        "login" : {
            "error" : "Invalid Username or Password",
        },
        "not_active" : {
            "error" : "This account is not activated, Please contact the manager.",
        }
    }

    username = serializers.CharField(help_text="Enter phone here")
    password = serializers.CharField(help_text="Enter password here")

    class Meta:
        model = User
        fields = ('username', 'password',)

    def validate(self, attrs):
        user = User.objects.filter(username=attrs['username']).last()

        if not user:
            raise serializers.ValidationError(self.error_msg['login'])

        if not user.check_password(attrs['password']):
            logger.warn(f"[Login] Wrong password for username: {attrs['username']}")
            raise serializers.ValidationError(self.error_msg['login'])

        if not user.is_active:
            raise serializers.ValidationError(self.error_msg['not_active'])

        attrs['user'] = user

        return attrs