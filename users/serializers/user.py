from rest_framework import serializers
from users.models import User
import logging
logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'phone_number', 'role',)

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        return attrs
    
    def update(self, validated_data):
        user = validated_data.get('user')
        user.set_password(validated_data.get('password'))
        user.save()
        return user