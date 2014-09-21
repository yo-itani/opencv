# -*- coding: utf-8 -*-

import os
from django.shortcuts import render
import modules.analyze_color as ac

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

def create(request):
    if 'page' in request.GET:
        page = int(request.GET['page'])
    else:
        page = 1
    if 'type' in request.GET:
        type = request.GET['type']
    else:
        type = 't_shirts'
    basedir = '/home/thatsping/opencv/develop'
    srcdir = os.path.join(basedir, 'src_img', 'web', type)
    dstdir = os.path.join(basedir, 'img', type)
    ac.main(srcdir, dstdir, page)
    context = {
        'page': page,
        'img_num': page - 1,
        'type': type,
    }
    return render(request, 'devel/index.html', context)
