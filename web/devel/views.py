# -*- coding: utf-8 -*-

import os
from .models import Image
from django.shortcuts import render
import modules.analyze_color_devel as ac

from opencv_config import BASE_DIR
from tools.utils import get_related_path
# Create your views here.
import csv
CLUSTER_DATA = []
for row in csv.reader(open('/home/thatsping/opencv/develop/bag_of_features/data/cluster2.tsv'), delimiter='\t'):
    CLUSTER_DATA.append(row)

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
    return render(request, 'devel/devel.html', context)

def cluster(request):
    if 'num' in request.GET:
        num = int(request.GET['num'])
    else:
        num = 1
    if 'page' in request.GET:
        page = int(request.GET['page'])
    else:
        page = 1
    if num >= len(CLUSTER_DATA):
        num = 1
    if page >= len(CLUSTER_DATA[num]):
        page = 1
    img = get_related_path(BASE_DIR, CLUSTER_DATA[num][page])
    context = {
        'num': num,
        'page': page,
        'img': img,
    }
    return render(request, 'devel/cluster.html', context)

def check_image(request, page=1):
    if 'status' in request.GET:
        _change_status(request, page)
    image = Image.objects.get(id=page)
    context = {
        'image': image,
        'image_file': image.get_image_path(),
        'url': request.path,
    }
    return render(request, 'devel/show_bing_images.html', context)

def _change_status(request, page):
    if 'status' in request.GET:
        status = request.GET['status']
        if status.isdigit():
            status = int(status)
            prev_page = int(page) - 1
            if prev_page < 1:
                prev_page = 1
            prev_image = Image.objects.get(id=prev_page)
            prev_image.change_status(status)
