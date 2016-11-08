from django.db import models


class Hoover(models.Model):
    nvmid = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    basic_info = models.CharField(max_length=400)
    avg_rating = models.FloatField(default=0)


class Review(models.Model):
    product_id = models.ForeignKey(Hoover, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.IntegerField(default=0)
    pub_date = models.DateTimeField()

