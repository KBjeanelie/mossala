from rest_framework import serializers
from backend.models.app_report import WarningFromUser, FeedBackFromUser

class WarningFromUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarningFromUser
        fields = ['id', 'warning_message', 'created_at']

class FeedBackFromUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBackFromUser
        fields = ['id', 'feedback_message', 'created_at']