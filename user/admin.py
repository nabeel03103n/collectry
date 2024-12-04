from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Contact)
admin.site.register(InfoAPI)
admin.site.register(Payment)
admin.site.register(Location)
admin.site.register(UserForm)
admin.site.register(UserProfile)
# admin.site.register(UserProfile)


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'image')  # Fields to display in the admin list
    search_fields = ('title', 'content')  # Fields to search by
    list_filter = ('start_date', 'end_date')  # Filters for listing ads