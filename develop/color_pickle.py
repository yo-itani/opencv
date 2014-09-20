# -*- coding: utf-8 -*-

import sys
import csv
import pickle
import color_utils as cu

COLOR_NAME = 'color_name'
RGB = 'rgb'
BGR = 'bgr'
HSV = 'hsv'
CIELAB = 'lab'

def main(tsvfile, picklefile):
    create_color_pickle(tsvfile, picklefile)


def create_color_pickle(tsvfile, picklefile):
    """ color_pickleファイルを作成する

        TSVファイルは以下の形式
            文字コード: utf-8
            区切り文字: タブ
            タイトル行: なし

            項目
            1. カラー名
            2. RGB値(#RRGGBB形式 or R,G,B形式)

        RGBに同じ値があったときは後の値で上書きされる

        出力されるpickleファイルは以下の形式のディクショナリ
            {RGB: {COLOR_NAME: 色名(unicode),
                   BGR: BGR値(tuple),
                   HSV: HSV値(tuple),
                   LAB: CIE L*a*b値(tuple),
                  }, ...
            }

        Args:
            tsvfile: 読み込むTSVファイル名(フルパス)
            picklefile: 作成するpickleファイル名(フルパス)
        Returns:
            なし
    """
    colors = {}
    for row in csv.reader(open(tsvfile), delimiter='\t'):
        if len(row) != 2:
            continue
        rgb = cu.rgbstr2rgb(row[1])
        bgr = cu.rgb2bgr(rgb)
        hsv = cu.bgr2hsv(bgr)
        lab = cu.bgr2lab(bgr)
        colors[rgb] = {COLOR_NAME: row[0].decode('utf8'),
                       BGR: bgr,
                       HSV: hsv,
                       CIELAB: lab,}
    pickle.dump(colors, open(picklefile, 'w'))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
