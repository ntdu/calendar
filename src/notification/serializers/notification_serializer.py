# -*- coding: utf-8 -*-
import json

from rest_framework import serializers
from src.notification.models import Notification, User


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

    def validate(self, data):
        if not data:
            raise serializers.ValidationError({"data": "data None"})

        if not isinstance(data, dict):
            data = json.loads(data)

        if not data.get("users") or not isinstance(data.get("users"), list):
            raise serializers.ValidationError({"users": "users Invalid"})

        if data.get("type") not in [c[0] for c in Notification.NotificationTypeChoice.choices]:
            raise serializers.ValidationError({"type": "type Invalid"})

        users = data.get("users")
        del data['users']

        data_keys = list(data.keys())
        data_vals = data.values()
        data_vals = list(map(lambda x: '' if x is None else x, data_vals))

        return users, {data_keys[i]: data_vals[i] for i in range(len(data_keys))}


class GetMergedNotificationSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(source='get_id', read_only=True)
    merged_data = serializers.SerializerMethodField(source='get_merged_data', read_only=True)

    def get_id(self, obj):
        return str(obj.id)

    def get_merged_data(self, obj):
        data = []
        count = 0   # NOSONAR

        for item in obj.get_all_children():
            count += 1      # NOSONAR
            data.append(item.id)

        return str(data)

    class Meta:
        model = Notification
        fields = ["id", "merged_data"]


class GetNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class RegisterTokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)


class RegisterCalendarTokenSerializer(serializers.Serializer):
    calendar_access_token = serializers.CharField(required=True)
    calendar_refresh_token = serializers.CharField(required=True)
    client_id = serializers.CharField(required=True)
    client_secret = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'