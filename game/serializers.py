from rest_framework import serializers
from .models import GameResult
from user.models import UserProfile
from museum.models import Simulator
from django.shortcuts import get_object_or_404
from badges.models import Badge

class GameResultSerializer(serializers.Serializer):
    pilot = serializers.SlugRelatedField(slug_field='qr_token', queryset=UserProfile.objects.all())
    copilot = serializers.SlugRelatedField(slug_field='qr_token', allow_null=True, queryset=UserProfile.objects.all())
    simulator = serializers.PrimaryKeyRelatedField(queryset=Simulator.objects.all())
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    score = serializers.IntegerField()
    num_of_rolls = serializers.IntegerField()
    museum_secret_key = serializers.CharField(max_length=24, write_only=True)
    badges = serializers.ListField(allow_empty=True)
        
    def validate(self, data):
        if not data['museum_secret_key'] == data['simulator'].museum.secret_key:
            raise serializers.ValidationError("Incorrect API key")

        if data['end_time'] <= data['start_time']:
            raise serializers.ValidationError("Start time is after end time")

        if (GameResult.objects.filter(
            pilot=data['pilot'], start_time=data['start_time']).exists()):
            raise serializers.ValidationError("Duplicate result")

        return data

    def save(self):
        params = self.validated_data.copy()
        params.pop('museum_secret_key')

        badges = params.pop('badges')

        gr = GameResult.objects.create(**params)

        for badgeId in badges:
            guid = badgeId['guid']
            tier = badgeId['tier']
            badge = get_object_or_404(Badge, guid=guid)
            bt = badge.badgetier_set.filter(tier_number=tier).first()
            bt.game_results.add(gr)
            bt.save()

        gr.send_live_result() 



class DisplayGameResultSerializer(serializers.ModelSerializer):
    pilot = serializers.SerializerMethodField(method_name='get_pilot_username')
    copilot = serializers.SerializerMethodField(method_name='get_copilot_username')

    class Meta:
        model = GameResult
        fields = ['pilot', 'copilot', 'score']

    def get_pilot_username(self, obj):
        return obj.pilot.display_name

    def get_copilot_username(self, obj):
        if obj.copilot:
            return obj.copilot.display_name
        else:
            return ''
