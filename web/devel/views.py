from django.shortcuts import render

# Create your views here.

def index(request):
    if 'page' in request.GET:
        page = int(request.GET['page'])
    else:
        page = 1
    if 'type' in request.GET:
        type = request.GET['type']
    else:
        type = 't_shirts'
    context = {
        'page': page,
        'img_num': page - 1,
        'type': type,
    }
    return render(request, 'devel/index.html', context)
