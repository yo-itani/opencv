# -*- coding: utf-8 -*-

import math
import pickle

from bs4 import BeautifulSoup

import color_utils as cu

"""
http://www.tagindex.com/color/color_gradation.html
このページの情報をもとに作成

"""
COLOR_VALUES = 'color_values'
COLORTYPE_NAMES = 'color_names'
COLORTYPE_NAMES_ENG = 'color_names_eng'
COLORTYPE_CODE = 'colortype_code'

COLOR_NAME = 'colorname'
BRIGHTNESS = 'brightness'
VIVIDNESS = 'vividness'
RGB = 'rgb'
BGR = 'bgr'
HSV = 'hsv'
CIELAB = 'cielab'
DIFF = 'diff'

def main():
    create_colortype_pickle('colortype.pickle')

def create_colortype_pickle(picklefile):
    soup = BeautifulSoup(open('color_gradation.html'))
    colorvalues = []
    colornames = {}
    for color_type, tbody in enumerate(soup.find_all('tbody')):
        colornames[color_type] = tbody.find('th').text
        for brightness, tr in enumerate(tbody.find_all('tr')):
            if brightness == 0:
                continue
            for vividness, td in enumerate(tr.find_all('td')):
                color_code = td.text
                if color_code:
                    colorvalue = {COLORTYPE_CODE: color_type,
                                 BRIGHTNESS: brightness,
                                 VIVIDNESS: vividness, }
                    colorvalue[RGB] = cu.rgbstr2rgb(color_code)
                    colorvalue[BGR] = cu.rgb2bgr(colorvalue[RGB])
                    colorvalue[HSV] = cu.bgr2hsv(colorvalue[BGR])
                    colorvalue[CIELAB] = cu.bgr2lab(colorvalue[BGR])
                    colorvalues.append(colorvalue)
    # 日本語が使えないので英語表記を追加
    color_names_eng = {
        0: 'white, black, grey',
        1: 'red',
        2: 'brown, orange',
        3: 'yellow',
        4: 'yellowgreen',
        5: 'green',
        6: 'mediumseagreen',
        7: 'aqua',
        8: 'skyblue',
        9: 'blue',
        10: 'vilet bule',
        11: 'purple',
        12: 'red purple',
    }
    pickle.dump({
                    COLOR_VALUES: colorvalues,
                    COLORTYPE_NAMES: colornames,
                    COLORTYPE_NAMES_ENG: color_names_eng, }, open(picklefile, 'w'))


def get_color(rgb, colortype_data):
    cielab = cu.bgr2lab(cu.rgb2bgr(rgb))
    mindiff = 99999999
    color_values = colortype_data[COLOR_VALUES]
    color_names_eng = colortype_data[COLORTYPE_NAMES_ENG]
    for i, colorvalue in enumerate(color_values):
        ldiff = cielab[0] - colorvalue[CIELAB][0]
        adiff = cielab[1] - colorvalue[CIELAB][1]
        bdiff = cielab[2] - colorvalue[CIELAB][2]
        diff = math.sqrt(ldiff * ldiff + adiff * adiff + bdiff * bdiff)
        if mindiff > diff:
            mindiff_index = i
            mindiff = diff
    colortype_code = color_values[mindiff_index][COLORTYPE_CODE]
    return {COLOR_NAME: color_names_eng[colortype_code],
            RGB: color_values[mindiff_index][RGB],
            BRIGHTNESS: color_values[mindiff_index][BRIGHTNESS],
            VIVIDNESS: color_values[mindiff_index][VIVIDNESS],
            DIFF: mindiff, }


if __name__ == '__main__':
    main()

