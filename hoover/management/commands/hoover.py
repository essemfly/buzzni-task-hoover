# coding: utf-8

from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from hoover.models import Hoover

DOMAIN = 'http://shopping.naver.com'


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        index = 1
        review_urls = []
        product_per_page = 80
        page_total = 5

        for i in range(page_total):
            url = DOMAIN + '/search/all.nhn?query=청소기&pagingIndex=' + str(i + 1) + '&pagingSize=' + str(
                product_per_page) + '&productSet=total'
            lxml_code = get_lxml_code(url)
            for item in lxml_code.findAll('div', attrs={'class': 'info'}):
                review_section = item.find('a', attrs={'class': 'graph'})
                if hasattr(review_section, 'get'):
                    product_link = review_section.get('href')
                    if product_link.startswith('/detail'):
                        index += 1
                        review_urls.append(product_link)
                        self.stdout.write(self.style.SUCCESS('Successfully Crawlling product' + str(index)))

        for url in review_urls:
            lxml_code = get_lxml_code(DOMAIN + url)
            product_summary = lxml_code.find('div', attrs={'id': 'summary_info'})
            product_detail_summary = lxml_code.find('div', attrs={'class': 'detail_summary'})

            product_nv_mid = url.split('nv_mid=')[1].split('&')[0]
            product_name = product_summary.find('h2').text
            product_rating = product_summary.find('span', attrs={'class': 'gpa_star'}).find('span').get('style').split(':')[1]
            product_information = product_summary.find('div', attrs={'class': 'tit'}).text.replace('\n', '').replace('|신고하기', '')
            product_price = product_detail_summary.find('span', attrs={'class': 'low_price'}).find('em').text.replace(',', '')

            self.stdout.write(self.style.SUCCESS('Crawling product: ' + product_name))

            new_product = Hoover(
                nvmid=product_nv_mid,
                name=product_name,
                price=int(product_price),
                basic_info=product_information,
                avg_rating=float(product_rating.strip('%')),
            )
            new_product.save()

def get_lxml_code(url):
    return BeautifulSoup(requests.get(url).text, 'lxml')
