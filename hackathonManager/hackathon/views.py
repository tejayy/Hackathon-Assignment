from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.utils import timezone


# Create your views here.

"""Create a new hackathon for authorized users"""


class CreateHackathon(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            hackathon = Hackathon.objects.create(
                hosted_by=request.user,
                title=data["title"],
                background_image=data["background_image"],
                hackathon_image=data["hackathon_image"],
                submission_type=data["submission_type"],
                start_datetime=data["start_datetime"],
                end_datetime=data["end_datetime"],
                reward_price=data["reward_price"],
            )
            serialized_data = HackathonSerializer(hackathon).data
            return Response(
                {
                    "success": True, 
                    "details": serialized_data
                }, status=status.HTTP_202_ACCEPTED
            )
        except Exception:
            return Response(
                {"success": False, "message": "Please Enter Valid Entry"},
                status=status.HTTP_400_BAD_REQUEST
            )


"""Shows all the hackathon entries"""
class ViewHackathon(APIView):
    def get(self, request):
        all_entries = Hackathon.objects.filter(end_datetime__gte=timezone.now())
        serialized_data = HackathonEnrollSerializer(all_entries, many=True).data
        return Response(
            {"success": True, "details": serialized_data}, status=status.HTTP_200_OK
        )


"""shows users enrollments"""


from django.shortcuts import get_object_or_404


class Enroll(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            hackathon_id = data["hackathon_id"]
            hackathon_obj = Hackathon.objects.get(id=hackathon_id)
            if hackathon_obj.end_datetime < timezone.now():
                return Response(
                    {"success": False, "message": "Hackathon expired"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            enrl_obj = Enroll.objects.filter(user=request.user, hackathon=hackathon_obj)
            if len(enrl_obj) > 0:
                return Response(
                    {"success": False, "message": "Already Enrolled"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                enrl_obj = Enroll.objects.create(
                    user=request.user, hackathon=hackathon_obj
                )
                serialized_data = EnrollSerializer(enrl_obj).data
                return Response(
                    {"success": True, "hackathon_data": serialized_data},
                    status=status.HTTP_202_ACCEPTED,
                )
        except Exception:
            return Response(
                {"success": False, "message": "Hackathon does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
