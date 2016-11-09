# coding: utf-8

from django.core.management.base import BaseCommand
from hoover.models import Review
from konlpy.tag import Twitter
from pprint import pprint

pos_tagger = Twitter()
def tokenize(doc):
    return ['/'.join(t) for t in pos_tagger.pos(doc, norm=True, stem=True)]

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        high_reviews = Review.objects.filter(rating__gte=5)
        low_reviews = Review.objects.filter(rating__lte=3)

        high_tokens = [(tokenize(review.content), review.product_id_id) for review in high_reviews]
        low_tokens = [(tokenize(review.content), review.product_id_id) for review in low_reviews]

