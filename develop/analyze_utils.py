# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np

import color_utils as cu

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

    # セパレータとして黒を入れた後判定値を入れる
    rgbs.append((0, 0, 0))
    rgbs.append(cu.get_avg_color(rgbs[1:], 2))
    rgbs.append((0, 0, 0))

    ## 描画
    patterns = cu.get_color_pattern(rgbs, 40, 8)
    small_img_height = small_img.shape[0]
    campass = np.zeros((small_img_height * 2 + patterns.shape[0], WIDTH * 2, 3), np.uint8)
    campass[:small_img_height, :WIDTH,:] = small_img
    campass[:small_img_height, WIDTH:,:] = edge_img
    campass[small_img_height * 2:,:patterns.shape[1],:] = patterns
    cv2.imwrite(dstfile, campass)

if __name__ == '__main__':
    main()
