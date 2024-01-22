from django.contrib import admin
from zira.models import GeminiImage

# Register your models here.

class GeminiImageAdmin(admin.ModelAdmin):
    list_display = ["id","text_field", "image_field"]


admin.site.register(GeminiImage, GeminiImageAdmin)
