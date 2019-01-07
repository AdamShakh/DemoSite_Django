from django.contrib.auth.models import User
from django.shortcuts import render
import datetime
from first.models import CalcHistory

# Create your views here.

# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip
def get_client_http_host(request):
    return 'http://' + request.META.get('HTTP_HOST')

def get_client_LOGNAME_OSname(request):
    return [request.META.get('LOGNAME'), request.META.get('DESKTOP_SESSION')]


def index_page(request):
    title = 'Курс "Промышленное программирование"'
    lines = []
    lines.append('Занятие №12')
    lines.append('Тема: "Знакомство с Django"')
    d1, d2, d3 = (lambda d: map(str, [d.day, d.month, d.year]))(datetime.datetime.now())
    lines.append('Сегодня - {}.{}.{}'.format(d1, d2, d3))

    btns = {}
    btns['Заhадка'] = get_client_http_host(request) + '/riddle'
    btns['Ответо'] = get_client_http_host(request) + '/answer'
    btns['Калбкулято'] = get_client_http_host(request) + '/calc'

    author_name = "Adam"
    page_count = 1
    curreny_date = datetime.datetime.now()
    context = {
        'author': author_name,
        'title': title,
        'icon': './static/index_icon.png',
        'pcount': page_count,
        'date': curreny_date,
        'lines': lines,
        'riddleSite': btns['Заhадка'],
        'answerSite': btns['Ответо'],
        'calcSite': btns['Калбкулято'],
        'multiplytableSite': get_client_http_host(request) + '/multiply',
        'indexSite': get_client_http_host(request),
        'menuSite': get_client_http_host(request) + '/menu',
        'btns': btns
    }

    # print('----->', get_client_ip(request))
    return render(request, 'index.html', context)

def menu_page(request):

    allSites = {}
    allSites['hлавная'] = get_client_http_host(request)
    allSites['Заhадка'] = get_client_http_host(request) + '/riddle'
    allSites['Ответо'] = get_client_http_host(request) + '/answer'
    allSites['Калбкулято'] = get_client_http_host(request) + '/calc'
    allSites['Админка'] = get_client_http_host(request) + '/admin'
    allSites['прост'] = get_client_http_host(request) + '/idk'
    allSites['таблицаУмножения'] = get_client_http_host(request) + '/multiply'

    context = {
        'title': 'Menu of all Site',
        'indexSite': allSites['hлавная'],
        'answerSite': allSites['Ответо'],
        'riddleSite': allSites['Заhадка'],
        'calcSite': allSites['Калбкулято'],
        'idkSite': allSites['прост'],
        'adminSite': allSites['Админка'],
        'multiplytableSite': allSites['таблицаУмножения'],
        'allSitesbtn': allSites
    }

    return render(request, 'menu.html', context)

def calculator_page(request):
    context = {
        'title': 'калбкулято - демосайт',
        'icon': './static/calc_icon.png',
        'header': 'страница калькулятора',
        'indexSite': get_client_http_host(request)
    }

    # current_user = User.objects.get(username='LODE')
    current_user = request.user
    history = CalcHistory.objects.all()  ###
    # history = CalcHistory.objects.filter(author=current_user)  ###
    context['history'] = history

    try:
        first_value = request.GET.get('a', '0')   # /?a=36&b=18
        second_value= request.GET.get('b', '0')



        if first_value.isdigit() and second_value.isdigit():
            result = int(first_value) + int(second_value)

            record = CalcHistory(
                date=datetime.datetime.now(),
                first=first_value,
                second=second_value,
                result=result,
                author=current_user
            )
            record.save()

            context.update({
                'a': first_value,
                'b': second_value,
                'c': result,
            })
        else:
            context['error'] = 'вы не цыфру целую ввёло в поле , а это _{}_ и это _{}_'.format(first_value, second_value)

    except Exception:
        context['error'] = 'вы чё , вы не ввело по форме - ?a=0&b=0'

    return render(request, 'calc.html', context)

def multiply_page(request):

    context = {
        'title': 'Таблица Умножения',
        'number': int(1),
        'indexSite': get_client_http_host(request)
    }

    try:
        number = int(request.GET.get('number', int(1)))  # /?number=9
        vals = [number * j for j in range(1, 11)]
        context['number'] = number
        context['vals'] = vals

    except Exception:
        vals = [context['number'] * i for i in range(1, 11)]
        context['vals'] = vals


    return render(request, 'multiply.html', context)

def riddle(request):
    context = {
        'title': 'Загадка собсно :',
        'icon': './static/riddle_icon.png',
        'riddle': "главная вещь вокруг которой крутится культура { "
                  ""
                  "( str( аббревиатура имени музыкальной группы того человека , "
                  "который вместе с ещё одним челом делали большую часть крутых ost для фильма про челевека , "
                  "который сделал популярный продукт , который был частично скопирован человеком у , которого фамилия такаяже , "
                  "как у улицы , которая проходит мимо стадиона , который находится около станции метро , "
                  "которая находится около отделения МШП в , котором проходят подготовки к ЕГЭ ) + 'a' ) "
                  "--> ru --> "
                  "протяжонность в минутах всех серий этого сериала + 10"
                  " }",
        'answerSite': get_client_http_host(request) + '/answer',
        'indexSite': get_client_http_host(request)


    }
    return render(request, 'riddle.html', context)

def answer(request):
    context = {
        'title': 'Ответ на загадку :',
        'icon': './static/answer_icon.png',
        'answer': 'марихуанна',
        'riddleSite': get_client_http_host(request) + '/riddle',
        'indexSite': get_client_http_host(request)
    }
    return render(request, 'answer.html', context)