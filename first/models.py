from django.contrib.auth.models import User
from django.db import models


class CalcHistory(models.Model):
    date = models.DateTimeField()
    first = models.IntegerField()
    second = models.IntegerField()
    result = models.IntegerField()
    author = models.ForeignKey(to=User, default=1, on_delete=models.CASCADE)
                                                # on_delete что делать если посльзователь будет удалён ,, мусор

class StrParsHistory(models.Model):
    date = models.DateField()
    time = models.CharField(max_length=8)
    stroka0 = models.CharField(max_length=255)
    countWords = models.IntegerField()
    countNumbers = models.IntegerField()
    userWas = models.ForeignKey(to=User, default=1, on_delete=models.CASCADE)