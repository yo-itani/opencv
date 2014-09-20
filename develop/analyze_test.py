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
RADIUS = 5
CANNY_THRESHOLD1 = 5
CANNY_THRESHOLD2 = 25
VIRTICAL = 0
HORIZONTAL = 1

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

            left_origin, right_origin = get_top_left_right_coordinate(edge_img, RADIUS)
            rgb, origin = utils.pick_color_circle(small_img, RADIUS, left_origin, most_common=3)
            rgbs.append(rgb)
            cv2.circle(small_img, origin, RADIUS, (255, 255, 0), 1)
            rgb, origin = utils.pick_color_circle(small_img, RADIUS, right_origin, most_common=3)
            rgbs.append(rgb)
            cv2.circle(small_img, origin, RADIUS, (255, 255, 0), 1)
            patterns = utils.get_color_pattern(rgbs, 40, 6)
            small_img_height = small_img.shape[0]
            campass = np.zeros((small_img_height * 2 + patterns.shape[0], WIDTH * 2, 3), np.uint8)
            campass[:small_img_height, :WIDTH,:] = small_img
            campass[:small_img_height, WIDTH:,:] = edge_img
            campass[small_img_height * 2:,:patterns.shape[1],:] = patterns
            cv2.imwrite('img/%s.jpg' % i, campass)
        #if i > 3:
        #    break

def get_top_left_right_coordinate(edge_img, radius):
    """
    """
    MARGIN = 5
    left_w, right_w = -1, -1
    black = np.array([0, 0, 0])
    # 上下を少しカットする
    start_h = int(edge_img.shape[0] * 1 / 10.0)
    end_h = int(edge_img.shape[0] * 9 / 10.0)
    for w in xrange(0, edge_img.shape[1]):
        if not np.array_equal(sum(edge_img[start_h:end_h,w,:]), black):
            left_w = w
            break
    left_h = get_nonzero_index(edge_img, left_w, VIRTICAL, revrse=False)
    for w in xrange(edge_img.shape[1] - 1, -1, -1):
        if not np.array_equal(sum(edge_img[start_h:end_h,w,:]), black):
            right_w = w
            break
    right_h = get_nonzero_index(edge_img, right_w, VIRTICAL, revrse=False)
    # 下に半径ほど落として中に半径ほど入れる
    left_w += radius + MARGIN * 2
    left_h += radius + MARGIN
    right_w -= radius + MARGIN * 2
    right_h += radius + MARGIN
    return ((left_w, left_h), (right_w, right_h),)


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
    under_h, left_w, right_w = -1, -1, -1
    start_h = edge_img.shape[0] * 9 / 10
    under_h = get_nonzero_index(edge_img, mid_x, VIRTICAL, revrse=True, end=start_h)
    under_h = under_h - radius - MARGIN
    left_w = get_nonzero_index(edge_img, under_h, HORIZONTAL, revrse=False)
    left_w = left_w + radius + MARGIN
    right_w = get_nonzero_index(edge_img, under_h, HORIZONTAL, revrse=True)
    right_w = right_w - radius - MARGIN
    return ((left_w, under_h), (right_w, under_h),)


def get_nonzero_index(img, fixed_index, direction, revrse=False, end=None):
    black = np.array([0, 0, 0])
    if direction == VIRTICAL:
        if not end:
            end = img.shape[0]
        arr = img[:,fixed_index,:]
    else:
        if not end:
            end = img.shape[1]
        arr = img[fixed_index,:,:]
    if revrse:
        iter = xrange(end - 1, -1, -1)
    else:
        iter = xrange(0, end)
    for a in iter:
        if not np.array_equal(arr[a], black):
            return a

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
