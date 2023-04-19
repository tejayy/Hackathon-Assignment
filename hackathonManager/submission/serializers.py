from .models import *
from rest_framework import serializers
from users.serializers import DisplaySerializer
from hackathon.serializers import HackathonEnrollSerializer



class SubmissionSerializer(serializers.ModelSerializer):
    hackathon = HackathonEnrollSerializer()
    owner = DisplaySerializer()
    class Meta:
        model = Submission
        fields = '__all__'