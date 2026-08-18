from django.contrib import admin

from App.models import userProfile,Block,BlockAmount,Policy,Notification

# Register your models here.
admin.site.register(userProfile)
admin.site.register(Block)
admin.site.register(BlockAmount)
admin.site.register(Policy)
admin.site.register(Notification)