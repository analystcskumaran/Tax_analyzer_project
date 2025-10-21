from django.db import models

class TaxQuery(models.Model):
    income = models.FloatField()
    year = models.IntegerField()
    predicted_tax = models.FloatField()