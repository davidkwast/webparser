from django.contrib import admin

from .models import *

# Register your models here.

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('youtube_id', 'title')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('youtube_id','title','channel','publish_date','view_count','likes','dislikes')
    list_filter = ('category',)
    date_hierarchy = 'publish_date'
    raw_id_fields = ('url',)

@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    list_display = ('query','timestamp')

@admin.register(VideoSearch)
class VideoSearchAdmin(admin.ModelAdmin):
    list_display = ('video_id','search_id','rank')
