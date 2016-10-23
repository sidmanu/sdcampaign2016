from rest_framework import serializers
from bodhibuddyapp.models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # A field from the user's profile:
    current_state = serializers.CharField(source='profile.current_state')
    status = serializers.CharField(source='profile.status')

    class Meta:
        model = User
        fields = ('url', 'username', 'status', 'current_state')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = super(UserSerializer, self).create(validated_data)
        self.create_or_update_profile(user, profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        self.create_or_update_profile(instance, profile_data)
        return super(UserSerializer, self).update(instance, validated_data)

    def create_or_update_profile(self, user, profile_data):
        profile, created = Profile.objects.get_or_create(user=user, defaults=profile_data)
        if not created and profile_data is not None:
            super(UserSerializer, self).update(profile, profile_data)


class SharedDaimokuTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedDaimokuTarget
        fields = ('title','description','creator','target_count',
            'target_date_millis','create_date_millis')
