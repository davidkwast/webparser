from django.db import models

from core import models as core_models

# Create your models here.

class Channel(models.Model):
    youtube_id = models.CharField(max_length=32, unique=True, db_index=True)
    title = models.CharField(max_length=256, db_index=True)
    
    def __str__(self):
        return self.title

class Video(models.Model):
    youtube_id = models.CharField(max_length=32, unique=True, db_index=True)
    title = models.CharField(max_length=256, db_index=True)
    publish_date = models.DateField(db_index=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, db_index=True)
    category = models.CharField(max_length=256, db_index=True)
    license = models.CharField(max_length=265, db_index=True)
    view_count = models.IntegerField(db_index=True)
    likes = models.IntegerField(db_index=True)
    dislikes = models.IntegerField(db_index=True)
    description_text = models.TextField()
    description_html = models.TextField()
    url = models.OneToOneField(core_models.URL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

class Search(models.Model):
    query = models.CharField(max_length=256)
    timestamp = models.DateTimeField()
    videos = models.ManyToManyField(Video, through='VideoSearch')

class VideoSearch(models.Model):
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE)
    search_id = models.ForeignKey(Search, on_delete=models.CASCADE)
    rank = models.IntegerField()
