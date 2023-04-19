from rest_framework import serializers
from .models import *
from users.serializers import DisplaySerializer


class HackathonSerializer(serializers.ModelSerializer):
    hosted_by = DisplaySerializer
    class Meta:
        model = Hackathon
        fields = ('id', 'title', 'hosted_by', 'background_image', 'hackathon_image', 'submission_type', 'start_datetime', 'end_datetime', 'reward_price')
        

class HackathonEnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = ('id', 'title', 'hackathon_image', 'start_datetime', 'end_datetime', 'reward_price')

       
class EnrollSerializer(serializers.ModelSerializer):
    hackathon = HackathonEnrollSerializer()
    user = DisplaySerializer()
    class Meta:
        model = Enroll
        fields = ('user', 'hackathon', 'enrollment_date')
        

