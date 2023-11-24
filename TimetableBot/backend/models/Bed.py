from django.db import models
from TelegramUser import TelegramUser

class Bed(models.Model):
    room = models.ForeignKey("Room", on_delete=models.SET_NULL, null=True, related_name="room_beds")
    qr_code = models.FileField(upload_to="generated_qr_сodes", verbose_name="QR")

    class Meta:
        verbose_name = "Вип место"
        verbose_name_plural = "Вип места"

    def __str__(self):
        return f"{self.room.number} {self.room.coordinates}"


class UserBed(models.Model):
    bed = models.ForeignKey(Bed, on_delete=models.SET_NULL, null=True, related_name="patient_on_bed")
    patient = models.ForeignKey(TelegramUser, on_delete=models.SET_NULL, null=True, related_name="bed")
    user = models.ForeignKey(TelegramUser, on_delete=models.SET_NULL, null=True, related_name="patient")

    class Meta:
        verbose_name = "Вип связь"
        verbose_name_plural = "Вип связи"

    def __str__(self):
        return f"{self.user.full_name} {self.patient.full_name}"


class Room(models.Model):
    number = models.CharField(max_length=256, default="")
    coordinates = models.CharField(max_length=512, default="") 

    class Meta:
        verbose_name = "Вип палата"
        verbose_name_plural = "Вип палаты"

    def __str__(self):
        return f"{self.number} {self.coordinates}"

 