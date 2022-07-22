from rest_framework import serializers
from .models import newUser
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.serializers import AuthTokenSerializer


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = newUser
        fields = ('email', 'username', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }

    def create(self, validation_data):
        password = validation_data.pop('password')
        user = self.Meta.model(**validation_data)
        user.set_password(password)
        user.save()
        return user

    def validate(self, data):
        password = data.get('password')
        password2 = data.pop('password2')
        if(password2 != password):
            raise serializers.ValidationError(_('passwords do not match'))
        return data


class newTokenSerializer(AuthTokenSerializer):
    username = None
    email = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs.get('email') and attrs.get('password'):
            user = authenticate(request=self.context.get('request'),
                                **attrs)
            user2 = authenticate()
            print(user2)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
