from django.db import models


class TelegramUser(models.Model):
    username = models.CharField(max_length=255)
    userid = models.CharField(max_length=255)
    referid = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return self.username
class Configure(models.Model):
    token = models.CharField(max_length=1000, verbose_name="Bot tokeni")
    channels = models.TextField(verbose_name="Kanallar")
    links = models.TextField(verbose_name="Linklar")

    def __str__(self) -> str:
        return str(self.token)
    
class PhoneNumber(models.Model):
    username = models.CharField(max_length=1000, verbose_name="Telegram username")
    number = models.CharField(max_length=20, verbose_name="Telefon raqam")

    def __str__(self) -> str:
        return self.number