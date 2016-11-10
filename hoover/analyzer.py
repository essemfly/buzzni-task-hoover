# coding: utf-8

from konlpy.tag import Twitter
from hoover.models import Hoover, Review
from hoover import search
from collections import defaultdict


def get_keyword(doc):
    keywords = []
    pos_tagger = Twitter()
    tokens = pos_tagger.pos(doc, norm=True, stem=True)
    for token in tokens:
        if token[1] == 'Noun':
            keywords.append(token[0])
    return keywords


def get_recommended_hoover(keywords):
    hoover_ids = Hoover.objects.values_list('id', flat=True)
    hoover_scores = {}
    for hoover_id in hoover_ids:
        hoover_scores[hoover_id] = get_hoover_score(hoover_id, keywords)
    return hoover_scores


def get_hoover_score(hoover_id, keywords):
    hoover_score = 0
    pos_tagger = Twitter()
    reviews = Review.objects.filter(product_id_id=hoover_id)
    for review in reviews:
        review_nouns = set(pos_tagger.nouns(review.content))
        for keyword in keywords:
            if keyword in review_nouns:
                hoover_score += review.rating - 3
    return hoover_score


def get_recommended_hoover_by_dict(keywords):
    temp = []
    for keyword in keywords:
        if len(keyword) > 1:
            res = search.search(keyword)
            review_ids = res['hits']['hits'][0]['_source']['review_ids']
            temp.append(get_hoover_score_by_dict(review_ids))
        else:
            pass
    results = {}
    for res in temp:
        results = dsum(results, res)
    return results


def get_hoover_score_by_dict(review_ids):
    hoover_scores = {}
    for review_id in review_ids:
        review = Review.objects.get(id=review_id)
        if review.product_id_id in hoover_scores.keys():
            hoover_scores[review.product_id_id] += review.rating - 3
        else:
            hoover_scores[review.product_id_id] = review.rating - 3
    return hoover_scores


def dsum(*dicts):
    ret = defaultdict(int)
    for d in dicts:
        for k, v in d.items():
            ret[k] += v
    return dict(ret)
