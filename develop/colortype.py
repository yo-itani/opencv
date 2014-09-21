# -*- coding: utf-8 -*-

import csv
import math
import numpy as np
import pickle

#from bs4 import BeautifulSoup

import color_utils as cu

"""
http://www.tagindex.com/color/color_gradation.html
このページの情報をもとに作成

"""
COLOR_VALUES = 'color_values'
COLORTYPE_NAMES = 'color_names'
COLORTYPE_NAMES_ENG = 'color_names_eng'
COLORTYPE_CODE = 'colortype_code'

INDEX = 'index'
COLOR_NAME = 'colorname'
BRIGHTNESS = 'brightness'
VIVIDNESS = 'vividness'
RGB = 'rgb'
BGR = 'bgr'
HSV = 'hsv'
CIELAB = 'cielab'
DIFF = 'diff'

def main():
    pass
    #create_colortype_pickle('colortype.pickle')

#def create_colortype_pickle(picklefile):
#    soup = BeautifulSoup(open('color_gradation.html'))
#    colorvalues = []
#    colornames = {}
#    for color_type, tbody in enumerate(soup.find_all('tbody')):
#        colornames[color_type] = tbody.find('th').text
#        for brightness, tr in enumerate(tbody.find_all('tr')):
#            if brightness == 0:
#                continue
#            for vividness, td in enumerate(tr.find_all('td')):
#                color_code = td.text
#                if color_code:
#                    colorvalue = {COLORTYPE_CODE: color_type,
#                                 BRIGHTNESS: brightness,
#                                 VIVIDNESS: vividness, }
#                    colorvalue[RGB] = cu.rgbstr2rgb(color_code)
#                    colorvalue[BGR] = cu.rgb2bgr(colorvalue[RGB])
#                    colorvalue[HSV] = cu.bgr2hsv(colorvalue[BGR])
#                    colorvalue[CIELAB] = cu.bgr2lab(colorvalue[BGR])
#                    colorvalues.append(colorvalue)
#    # 日本語が使えないので英語表記を追加
#    color_names_eng = {
#        0: 'white, black, gray',
#        1: 'red',
#        2: 'brown, orange',
#        3: 'yellow',
#        4: 'yellowgreen',
#        5: 'green',
#        6: 'mediumseagreen',
#        7: 'aqua',
#        8: 'skyblue',
#        9: 'blue',
#        10: 'vilet bule',
#        11: 'purple',
#        12: 'red purple',
#    }
#    pickle.dump({
#                    COLOR_VALUES: colorvalues,
#                    COLORTYPE_NAMES: colornames,
#                    COLORTYPE_NAMES_ENG: color_names_eng, }, open(picklefile, 'w'))


def load_tsv(tsvfile):
    colorvalues = []
    for row in csv.reader(open(tsvfile), delimiter='\t'):
        # #で始まる行をスキップ
        if row[0].startswith('#'):
            continue
        index = row[0]
        rgb = cu.rgbstr2rgb(row[1])
        bgr = cu.rgb2bgr(rgb)
        color_name = row[2]
        brightness = int(row[3])
        vividness = int(row[4])
        colorvalues.append({
            INDEX: index,
            RGB: rgb,
            COLOR_NAME: color_name,
            BRIGHTNESS: brightness,
            VIVIDNESS: vividness,
            BGR: bgr,
            HSV: cu.bgr2hsv(bgr),
            CIELAB: cu.bgr2lab(bgr),
        })
    return colorvalues

def create_tsv(dic, tsvfile):
    color_values = dic[COLOR_VALUES]
    color_names_eng = dic[COLORTYPE_NAMES_ENG]
    writer = csv.writer(open(tsvfile, 'w'), delimiter='\t')
    for i, colorvalue in enumerate(color_values):
        row = []
        row.append(str(i))
        row.append(str(colorvalue[RGB]))
        row.append(color_names_eng[colorvalue[COLORTYPE_CODE]])
        row.append(str(colorvalue[BRIGHTNESS]))
        row.append(str(colorvalue[VIVIDNESS]))
        writer.writerow(row)


def get_color_devel(rgb, colors):
    NUM_VALS = 10
    bgr = cu.rgb2bgr(rgb)
    cielab = cu.bgr2lab(bgr)
    #hsv = cu.bgr2hsv(bgr)
    mindiff_indexes = np.array([-1] * NUM_VALS)
    mindiffs = np.array([9999999] * NUM_VALS)
    for i, colorvalue in enumerate(colors):
        diff = _get_diff(cielab, colorvalue[CIELAB])
        #diff = _get_diff(rgb, colorvalue[RGB])
        #diff = _get_diff(hsv, colorvalue[HSV])
        bigger = mindiffs[(mindiffs > diff)]
        num_bigger = len(bigger)
        if num_bigger:
            interrupt_index = NUM_VALS - num_bigger
            mindiffs[interrupt_index + 1:] = mindiffs[:-(interrupt_index + 1)]
            mindiffs[interrupt_index] = diff
            mindiff_indexes[interrupt_index + 1:] = mindiff_indexes[:-(interrupt_index + 1)]
            mindiff_indexes[interrupt_index] = i
    mindiff_index = mindiff_indexes[0]
    mindiff = mindiffs[0]
    for i, index in enumerate(mindiff_indexes):
        if colors[index][COLOR_NAME] != 'white, black, gray':
            mindiff_index = mindiff_indexes[i]
            mindiff = mindiffs[i]
            break
    rgbs = [colors[index][RGB] for index in mindiff_indexes[:9]]
    return {
            INDEX: colors[mindiff_index][INDEX],
            COLOR_NAME: colors[mindiff_index][COLOR_NAME],
            #RGB: colors[mindiff_index][RGB],
            RGB: rgbs,
            BRIGHTNESS: colors[mindiff_index][BRIGHTNESS],
            VIVIDNESS: colors[mindiff_index][VIVIDNESS],
            DIFF: mindiff, }

def _get_diff(vals1, vals2):
    sum_diff = 0
    for i, (val1, val2) in enumerate(zip(vals1, vals2)):
        sum_diff += (val1 - val2) * (val1 - val2)
    return math.sqrt(sum_diff)


if __name__ == '__main__':
    #dic = pickle.load(open('colortype.pickle'))
    tsvfile = 'colortype.org.tsv'
    #create_tsv(dic, tsvfile)
    for val in load_tsv(tsvfile):
        print val[INDEX], val[COLOR_NAME], val[RGB], val[CIELAB]
    #main()

