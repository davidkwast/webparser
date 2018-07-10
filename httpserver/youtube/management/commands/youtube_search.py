from django.core.management.base import BaseCommand, CommandError

from youtube.api import search


class Command(BaseCommand):
    help = 'Searches in youtube and records in database'

    def add_arguments(self, parser):
        parser.add_argument('query')
        parser.add_argument('limit', type=int)
    
    def handle(self, *args, **options):
        query = options['query']
        limit = options['limit']
        
        search(query, limit)
        
        self.stdout.write(self.style.SUCCESS('OK'))
