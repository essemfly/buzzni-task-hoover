# coding: utf-8

from django.core.management.base import BaseCommand
from hoover.models import Review
from konlpy.tag import Twitter
import nltk
from elasticsearch import Elasticsearch


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pos_tagger = Twitter()
        es = Elasticsearch(
            [{'host': 'search-hoover-review-xyvam7y4p25hqc3ivhv2onwmna.ap-northeast-2.es.amazonaws.com', 'port': 80}])
        reviews = Review.objects.all()

        self.stdout.write(self.style.SUCCESS('Total reviews: ' + str(len(reviews))))
        tokens = []
        review_tokens = []

        for review in reviews:
            self.stdout.write(self.style.SUCCESS('Review ..tokenizing : ' + str(review.id)))
            token_per_review = []
            for token in pos_tagger.nouns(review.content):
                # self.stdout.write(self.style.SUCCESS(str(token)))
                token_per_review.append(token)
            tokens += token_per_review
            review_tokens.append([review.id, token_per_review])
        texts = nltk.Text(tokens, name='NMSC')

        for unique_noun in set(texts.tokens):
            self.stdout.write(self.style.SUCCESS('Elasticsearch ..inserting for :' + unique_noun ))
            review_ids = []
            for review_token in review_tokens:
                if unique_noun in review_token[1]:
                    review_ids.append(review_token[0])
            body = {
                'key': unique_noun,
                'review_ids': review_ids
            }
            es.index(index='review', doc_type='noun', body=body)
