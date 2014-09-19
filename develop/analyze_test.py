# -*- coding: utf-8 -*-
"""
指定したディレクトリの画像を解析し、指定したディレクトリに結果画像を作成するプログラム。

"""

import os
import numpy as np
import cv2
import color_utils as utils

def main(srcdir, dstdir):
    WIDTH = 200
    RADIUS = 10
    for i, f in enumerate(os.listdir(srcdir)):
        if f.endswith('.jpg'):
            img = cv2.imread(os.path.join(srcdir, f))
            height, width = img.shape[:2]
            small_height = int(float(WIDTH) / width * height)
            small_img = cv2.resize(img, (WIDTH, small_height))

            rgb, origin = utils.pick_color_circle(small_img, RADIUS, shift_x=0, shift_y=-0, most_common=3)
            cv2.circle(small_img, origin, RADIUS, (255, 255, 0), 1)

            gray_img = cv2.cvtColor(small_img, cv2.COLOR_BGR2GRAY)
            edge_img = cv2.Canny(gray_img, 5, 25)
            gray_img = cv2.cvtColor(edge_img, cv2.COLOR_GRAY2BGR)
            campass = np.zeros((small_height * 2, WIDTH * 2, 3), np.uint8)
            campass[:small_height, :WIDTH,:] = small_img
            campass[:small_height, WIDTH:,:] = gray_img
            cv2.imwrite('img/%s.jpg' % i, campass)
        if i > 5:
            break

if __name__ == '__main__':
    main('src_img/web/t-shirts', 'img')
