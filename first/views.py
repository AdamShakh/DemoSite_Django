from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from datetime import datetime
from django.utils.timezone import now, pytz
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CalcForm, SignUpForm, SquadEquation, str2wordsForm
from first.models import CalcHistory, StrParsHistory


# Create your views here.

# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip
def get_client_http_host(request):
    return 'http://' + request.META.get('HTTP_HOST') if request else 'http://127.0.0.1:8000'


def get_client_LOGNAME_OSname(request):
    return [request.META.get('LOGNAME'), request.META.get('DESKTOP_SESSION')]


def get_base_context(request=False):
    context = {
        'author': 'Adam',
        'date': datetime.now(tz=pytz.timezone("Europe/Moscow")),
        'current_user': request.user if request else '',

        'indexSite': get_client_http_host(request),

        'riddleSite': get_client_http_host(request) + '/riddle',
        'answerSite': get_client_http_host(request) + '/answer',

        'calcSite': get_client_http_host(request) + '/calc',
        'squadEqiual': get_client_http_host(request) + '/squadequal',
        'multiplytableSite': get_client_http_host(request) + '/multiply',
        'str2words': get_client_http_host(request) + '/str2words',
        'str_history': get_client_http_host(request) + '/str_history',

        'menuSite': get_client_http_host(request) + '/menu',
        'signup': get_client_http_host(request) + '/signup',
        'login': get_client_http_host(request) + '/login',
        'logout': get_client_http_host(request) + '/logout',
        'adminSite': get_client_http_host(request) + '/admin',
        'idkSite': get_client_http_host(request) + '/idk',

    }

    return context


def index_page(request):
    context = get_base_context(request)
    context.update({
        'title': 'Курс "Промышленное программирование"',
        'header': 'Главная',
        'icon': './static/index_icon.png',
    })

    lines = []
    lines.append('Занятие №12')
    lines.append('Тема: "Знакомство с Django"')
    d1, d2, d3 = (lambda d: map(str, [d.day, d.month, d.year]))(datetime.now())
    lines.append('Сегодня - {}.{}.{}'.format(d1, d2, d3))
    if str(request.user) != 'AnonymousUser':
        lines.append('Здравствуйте ' + str(request.user))
    context['lines'] = lines

    return render(request, 'index.html', context)


def menu_page(request):
    context = get_base_context(request)
    context.update({
        'title': 'Menu of all pages',
        'header': 'Menu',
        'icon': '',
    })
    return render(request, 'menu.html', context)


