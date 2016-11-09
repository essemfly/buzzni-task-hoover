# coding: utf-8

from konlpy.tag import Twitter
from hoover.models import Hoover, Review


def get_keyword(doc):
    keywords = []
    pos_tagger = Twitter()
    tokens = pos_tagger.pos(doc, norm=True, stem=True)
    for token in tokens:
        if token[1] == 'Noun':
            keywords.append(token[0])
    return keywords


def get_recommended_hoover(keywords):
    pos_tagger = Twitter()
    hoover_ids = Hoover.objects.values_list('id', flat=True)
    hoover_scores = {}
    for hoover_id in hoover_ids:
        hoover_score = 0
        reviews = Review.objects.filter(product_id_id=hoover_id)
        for review in reviews:
            review_nouns = set(pos_tagger.nouns(review.content))
            for keyword in keywords:
                if keyword in review_nouns:
                    hoover_score += review.rating-3
        hoover_scores[hoover_id] = hoover_score
    return hoover_scores

