from rest_framework import serializers
from django.contrib.auth import get_user_model

global User
User = get_user_model()


class UserTokenSerializer(serializers.Serializer):
    userID = serializers.IntegerField()

    def validate(self, data):
        User = get_user_model()
        try:
            User.objects.get(pk=data['userID'])
        except User.DoesNotExist:
            raise serializers.ValidationError('User Not Found.')
        return data



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        # fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)
