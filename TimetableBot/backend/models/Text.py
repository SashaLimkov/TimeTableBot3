from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Языки"

    def __str__(self) -> str:
        return self.name


class Text(models.Model):
    key = models.CharField(max_length=128, verbose_name="ключ")

    class Meta:
        verbose_name = "Ключ"
        verbose_name_plural = "Ключи"

    def __str__(self) -> str:
        return self.key


class Translate(models.Model):
    text_key = models.ForeignKey(
        Text, on_delete=models.CASCADE, related_name="all_translates"
    )
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="all_text"
    )
    translate = models.TextField(max_length=2048, verbose_name="Текст")

    class Meta:
        verbose_name = "Текст на языке"
        verbose_name_plural = "Тексты на языках"

    def __str__(self) -> str:
        return f"{self.text_key.key}: {self.translate}"