@login_required(login_url='/login/')
def calculator_page(request):
    context = get_base_context(request)
    context.update({
        'title': 'калбкулято - демосайт',
        'header': 'страница калькулятора',
        'icon': './static/calc_icon.png',
    })

    # current_user = User.objects.get(username='LODE')
    current_user = request.user
    history = CalcHistory.objects.all()
    # history = CalcHistory.objects.filter(author=current_user)  ###
    context['history'] = history

    if request.method == 'POST':

        form = CalcForm(request.POST)
        first_value = form.data['first']  # first  second  это имена которые в form
        second_value = form.data['second']
        if form.is_valid():  # проверка на валидность на сервере
                # сдесь на соответствие пришедшей формы (из html) (построенно на основе forms)
                # с созданной на сервере формой (также на основе forms)
            result = int(first_value) + int(second_value)
            record = CalcHistory(
                date=datetime.now(),
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
            context['error'] = 'form не is_valid'

        context['cform'] = form

    else:
        context['cform'] = CalcForm()
        context['error'] = 'не POST'

    # try:
    #     first_value = request.GET.get('a', '0')   # /?a=36&b=18
    #     second_value= request.GET.get('b', '0')
    #
    #     if first_value.isdigit() and second_value.isdigit():
    #         result = int(first_value) + int(second_value)
    #
    #         record = CalcHistory(
    #             date=datetime.now(),
    #             first=first_value,
    #             second=second_value,
    #             result=result,
    #             author=current_user
    #         )
    #         record.save()
    #
    #         context.update({
    #             'a': first_value,
    #             'b': second_value,
    #             'c': result,
    #         })
    #     else:
    #         context['error'] = 'вы не цыфру целую ввёло в поле , а это _{}_ и это _{}_'.format(first_value, second_value)
    #
    # except Exception:
    #     context['error'] = 'вы чё , вы не ввело по форме - ?a=0&b=0'

    return render(request, 'calc.html', context)


def squadEqualXes(a, b, c):
    des = b ** 2 - 4 * a * c

    if a == 0:
        return {'type': 'zeroerror'}
    elif des > 0:
        import math
        x1 = (-b + math.sqrt(des)) / (2 * a)
        x2 = (-b - math.sqrt(des)) / (2 * a)
        return {'type': 'two', 'value': [x1, x2]}
    elif des == 0:
        x = -b / (2 * a)
        return {'type': 'one', 'value': [x]}
    elif des < 0:
        return {'type': 'no'}


@login_required(login_url='/login/')
def squadEqual(request):
    context = get_base_context(request)
    context.update({
        'title': 'вычисление корней у квадратного уравнения',
        'header': 'страница Квадратного уравнения , мы поможем вам',
        'icon': './static/calc_icon.png',
    })

    if request.method == 'POST':

        form = SquadEquation(request.POST)
        first_value = int(form.data['a'])  # first  second  это имена которые в form
        second_value = int(form.data['b'])
        third_value = int(form.data['c'])

        if form.is_valid():  # проверка на валидность на сервере
            xexes = squadEqualXes(float(first_value), float(second_value), float(third_value))
            context.update({
                'a': first_value,
                'b': second_value,
                'c': third_value,
            })

            if xexes['type'] == 'two':
                x1 = xexes['value'][0]
                x2 = xexes['value'][1]
                context.update({
                    'x1': round(x1, 5),
                    'x2': round(x2, 5),
                    'type': 'two'
                })
            elif xexes['type'] == 'one':
                x = xexes['value'][0]
                context.update({
                    'x': round(x, 5),
                    'type': 'one'
                })
            elif xexes['type'] == 'zeroerror':
                context.update({
                    'type': 'zeroerror'
                })
            elif xexes['type'] == 'no':
                context.update({
                    'type': 'no'
                })

        else:
            context['error'] = 'form не is_valid'

        context['cform'] = form

    else:
        context['cform'] = SquadEquation()
        context['error'] = 'не POST'

    return render(request, 'squadEquation.html', context)


@login_required(login_url='/login/')
def str2words(request):
    context = get_base_context(request)
    context.update({
        'title': 'Парсинг Строки',
        'header': 'Форма Джедая',
        'icon': './static/calc_icon.png',
    })

    if request.method == 'POST':

        form = str2wordsForm(request.POST)
        stroka0 = form.data['stroka']

        if form.is_valid():  # проверка на валидность на сервере
            stroka = stroka0.split(" ")
            allWrd = [i for i in stroka if i.isalnum() and not i.isdigit()]
            allNum = [i for i in stroka if i.isdigit()]
            cntWrd = len(allWrd)
            cntNum = len(allNum)

            context.update({
                'countWords': cntWrd,
                'countNumbers': cntNum,
                'allWords': allWrd,
                'allNumbers': allNum,
            })

            # time = str(datetime.now())
            record = StrParsHistory(
                date=datetime.now(tz=pytz.timezone("Europe/Moscow")).date(),  # ''.join([(i if i != '-' else ' ') for i in time[:10]]),
                time=str(datetime.now(tz=pytz.timezone("Europe/Moscow")).time())[0:8],  # str(int(time[11] + time[12]) + 3) + ''.join([i for i in time[13:19]]),
                stroka0=stroka0,
                countWords=cntWrd,
                countNumbers=cntNum,
                userWas=request.user
            )
            record.save()

        else:
            context['error'] = 'form не is_valid'

        context['cform'] = form

    else:
        context['cform'] = str2wordsForm()
        context['error'] = 'не POST'

    return render(request, 'str2words.html', context)


@login_required(login_url='/login/')
def str_history(request):
    context = get_base_context(request)
    context.update({
        'title': 'История Парсинга Строк',
        'header': 'История Парсинга Строк',
        'icon': '',
        'history': StrParsHistory.objects.all()
    })

    return render(request, 'str_history.html', context)


def multiply_page(request):
    context = get_base_context(request)
    context.update({
        'title': 'Таблица Умножения',
        'number': int(1),
    })

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
    context = get_base_context(request)
    context.update({
        'title': 'Загадка собсно',
        'header': 'Загадка',
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
    })
    return render(request, 'riddle.html', context)


def answer(request):
    context = get_base_context(request)
    context.update({
        'title': 'Ответ на загадку',
        'header': 'Ответ',
        'icon': './static/answer_icon.png',
        'answer': 'марихуанна',
    })
    return render(request, 'answer.html', context)


def signup(request):
    context = get_base_context(request)
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
    context = get_base_context(request)
    context['title'] = 'LogIN'

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
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

