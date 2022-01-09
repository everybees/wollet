from rest_framework import serializers
from api.models import User, Wallet


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'user_type', 'email', 'user_type', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Creates User and Wallet"""
        user = User(
            **validated_data
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class WalletSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Wallet
        fields = '__all__'
