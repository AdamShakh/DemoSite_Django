from django.contrib import admin

from first.models import CalcHistory

admin.site.register(CalcHistory)  #теперь можно смотреть БД через панель admin
