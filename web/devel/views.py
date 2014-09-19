from django.shortcuts import render

# Create your views here.

def index(request):
    if 'page' in request.GET:
        page = int(request.GET['page'])
    else:
        page = 1
    context = {
        'page': page,
        'img_num': page - 1,
    }
    return render(request, 'devel/index.html', context)
