from django.contrib import admin
from .models import User, Usage 

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "password")

class UsageAdmin(admin.ModelAdmin):
    list_display = ("user", "cause", "cost", "year", "month", "day")

admin.site.register(User, UserAdmin)
admin.site.register(Usage, UsageAdmin)