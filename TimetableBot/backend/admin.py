from django.contrib import admin
from .models import TelegramUser, Text


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "full_name", "selected_language")
    list_display_links = ("full_name",)
    search_fields = (
        "full_name",
        "telegram_id",
    )


class TranslatesAdmin(admin.ModelAdmin):
    list_display = ("text_key", "language", "translate")
    list_display_links = ("translate",)
    raw_id_fields = ("text_key", "language")
    search_fields = ("Translate",)
    list_filter = ("language",)


class TranslatesInline(admin.StackedInline):
    model = Text.Translate
    fields = ["text_key", "language", "translate"]
    show_change_link = True
    extra = 0


class TextAdmin(admin.ModelAdmin):
    inlines = [TranslatesInline]


admin.site.register(TelegramUser.TelegramUser, TelegramUserAdmin)
admin.site.register(Text.Language)
admin.site.register(Text.Translate, TranslatesAdmin)
admin.site.register(Text.Text, TextAdmin)
