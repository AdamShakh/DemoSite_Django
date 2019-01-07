from django.shortcuts import render

# Create your views here.
def index_page(request):
    author_name = "no"
    page_count = 1

    context = {
        'author': author_name,
        'pcount': page_count
    }


    return render(request, 'index.html', context)