# -*- coding: utf-8 -*-

import os
import numpy as np
import cv2
import color_utils as cu
import colortype


SCRIPT_DIR = os.path.dirname(__file__)
WIDTH = 200
RADIUS = 5
CANNY_THRESHOLD1 = 5
CANNY_THRESHOLD2 = 25
VIRTICAL = 0
HORIZONTAL = 1
DELETE_RATE = 20.0

PATTERN_SIZE = 40
WIDTH = 200
REF_COLOR_SIZE = 15
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

COLORS = colortype.load_tsv(os.path.join(SCRIPT_DIR, 'colortype.tsv'))

def main(srcdir, dstdir, index=None):
    """ 調査用画像作成

    """
    for i, f in enumerate(os.listdir(srcdir)):
        if index:
            if i != int(index) - 1:
                continue
        if f.endswith('.jpg'):
            srcfile = os.path.join(srcdir, f)
            dstfile = '%s/%s.jpg' % (dstdir, i)
            create_color_pick_img(srcfile, dstfile)
        #if i > 200:
        if i > 20:
            break


def create_color_pick_img(srcfile, dstfile):
    """ 色取得調査用画像を生成する

    """
    img = cv2.imread(srcfile)
    # 画像縮小取得
    small_img = cu.get_small_img(img, WIDTH)
    small_img_height, small_img_width = small_img.shape[:2]
    # エッジ画像取得
    edge_img = cu.get_edge_img(small_img, CANNY_THRESHOLD1, CANNY_THRESHOLD2)

    rgbs = []
    try:
        rgbs = []
        # 左上、右上の色取得
        left_origin, right_origin = _get_top_left_right_coordinate(edge_img, RADIUS)
        left_top_rgb, left_top_origin = cu.pick_color_circle(small_img, RADIUS, left_origin, most_common=3)
        rgbs.append(left_top_rgb)
        cv2.rectangle(small_img,
                      (0, 0),
                      (REF_COLOR_SIZE, REF_COLOR_SIZE), cu.rgb2bgr(left_top_rgb), -1)
        cv2.rectangle(small_img,
                      (0, 0),
                      (REF_COLOR_SIZE, REF_COLOR_SIZE), TOP_LEFT_CIRCLE_COLOR, 1)
        cv2.circle(small_img, left_top_origin, RADIUS, TOP_LEFT_CIRCLE_COLOR, 1)

        right_top_rgb, right_top_origin = cu.pick_color_circle(small_img, RADIUS, right_origin, most_common=3)
        rgbs.append(right_top_rgb)
        cv2.rectangle(small_img,
                      (small_img_width - REF_COLOR_SIZE, 0),
                      (small_img_width, REF_COLOR_SIZE), cu.rgb2bgr(right_top_rgb), -1)
        cv2.rectangle(small_img,
                      (small_img_width - REF_COLOR_SIZE, 0),
                      (small_img_width, REF_COLOR_SIZE), TOP_RIGHT_CIRCLE_COLOR, 1)
        cv2.circle(small_img, right_top_origin, RADIUS, TOP_RIGHT_CIRCLE_COLOR, 1)

        # 左下隅、右下隅の色取得
        left_origin, right_origin = _get_under_left_right_coordinage(edge_img, RADIUS)
        left_bottom_rgb, left_bottom_origin = cu.pick_color_circle(small_img, RADIUS, left_origin, most_common=3)
        rgbs.append(left_bottom_rgb)
        cv2.rectangle(small_img,
                      (0, small_img_height - REF_COLOR_SIZE),
                      (REF_COLOR_SIZE, small_img_height), cu.rgb2bgr(left_bottom_rgb), -1)
        cv2.rectangle(small_img,
                      (0, small_img_height - REF_COLOR_SIZE),
                      (REF_COLOR_SIZE, small_img_height), BOTTOM_LEFT_CIRCLE_COLOR, 1)
        cv2.circle(small_img, left_bottom_origin, RADIUS, BOTTOM_LEFT_CIRCLE_COLOR, 1)
        right_bottom_rgb, right_bottom_origin = cu.pick_color_circle(small_img, RADIUS, right_origin, most_common=3)
        rgbs.append(right_bottom_rgb)
        cv2.rectangle(small_img,
                      (small_img_width - REF_COLOR_SIZE, small_img_height - REF_COLOR_SIZE),
                      (small_img_width, small_img_height), cu.rgb2bgr(right_bottom_rgb), -1)
        cv2.rectangle(small_img,
                      (small_img_width - REF_COLOR_SIZE, small_img_height - REF_COLOR_SIZE),
                      (small_img_width, small_img_height), BOTTOM_RIGHT_CIRCLE_COLOR, 1)
        cv2.circle(small_img, right_bottom_origin, RADIUS, BOTTOM_RIGHT_CIRCLE_COLOR, 1)

    except Exception, e:
        print str(e), '%s cannot create image' % (srcfile)
        raise e

    analyzed_color, keys = cu.get_avg_color(rgbs, 2)
    color = colortype.get_color_devel(analyzed_color, COLORS)

    ## 描画
    pattern_rgbs = [analyzed_color] + color[colortype.RGB]
    patterns = cu.get_color_pattern(pattern_rgbs, PATTERN_SIZE, 10)
    patterns[:,PATTERN_SIZE * len(pattern_rgbs):,:] = 255
    small_img_height = small_img.shape[0]
    pict_height = small_img_height
    text_height = 40 
    pattern_height = patterns.shape[0]
    pict_width =  WIDTH * 2
    campass = np.zeros((pict_height + text_height + pattern_height, pict_width, 3), np.uint8)
    campass[pict_height:pict_height + text_height,:,:] = 255
    campass[:small_img_height, :WIDTH,:] = small_img
    campass[:small_img_height, WIDTH:,:] = edge_img
    campass[pict_height + text_height:,:patterns.shape[1],:] = patterns
    text = get_corner_names(keys)
    cv2.putText(campass, text, (0, pict_height + text_height - 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
    text = '%s: %s :%s' % (color[colortype.INDEX], color[colortype.COLOR_NAME], color[colortype.DIFF])
    cv2.putText(campass, text, (0, pict_height + text_height - 4), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
    cv2.imwrite(dstfile, campass)


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


def get_corner_names(keys):
    """

    """
    corners = []
    for k in keys:
        if k == 0:
            corners.append('top-left')
        elif k == 1:
            corners.append('top-right')
        elif k == 2:
            corners.append('bottom-left')
        else:
            corners.append('bottom-right')
    return ','.join(corners)


if __name__ == '__main__':
    #import sys
    #type = sys.argv[1]
    type = 't_shirts'
    index = 1
    #type = 'one_piece'
    main(os.path.join(SCRIPT_DIR, 'src_img/web/%s' % type), os.path.join(SCRIPT_DIR, 'img/%s' % type), index)
