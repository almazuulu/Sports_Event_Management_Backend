from rest_framework import serializers
from ..models import User
   
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['id']
       
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
   
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'role']
        read_only_fields = ['id']
   
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
   
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data.get('role', 'user')
        )
        user.set_password(validated_data['password'])  # Хэшируем пароль
        user.save()
        return user