# -*- coding: utf-8 -*-

import os
import math
import pickle

import cv2
import numpy as np

import color_pickle as cp
import color_utils as cu
import colortype

SCRIPT_DIR = os.path.dirname(__file__)
WIDTH = 200
REF_COLOR_SIZE = 10
RADIUS = 5
CANNY_THRESHOLD1 = 5
CANNY_THRESHOLD2 = 25
#VIRTICAL = 0
#HORIZONTAL = 1
#DELETE_RATE = 20.0

# 以下BGR形式
CENTER_CIRCLE_COLOR = (255, 255, 0)
TOP_LEFT_CIRCLE_COLOR = (0, 0, 255)
TOP_RIGHT_CIRCLE_COLOR = (0, 255, 0)
BOTTOM_LEFT_CIRCLE_COLOR = (255, 0, 0)
BOTTOM_RIGHT_CIRCLE_COLOR = (255, 255, 0)

#BASECOLORS = pickle.load(open('basecolor.pickle'))
#COLORS = pickle.load(open('color.pickle'))
COLORTYPE_DATA = pickle.load(open('colortype.pickle'))

def main():
    pass

def create_color_pick_img(srcfile, dstfile,
                       _get_top_left_right_coordinate,
                       _get_under_left_right_coordinage):
    """ 色取得調査用画像を生成する

    """
    img = cv2.imread(srcfile)
    # 画像縮小取得
    small_img = cu.get_small_img(img, WIDTH)
    small_img_height, small_img_width = small_img.shape[:2]
    # エッジ画像取得
    edge_img = cu.get_edge_img(small_img, CANNY_THRESHOLD1, CANNY_THRESHOLD2)

    rgbs = []
    # センターの色取得
    rgb, origin = cu.pick_center_color(small_img, RADIUS, shift_x=0, shift_y=-0, most_common=3)
    rgbs.append(rgb)
    cv2.circle(small_img, origin, RADIUS, CENTER_CIRCLE_COLOR, 1)

    try:
        # 左下隅、右下隅の色取得
        left_origin, right_origin = _get_under_left_right_coordinage(edge_img, RADIUS)
        rgb, origin = cu.pick_color_circle(small_img, RADIUS, left_origin, most_common=3)
        rgbs.append(rgb)
        cv2.rectangle(small_img,
                      (0, small_img_height - REF_COLOR_SIZE),
                      (REF_COLOR_SIZE, small_img_height), BOTTOM_LEFT_CIRCLE_COLOR, -1)
        cv2.circle(small_img, origin, RADIUS, BOTTOM_LEFT_CIRCLE_COLOR, 1)
        rgb, origin = cu.pick_color_circle(small_img, RADIUS, right_origin, most_common=3)
        rgbs.append(rgb)
        cv2.rectangle(small_img,
                      (small_img_width - REF_COLOR_SIZE, small_img_height - REF_COLOR_SIZE),
                      (small_img_width, small_img_height), BOTTOM_RIGHT_CIRCLE_COLOR, -1)
        cv2.circle(small_img, origin, RADIUS, BOTTOM_RIGHT_CIRCLE_COLOR, 1)

        # 左上、右上の色取得
        left_origin, right_origin = _get_top_left_right_coordinate(edge_img, RADIUS)
        rgb, origin = cu.pick_color_circle(small_img, RADIUS, left_origin, most_common=3)
        rgbs.append(rgb)
        cv2.rectangle(small_img,
                      (0, 0),
                      (REF_COLOR_SIZE, REF_COLOR_SIZE), TOP_LEFT_CIRCLE_COLOR, -1)
        cv2.circle(small_img, origin, RADIUS, TOP_LEFT_CIRCLE_COLOR, 1)
        rgb, origin = cu.pick_color_circle(small_img, RADIUS, right_origin, most_common=3)
        rgbs.append(rgb)
        cv2.rectangle(small_img,
                      (small_img_width - REF_COLOR_SIZE, 0),
                      (small_img_width, REF_COLOR_SIZE), TOP_RIGHT_CIRCLE_COLOR, -1)
        cv2.circle(small_img, origin, RADIUS, TOP_RIGHT_CIRCLE_COLOR, 1)
    except Exception, e:
        print str(e), '%s cannot create image' % (srcfile)

    analyzed_color, keys = cu.get_avg_color(rgbs[1:], 2)
    # セパレータとして黒を入れた後判定値を入れる
    rgbs.append((0, 0, 0))
    rgbs.append(analyzed_color)

    color = colortype.get_color(analyzed_color, COLORTYPE_DATA)
    #color_name, rgb, diff = get_color_name(analyzed_color)
    #color_name2, rgb2, diff2 = get_color_name2(analyzed_color)
    rgbs.append(rgb)
    #rgbs.append(rgb2)

    ## 描画
    patterns = cu.get_color_pattern(rgbs, 40, 9)
    small_img_height = small_img.shape[0]
    pict_height = small_img_height * 2
    text_height = 32
    pattern_height = patterns.shape[0]
    pict_width =  WIDTH * 2
    campass = np.zeros((pict_height + text_height + pattern_height, pict_width, 3), np.uint8)
    campass[pict_height:pict_height + text_height,:,:] = 255
    campass[:small_img_height, :WIDTH,:] = small_img
    campass[:small_img_height, WIDTH:,:] = edge_img
    campass[pict_height + text_height:,:patterns.shape[1],:] = patterns
    text = get_corner_names(keys)
    cv2.putText(campass, text, (0, pict_height + text_height - 16), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
    text = color[colortype.COLOR_NAME] + ': %s' % color[colortype.DIFF]
    cv2.putText(campass, text, (0, pict_height + text_height), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
    cv2.imwrite(dstfile, campass)

def get_color_name(rgb):
    lab = cu.bgr2lab(cu.rgb2bgr(rgb))
    mindiff = 99999999
    mincolor_name = None
    minrgb = None
    for k, v in BASECOLORS.items():
        ldiff = lab[0] - v[cp.CIELAB][0]
        adiff = lab[1] - v[cp.CIELAB][1]
        bdiff = lab[2] - v[cp.CIELAB][2]
        diff = math.sqrt(ldiff * ldiff + adiff * adiff + bdiff * bdiff)
        if mindiff > diff:
            mindiff = diff
            mincolor_name = v[cp.COLOR_NAME]
            minrgb = k
    return mincolor_name, minrgb, mindiff

def get_color_name2(rgb):
    lab = cu.bgr2lab(cu.rgb2bgr(rgb))
    mindiff = 99999999
    mincolor_name = None
    minrgb = None
    for k, v in COLORS.items():
        ldiff = lab[0] - v[cp.CIELAB][0]
        adiff = lab[1] - v[cp.CIELAB][1]
        bdiff = lab[2] - v[cp.CIELAB][2]
        diff = math.sqrt(ldiff * ldiff + adiff * adiff + bdiff * bdiff)
        if mindiff > diff:
            mindiff = diff
            mincolor_name = v[cp.COLOR_NAME]
            minrgb = k
    return mincolor_name, minrgb, mindiff

def get_corner_names(keys):
    """

    """
    corners = []
    for k in keys:
        if k == 0:
            corners.append('bottom-left')
        elif k == 1:
            corners.append('bottom-right')
        elif k == 2:
            corners.append('top-left')
        else:
            corners.append('top-right')
    return ','.join(corners)


if __name__ == '__main__':
    main()
