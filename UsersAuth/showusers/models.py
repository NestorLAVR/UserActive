from django.db import models
class FastProd_DATA(models.Model):
    date = models.CharField(max_length=40, default='')
    DAU = models.IntegerField()
    MAU = models.IntegerField()
    prevDAU = models.IntegerField()
    prevMAU = models.IntegerField()

    def __str__(self):
        return self.date