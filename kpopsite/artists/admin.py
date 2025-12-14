from django.contrib import admin
from .models import Company, Member, Group, SoloArtist, MonthlyRating
# Register your models here.

admin.site.register(Company)
admin.site.register(Member)
admin.site.register(Group)
admin.site.register(SoloArtist)
admin.site.register(MonthlyRating)