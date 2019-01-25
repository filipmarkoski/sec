from django.contrib import admin
from .models import Litigation


# Register your models here.
class LitigationsAdmin(admin.ModelAdmin):
    list_display = ('release_no',)


admin.site.register(Litigation, LitigationsAdmin)
