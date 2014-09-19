# -*- coding: utf-8 -*-

import pickle
import cv2
import numpy as np


def get_cielab_histgram(img, mask=None):
    """ cielab形式のヒストグラムデータを返す。

        Args:
            img: bgr形式のイメージデータ(numpy形式)
            mask: マスク情報
        Returns:
            numpy形式のヒストグラムデータ
    """
    lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    channels = [0, 1, 2,]  # L,a,b値を計算
    hist_size = [30, 20, 10,]  # 各値を30段階で量子化
    ranges = [0, 255, 0, 255, 0, 255,]  # 各値の範囲は0〜255(http://opencv.jp/opencv-2svn/cpp/histograms.html)
    return cv2.calcHist(lab_img, channels, mask, np.array(hist_size), np.array(ranges))


def create_single_color_img(height, width, rgb):
    """ 単色のイメージデータ(numpy形式)を返す

        Args:
            height: 画像の高さ(pixcel)
            width: 画像の幅(pixcel)
            rgb: 画像の色(r, g, b)軽視のタプル。各値はint。
        Returns:
            numpy形式の画像データ
    """
    blank_img = np.zeros((height, width, 3), np.uint8)
    blank_img[:] = tuple(reversed(rgb))
    return blank_img


def get_rgb_int(rgb_str):
    """ 'r,g,b'形式の文字列を(r, g, b)形式のtuple西て返す
        (r, g, b)の各値はint

        Args:
            rgb_str: r,g,b形式の文字列
        Returns
            (r, g, b)形式のtuple。各値はint。
    """
    r, g, b = rgb_str.split(',')
    return (int(r), int(g), int(b))


def get_rgb_avg(rgb_list):
    """ rgb_listで渡されたrgbの平均値を返す

        Args:
            rgbのリストrgbは(r, g, b)形式のtupleなどr, g, bはint
        Returns:
            rgbの平均値(r, g, b)形式
    """
    r, g, b, num_rgb = 0, 0, 0, 0
    for rgb in rgb_list:
        r += int(rgb[0])
        g += int(rgb[1])
        b += int(rgb[2])
        num_rgb += 1
    return (r / num_rgb, g / num_rgb, b / num_rgb)


def get_color_pattern(rgb_list, size_of_pattern, num_column):
    """ rgb_listで渡されたrgbのカラーパターンを作成する

        Args:
            size_of_pattern: rgb一つあたりのカラーパターンサイズ(pixcel)
            num_column: 列数
        Returns:
            カラーパターンデータ(numpy.array形式)
    """
    num_rgb = len(rgb_list)
    height = size_of_pattern + (num_rgb - 1)/ num_column * size_of_pattern
    width = num_column * size_of_pattern
    black_img = create_single_color_img(height,
                                        width,
                                        (0,0,0))
    row_count = 0
    column_count = 0
    for rgb in rgb_list:
        img = create_single_color_img(size_of_pattern, size_of_pattern, rgb)
        row_start = size_of_pattern * row_count
        column_start = size_of_pattern * column_count
        black_img[row_start:row_start + size_of_pattern, column_start:column_start + size_of_pattern, :] = img
        column_count += 1
        if column_count >= num_column:
            column_count = 0
            row_count += 1
    return black_img


def create_rgb_frequency_picle(img, pickle_file, height_range=None, width_range=None):
    """ rgb出現頻度を解析し、picleファイルに保存する

        Args:
            img: イメージデータ(numpy.array形式)
            pickle_file: 出力するpickleファイル名
            height_range: 頻度を計算する範囲(高さ)
            width_range: 頻度を計算する範囲(幅)
        Returns:
            なし
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    rgbs = {}
    if height_range:
        y_start = height_range[0]
        y_end = height_range[1]
    else:
        y_start = 0
        y_end = len(img)
    if width_range:
        x_start = width_range[0]
        x_end = width_range[1]
    else:
        x_start = 0
        x_end = len(img[0])
    for y in xrange(y_start, y_end):
        for x in xrange(x_start, x_end):
            ndarray_str = str(img[y][x])
            ndarray_str = ndarray_str[1:-1].strip().replace('  ', ' ')
            rgb_str = ','.join(ndarray_str.split(' '))
            if rgb_str in rgbs:
                rgbs[rgb_str] += 1
            else:
                rgbs[rgb_str] = 1
    pickle.dump(rgbs, open(pickle_file, 'w'))

def main():
    pass


if __name__ == '__main__':
    main()
