from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from hackathon.models import Hackathon, Enroll
from hackathon.constants import SUBMISSION_TYPE
import uuid

# Create your models here.


def username_path(instance, filename):
    return "{0}/user_{1}/{2}_{3}".format(
        instance.hackathon.submission_type,
        instance.owner.username,
        instance.hackathon.title,
        filename,
    )


class Submission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    submission_name = models.CharField(max_length=100)
    summary = models.TextField()
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=10, choices=SUBMISSION_TYPE, default="LINK")
    text_file = models.FileField(upload_to=username_path, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    image_file = models.ImageField(upload_to=username_path, blank=True, null=True)

    def __str__(self):
        return (
            str(self.owner.username)
            + ""
            + str(self.hackathon.title)
            + ""
            + str(self.id)
        )

    def clean(self):
        self.is_valid = True
        if self.hackathon.submission_type != self.type:
            raise ValidationError("The Submission Format is Invalid")
        if (
            self.type == "LINK"
            and self.link is None
            and self.text_file is not None
            and self.image_file is not None
        ):
            raise ValidationError("b Submission format invalid !")
        elif (
            self.type == "IMAGE"
            and self.image_file is None
            and self.text_file is not None
            and self.link is not None
        ):
            raise ValidationError("c Submission format invalid !")
        elif (
            self.type == "FILE"
            and self.text_file is None
            and self.link is not None
            and self.image_file is not None
        ):
            raise ValidationError("d Submission format invalid !")
        super(Submission, self).clean()

    def save(self, *args, **kwargs):
        if not self.is_valid:
            self.full_clean()
        super(Submission, self).save(*args, **kwargs)
