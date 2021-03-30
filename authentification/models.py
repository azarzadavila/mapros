import secrets

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from mapros.settings import CURRENT_URL


def create_confirmation(cls, user, frontend_url=""):
    url = secrets.token_urlsafe()
    while cls.objects.filter(url=url).exists():
        url = secrets.token_urlsafe()
    confirmation = cls.objects.create(
        url=secrets.token_urlsafe(),
        user=user,
        timestamp=timezone.now(),
        frontend_url=frontend_url,
    )
    confirmation.send()
    return confirmation


class EmailConfirmation(models.Model):
    url = models.URLField(unique=True)
    frontend_url = models.URLField(blank=True)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    def is_valid(self):
        return timezone.now() - self.timestamp < timezone.timedelta(days=1)

    def send(self):
        msg = "Please visit the following url to confirm your account :\n"
        if self.frontend_url:
            url = self.frontend_url + "?token=" + self.url + "/"
        else:
            url = CURRENT_URL + "confirm_account/" + self.url + "/"
        msg += url
        self.user.email_user(
            "MaPros account confirmation", msg, from_email="noreply@mapros.be"
        )

    @classmethod
    def create(cls, user, frontend_url=""):
        create_confirmation(cls, user, frontend_url)


class ResetPasswordConfirmation(models.Model):
    url = models.URLField(unique=True)
    frontend_url = models.URLField(blank=True)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    def is_valid(self):
        return timezone.now() - self.timestamp < timezone.timedelta(days=1)

    def send(self):
        msg = "Please visit the following url to reset your password :\n"
        if self.frontend_url:
            url = self.frontend_url + "?token=" + self.url + "/"
        else:
            url = CURRENT_URL + "reset_password/" + self.url + "/"
        msg += url
        self.user.email_user(
            "MaPros password reset", msg, from_email="noreply@mapros.be"
        )

    @classmethod
    def create(cls, user, frontend_url=""):
        return create_confirmation(cls, user, frontend_url)
