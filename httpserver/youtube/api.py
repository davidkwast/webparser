from webparser.youtube import api

from django.db import transaction
from django.utils import timezone

from . import models
from core import models as core_models

def video__get(youtube_id):
    try:
        return models.Video.objects.get(youtube_id = youtube_id)
    except models.Video.DoesNotExist:
        return None

def channel__get_or_create(youtube_id, title):
    obj, create = models.Channel.objects.get_or_create(
        youtube_id = youtube_id,
        defaults = {
            'title': title,
        }
    )
    return obj

def search(query, limit):
    timestamp = timezone.now()
    videos_id = api.search(query, limit)
    with transaction.atomic():
        search = models.Search.objects.create(
            query = query,
            timestamp = timestamp,
        )
        for index, video_id in enumerate(videos_id):
            try:
                if not video__get(video_id):
                    rank = index + 1
                    d = api.get_video_info(video_id)
                    channel = channel__get_or_create(d['user_id'], d['user_username'])
                    video = models.Video.objects.create(
                        youtube_id = video_id,
                        title = d['title'],
                        publish_date = d['publish_date'],
                        channel = channel,
                        category = d['category'],
                        license = d['license'],
                        view_count = d['view_count'],
                        likes = d['likes'],
                        dislikes = d['dislikes'],
                        description_text = d['description_text'],
                        description_html = d['description_html'],
                        url = core_models.URL.objects.create(
                            url = d['_url'],
                            timestamp = timestamp,
                            content = d['_response_obj'].html.html
                        )
                    )
                    models.VideoSearch.objects.create(
                        video_id = video,
                        search_id = search,
                        rank = rank,
                    )
            except Exception:
                print('Video ID: {}'.format(video_id))
                raise
