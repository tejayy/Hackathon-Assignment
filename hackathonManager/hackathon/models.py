from urllib import request
from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext as _


# Create your models here.


def upload_to(instance, filename):
    return "img/{filename}".format(filename=filename)


class Hackathon(models.Model):
    SUBMISSION_TYPE = (
        ("IMAGE", _("Image")),
        ("FILE", _("File")),
        ("LINK", _("Link")),
    )
    id = models.UUIDField(primary_key=True, editable=True, default=uuid.uuid4)
    hosted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=255)
    background_image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    hackathon_image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    submission_type = models.CharField(
        max_length=6, choices=SUBMISSION_TYPE, default="LINK"
    )
    start_datetime = models.DateTimeField(default=timezone.now, editable=True)
    end_datetime = models.DateTimeField(editable=True, blank=True, null=True)
    reward_price = models.IntegerField()

    def get_absolute_url(self):
        return reverse("hackathon-detail", kwargs={"pk": self.pk})

    def get_bgimage_url(self):
        return self.background_image.url

    def get_hackathonimage_url(self):
        return self.hackathon_image.url

    def __str__(self):
        return str(self.title)


class Enroll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return str(self.user.username) + " " + str(self.hackathon.title)
