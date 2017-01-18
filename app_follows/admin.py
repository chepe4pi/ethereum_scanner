from django.contrib import admin

from app_follows.models import Follow, EthAccountInfo


class FollowAdmin(admin.ModelAdmin):
    pass


class EthAccountInfoAdmin(admin.ModelAdmin):
    pass


admin.site.register(Follow, FollowAdmin)
admin.site.register(EthAccountInfo, EthAccountInfoAdmin)
