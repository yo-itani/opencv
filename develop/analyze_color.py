# -*- coding: utf-8 -*-

import os
import numpy as np
import cv2
import color_utils as cu
from analyze_utils import create_color_pick_img


SCRIPT_DIR = os.path.dirname(__file__)
WIDTH = 200
RADIUS = 5
CANNY_THRESHOLD1 = 5
CANNY_THRESHOLD2 = 25
VIRTICAL = 0
HORIZONTAL = 1
DELETE_RATE = 20.0

def main(srcdir, dstdir):
    """ 調査用画像作成

    """
    for i, f in enumerate(os.listdir(srcdir)):
        if f.endswith('.jpg'):
            srcfile = os.path.join(srcdir, f)
            dstfile = '%s/%s.jpg' % (dstdir, i)
            create_color_pick_img(srcfile, dstfile,
                                  _get_top_left_right_coordinate,
                                  _get_under_left_right_coordinage)
        #if i > 200:
        if i > 20:
            break

def get_color(filename):
    """ 引数で渡されたTシャツ画像からそのTシャツの色を返す

        Args:
            filename: Tシャツ画像ファイル(フルパス)
        Returns:
            判定した色rgb形式(r, g, b)
    """
    img = cv2.imread(filename)
    # 画像縮小取得
    small_img = cu.get_small_img(img, WIDTH)
    # エッジ画像取得
    edge_img = cu.get_edge_img(small_img, CANNY_THRESHOLD1, CANNY_THRESHOLD2)

    rgbs = []
    # 左上、右上の色取得
    left_origin, right_origin = _get_top_left_right_coordinate(edge_img, RADIUS)
    rgb, origin = cu.pick_color_circle(small_img, RADIUS, left_origin, most_common=3)
    rgbs.append(rgb)
    rgb, origin = cu.pick_color_circle(small_img, RADIUS, right_origin, most_common=3)
    rgbs.append(rgb)

    # 左下隅、右下隅の色取得
    left_origin, right_origin = _get_under_left_right_coordinage(edge_img, RADIUS)
    rgb, origin = cu.pick_color_circle(small_img, RADIUS, left_origin, most_common=3)
    rgbs.append(rgb)
    rgb, origin = cu.pick_color_circle(small_img, RADIUS, right_origin, most_common=3)
    rgbs.append(rgb)
    return cu.get_avg_color(rgbs[1:], 2)

def _get_top_left_right_coordinate(edge_img, radius):
    """ エッジ画像から左上と右上の座標を取得する

        Args:
            edge_img: エッジ画像
            radius: 色検出に使う円の半径
        Returns:
            座標のtuple: ((left_x, left_y), (right_x, right_y))
    """
    MARGIN = 10
    mid_x = int(edge_img.shape[1] * 11.0 / 20.0)
    under_h, left_w, right_w = -1, -1, -1
    # 上を少しカットする
    start_h = int(edge_img.shape[0] * (DELETE_RATE - 1) / DELETE_RATE)
    mid_coordinate = cu.get_nonzero_coordinate(edge_img, mid_x, cu.TO_BOTTOM, start_index=start_h)

    # ヒットした箇所(Tシャツの裾)から少し上に上げる
    top_h = mid_coordinate[1] + radius + MARGIN
    left_coordinate = cu.get_nonzero_coordinate(edge_img, top_h, cu.TO_RIGHT)
    right_coordinate = cu.get_nonzero_coordinate(edge_img, top_h, cu.TO_LEFT)

    # 内側半径程度入れる 
    return ((left_coordinate[0] + radius + MARGIN, left_coordinate[1]),
            (right_coordinate[0] - radius - MARGIN, right_coordinate[1]),)

    MARGIN = 5
    left_w, right_w = -1, -1
    black = np.array([0, 0, 0])
    # 上下を少しカットする
    start_h = int(edge_img.shape[0] * 1 / DELETE_RATE)
    end_h = edge_img.shape[0] - start_h
    for w in xrange(0, edge_img.shape[1]):
        if not np.array_equal(sum(edge_img[start_h:end_h,w,:]), black):
            left_w = w
            break
    left_coordinate = cu.get_nonzero_coordinate(edge_img, left_w, cu.TO_BOTTOM)
    for w in xrange(edge_img.shape[1] - 1, -1, -1):
        if not np.array_equal(sum(edge_img[start_h:end_h,w,:]), black):
            right_w = w
            break
    right_coordinate = cu.get_nonzero_coordinate(edge_img, right_w, cu.TO_BOTTOM)

    # 下に半径ほど落として中に半径ほど入れる
    return ((left_coordinate[0] + radius + MARGIN * 2, left_coordinate[1] + radius + MARGIN),
            (right_coordinate[0] - radius - MARGIN * 2, right_coordinate[1] + radius + MARGIN),)


def _get_under_left_right_coordinage(edge_img, radius):
    """ エッジ画像から左下と右下の座標を取得する

        Args:
            edge_img: エッジ画像
            radius: 色検出に使う円の半径
        Returns:
            座標のtuple: ((left_x, left_y), (right_x, right_y))
    """
    MARGIN = 10
    mid_x = int(edge_img.shape[1] * 11.0 / 20.0)
    under_h, left_w, right_w = -1, -1, -1
    # 下を少しカットする
    start_h = int(edge_img.shape[0] * (DELETE_RATE - 1) / DELETE_RATE)
    mid_coordinate = cu.get_nonzero_coordinate(edge_img, mid_x, cu.TO_TOP, start_index=start_h)

    # ヒットした箇所(Tシャツの裾)から少し上に上げる
    under_h = mid_coordinate[1] - radius - MARGIN
    left_coordinate = cu.get_nonzero_coordinate(edge_img, under_h, cu.TO_RIGHT)
    right_coordinate = cu.get_nonzero_coordinate(edge_img, under_h, cu.TO_LEFT)

    # 内側半径程度入れる 
    return ((left_coordinate[0] + radius + MARGIN, left_coordinate[1]),
            (right_coordinate[0] - radius - MARGIN, right_coordinate[1]),)


if __name__ == '__main__':
    #import sys
    #type = sys.argv[1]
    type = 't_shirts'
    #type = 'one_piece'
    main(os.path.join(SCRIPT_DIR, 'src_img/web/%s' % type), os.path.join(SCRIPT_DIR, 'img/%s' % type))
