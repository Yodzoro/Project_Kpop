from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Company, Member, Group, SoloArtist, MonthlyRating, SocialPlatform, SocialLink
# Register your models here.


class SocialLinkInline(GenericTabularInline):
    model = SocialLink
    extra = 1


class MemberAdmin(admin.ModelAdmin):
    inlines = [SocialLinkInline]


class GroupAdmin(admin.ModelAdmin):
    inlines = [SocialLinkInline]


class SoloArtistAdmin(admin.ModelAdmin):
    inlines = [SocialLinkInline]


class SocialPlatformAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']


admin.site.register(Company)
admin.site.register(Member, MemberAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(SoloArtist, SoloArtistAdmin)
admin.site.register(MonthlyRating)
admin.site.register(SocialPlatform, SocialPlatformAdmin)