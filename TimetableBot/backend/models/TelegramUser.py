from django.db import models

class TelegramUser(models.Model):
    telegram_id = models.CharField(max_length=20, verbose_name="Телеграм ID")
    full_name = models.CharField(max_length=128, verbose_name="Пользователь")
    selected_language = models.ForeignKey("Language", on_delete=models.SET_NULL, null=True, verbose_name="язык Бота", related_name="users_with_lang")
    notifications = models.BooleanField("Уведомления включены?", default=False)
    selected_group = models.CharField("Группа пользователя", max_length=512,default=None, blank=True, null=True)
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return self.full_name
