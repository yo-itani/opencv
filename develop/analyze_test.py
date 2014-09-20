# -*- coding: utf-8 -*-
"""
指定したディレクトリの画像を解析し、指定したディレクトリに結果画像を作成するプログラム。

"""

import os
import numpy as np
import cv2
import color_utils as utils

SCRIPT_DIR = os.path.dirname(__file__)
WIDTH = 200
RADIUS = 10
CANNY_THRESHOLD1 = 5
CANNY_THRESHOLD2 = 25


def main(srcdir, dstdir):
    for i, f in enumerate(os.listdir(srcdir)):
        if f.endswith('.jpg'):
            img = cv2.imread(os.path.join(srcdir, f))
            # 画像縮小取得
            small_img = get_small_img(img, WIDTH)

            # エッジ画像取得
            edge_img = get_edge_img(small_img, CANNY_THRESHOLD1, CANNY_THRESHOLD2)

            rgbs = []
            # センターの色取得
            rgb, origin = utils.pick_center_color(small_img, RADIUS, shift_x=0, shift_y=-0, most_common=3)
            rgbs.append(rgb)
            cv2.circle(small_img, origin, RADIUS, (255, 255, 0), 1)

            # 左下隅、右下隅の色取得
            left_origin, right_origin = get_under_left_right_coordinage(edge_img, RADIUS)
            rgb, origin = utils.pick_color_circle(small_img, RADIUS, left_origin, most_common=3)
            rgbs.append(rgb)
            cv2.circle(small_img, origin, RADIUS, (255, 255, 0), 1)
            rgb, origin = utils.pick_color_circle(small_img, RADIUS, right_origin, most_common=3)
            rgbs.append(rgb)
            cv2.circle(small_img, origin, RADIUS, (255, 255, 0), 1)

            patterns = utils.get_color_pattern(rgbs, 40, 3)
            small_img_height = small_img.shape[0]
            campass = np.zeros((small_img_height * 2 + patterns.shape[0], WIDTH * 2, 3), np.uint8)
            campass[:small_img_height, :WIDTH,:] = small_img
            campass[:small_img_height, WIDTH:,:] = edge_img
            campass[small_img_height * 2:,:patterns.shape[1],:] = patterns
            cv2.imwrite('img/%s.jpg' % i, campass)
        if i > 5:
            break

def get_under_left_right_coordinage(edge_img, radius):
    """ エッジ画像から左下と右下の座標を取得する

        Args:
            edge_img: エッジ画像
            radius: 色検出に使う円の半径
        Returns:
            座標のtuple: ((left_x, left_y), (right_x, right_y))
    """
    MARGIN = 3
    mid_x = edge_img.shape[1] / 2
    black = np.array([0, 0, 0])
    under_h, left_w, right_w = -1, -1, -1
    start_h = edge_img.shape[0] * 9 / 10
    for h in xrange(start_h - 1, -1, -1):
        if not np.array_equal(edge_img[h][mid_x], black):
            under_h = h
            break
    under_h = under_h - radius - MARGIN
    for w in xrange(0, edge_img.shape[1]):
        if not np.array_equal(edge_img[under_h][w], black):
            left_w = w
            break
    left_w = left_w + radius + MARGIN
    for w in xrange(edge_img.shape[1] - 1, -1, -1):
        if not np.array_equal(edge_img[under_h][w], black):
            right_w = w
            break
    right_w = right_w - radius - MARGIN
    return ((left_w, under_h), (right_w, under_h),)


def get_edge_img(img, threshold1, threshold2):
    """ エッジ画像を返す。
        カラー画像と結合するためにbgrに変換して返す

        Args:
            img: エッジ画像を取得したい画像(np.array)形式
            threshold1: しきい値1
            threshold2: しきい値2
        Returns:
            エッジ画像:(np.array形式)
    """
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edge_img = cv2.Canny(gray_img, threshold1, threshold2)
    return cv2.cvtColor(edge_img, cv2.COLOR_GRAY2BGR)


def get_small_img(img, small_width):
    """ widthの幅まで縮小(比率維持)した画像を返す

        Args:
            img: 元画像(np.array形式)
            small_width: 縮小後の画像の幅
        Returns:
            縮小画像(np.array形式)
    """
    height, width = img.shape[:2]
    small_height = int(float(small_width) / width * height)
    return cv2.resize(img, (small_width, small_height))


if __name__ == '__main__':
    main(os.path.join(SCRIPT_DIR, 'src_img/web/t-shirts'), os.path.join(SCRIPT_DIR, 'img'))
