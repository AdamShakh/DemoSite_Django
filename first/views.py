from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import datetime
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, SquadEquation

from first.forms import CalcForm
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
        'riddleSite': get_client_http_host(request) + '/riddle',
        'answerSite': get_client_http_host(request) + '/answer',
        'calcSite': get_client_http_host(request) + '/calc',
        'squadEqiual': get_client_http_host(request) + '/squadequal',
        'multiplytableSite': get_client_http_host(request) + '/multiply',
        'indexSite': get_client_http_host(request),
        'menuSite': get_client_http_host(request) + '/menu',
    }

    # print('----->', get_client_ip(request))
    return render(request, 'index.html', context)

def menu_page(request):

    allSites = {}
    allSites['hлавная'] = get_client_http_host(request)
    allSites['Заhадка'] = get_client_http_host(request) + '/riddle'
    allSites['Ответо'] = get_client_http_host(request) + '/answer'
    allSites['Калбкулято'] = get_client_http_host(request) + '/calc'
    allSites['КвадратноеУравнение'] = get_client_http_host(request) + '/squadequal'
    allSites['Админка'] = get_client_http_host(request) + '/admin'
    allSites['прост'] = get_client_http_host(request) + '/idk'
    allSites['таблицаУмножения'] = get_client_http_host(request) + '/multiply'

    context = {
        'title': 'Menu of all Site',
        'indexSite': allSites['hлавная'],
        'answerSite': allSites['Ответо'],
        'riddleSite': allSites['Заhадка'],
        'calcSite': allSites['Калбкулято'],
        'squadEqiual': allSites['КвадратноеУравнение'],
        'idkSite': allSites['прост'],
        'adminSite': allSites['Админка'],
        'multiplytableSite': allSites['таблицаУмножения'],
        'allSitesbtn': allSites
    }

    return render(request, 'menu.html', context)

@login_required(login_url='/login/')
def calculator_page(request):
    context = {
        'title': 'калбкулято - демосайт',
        'icon': './static/calc_icon.png',
        'header': 'страница калькулятора',
        'indexSite': get_client_http_host(request)
    }

    # current_user = User.objects.get(username='LODE')
    current_user = request.user

    if request.method == 'POST':

        form = CalcForm(request.POST)
        first_value = form.data['first']  # first  second  это имена которые в form
        second_value = form.data['second']
        if form.is_valid():  # проверка на валидность на сервере
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
            print('ooops ? we"ve got problems')
            context['error'] = True

        context['cform'] = form

    else:
        context['cform'] = CalcForm()

    return render(request, 'calc.html', context)

"""def calculator_page(request):
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

    return render(request, 'calc.html', context)"""

def squadequal(a, b, c):
    des = b ** 2 - 4 * a * c

    if a == 0:
        return 'zeroerror'
    elif des > 0:
        import math
        x1 = (-b + math.sqrt(des)) / (2 * a)
        x2 = (-b - math.sqrt(des)) / (2 * a)
        return (x1, x2)
    elif des == 0:
        x = -b / (2 * a)
        return ([x])
    else:
        return (False)


@login_required(login_url='/login/')
def squadEqual(request):
    context = {
        'title': 'вычисление корней у квадратного уравнения',
        'icon': './static/calc_icon.png',
        'header': 'страница Квадратного уравнения , мы поможем вам',
        'indexSite': get_client_http_host(request)
    }
    # current_user = User.objects.get(username='LODE')
    context['user'] = request.user


    if request.method == 'POST':

        form = SquadEquation(request.POST)
        first_value = int(form.data['a'])  # first  second  это имена которые в form
        second_value = int(form.data['b'])
        third_value = int(form.data['c'])

        if form.is_valid():  # проверка на валидность на сервере
            xexes = squadequal(float(first_value), float(second_value), float(third_value))


            if (xexes == False):
                context.update({
                    'a': first_value,
                    'b': second_value,
                    'c': third_value,
                    'type': 'none'
                })
            elif (len(xexes) == 2):
                x1 = xexes[0]
                x2 = xexes[1]
                context.update({
                    'a': first_value,
                    'b': second_value,
                    'c': third_value,
                    'x1': round(x1, 5),
                    'x2': round(x2, 5),
                    'type': 'two'
                })
            elif (len(xexes) == 1):
                x = xexes[0]
                context.update({
                    'a': first_value,
                    'b': second_value,
                    'c': third_value,
                    'x': round(x, 5),
                    'type': 'one'
                })
            elif (xexes == 'zeroerror'):
                context.update({
                    'a': first_value,
                    'b': second_value,
                    'c': third_value,
                    'type': 'zeroerror'
                })
            else:
                context.update({
                    'a': first_value,
                    'b': second_value,
                    'c': third_value,
                    'type': 'error'
                })


        else:
            print('ooops ? we"ve got problems')
            context['error'] = True

        context['cform'] = form

    else:
        context['cform'] = SquadEquation()


    return render(request, 'squadEquation.html', context)


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




def signup(request):
    context = {}
    context['title'] = 'SingUp'

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()

    context['form'] = form
    return render(request, 'signup.html', context)


def login(request):
    context = {}
    context['title'] = 'LogIN'

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            fw_username = form.cleaned_data['username']
            fw_password = form.cleaned_data['password']
            user = authenticate(username=fw_username, password=fw_password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    context['form'] = form
    return render(request, 'registration/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('home')

