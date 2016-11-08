# coding: utf-8

from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from hoover.models import Hoover, Review
import datetime
from django.utils import timezone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        review_url = 'http://shopping.naver.com/detail/review_list.nhn'
        hoovers = Hoover.objects.all()
        for hoover in hoovers:
            for i in range(5):
                self.stdout.write(self.style.SUCCESS(getattr(hoover, 'name') + ' : ' + str(i+1) + 'review page loaded'))
                data = {'nvMid': getattr(hoover, 'nvmid'), 'page': i + 1, 'reviewSort': 'accuracy'}
                review_html = BeautifulSoup(requests.post(review_url, data).text, 'lxml')
                reviews = review_html.findAll('li', attrs={'class': 'not_thmb'})
                for review in reviews:
                    review_product_id = hoover
                    review_title = review.find('p').text.split('|')[0]
                    review_content = review.find('div', attrs={'class': 'atc'}).text
                    review_rating = review.find('span', attrs={'class': 'curr_avg'}).find('strong').text
                    review_date = timezone.make_aware(datetime.datetime.strptime(review.find('span', attrs={'class': 'regdate'}).text, '%Y.%m.%d.'), timezone.get_current_timezone())

                    new_review = Review(
                        product_id=review_product_id,
                        title=review_title,
                        content=review_content,
                        rating=review_rating,
                        pub_date=review_date
                    )
                    new_review.save()

