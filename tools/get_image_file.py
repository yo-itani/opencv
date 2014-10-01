# -*- coding: utf-8 -*-

import bing_api.bing_api as bing_api

import os
import time

import cv2
import requests

import color_utils as cu
from secrets import BING_API_KEY

TOP = 50
IMG_INFO_TSV = 'img_info.tsv'
IMG_INFO_TSV_COLUMNS = ('No.', 'image url', 'image file', 'source url',)
CREATE_TSV_CMD = 'echo "%s" >> %%s' % ('\t'.join(['%s'] * len(IMG_INFO_TSV_COLUMNS)),)
WIDTH = 200
TIMEOUT = 10.0

def main(args):
    query = args.query
    num = args.num
    dest_dir = args.dest_dir
    counter = 0
    data_tsv = os.path.join(dest_dir, 'img_info.tsv')
    if os.path.isfile(data_tsv):
        os.remove(data_tsv)
    os.system(CREATE_TSV_CMD % (IMG_INFO_TSV_COLUMNS + (data_tsv,)))
    for skip in xrange(0, num, TOP):
        res = bing_api.get(BING_API_KEY, query, bing_api.IMAGE, bing_api.JSON, TOP, skip)
        for item in res['d']['results']:
            try:
                content_type = item.get('ContentType', '')
                image_url = item.get('MediaUrl', '')
                source_url = item.get('SourceUrl', '')
                if content_type and image_url:
                    img_file = get_img(image_url, content_type, counter, dest_dir)
                    if img_file:
                        resize_img(img_file, dest_dir, WIDTH)
                        os.system(CREATE_TSV_CMD % (counter, image_url, img_file, source_url, data_tsv))
                        counter += 1
            except Exception, e:
                print str(e)
        time.sleep(1)
        print '%s〜%s done' % (skip, skip + TOP,)
        if '__next' not in res['d']:
            break

def resize_img(img_file, dest_dir, width):
    """ 画像ファイルを引数で与えられた幅に縮める

        Args:
            img_file: 画像ファイル名
            dest_dir: 画像ファイルがあるディレクトリ
            width: 縮小(拡大)後の画像ファイルのサイズ(幅)
        Returns:
            なし
    """
    fpath_file = os.path.join(dest_dir, img_file)
    img = cv2.imread(fpath_file)
    resized_img = cu.get_resized_img(img, width)
    cv2.imwrite(fpath_file, resized_img)


def get_img(image_url, content_type, number, dest_dir):
    """ 画像をダウンロードしファイルとして保存する

        Args:
            image_url: イメージファイルのURL
            content_type: 服のタイプ
            number: イメージファイルにつける連番
            dest_dir: イメージファイル保存先
        Returns:
            取得成功: 作成した画像ファイル名  取得失敗: None
    """
    img_type = dest_dir.split('/')[-1]
    ext = get_ext(content_type)
    if not ext:
         ext = os.path.splitext(image_url)
    img_file = '%s.%08d%s' % (img_type, number, ext,)
    try:
        r = requests.get(image_url, timeout=TIMEOUT)
        if r.headers['content-type'].startswith(content_type) and \
           r.status_code == 200:
            fp = open(os.path.join(dest_dir, img_file), 'wb')
            fp.write(r.content)
            fp.close()
            return img_file
        return None
    except Exception, e:
        print str(e)
        print '%s could not get' % (image_url,)
        return None


def get_ext(content_type):
    """ コンテントタイプから拡張子を決定して返す。
        決定できないcontent typeの場合はNoneをかえす。

        Args:
            content_type: コンテントタイプ
        Returns:
            コンテントタイプから判断した拡張子(str)。
            判断できなかったときはNone
    """
    content_type = content_type.lower()
    if content_type == 'image/gif':
        return '.gif'
    elif content_type in ['image/jpeg', 'image/jpg',]:
        return '.jpg'
    elif content_type in ['image/x-png', 'image/png',]:
        return '.png'
    elif content_type in ['image/tiff', 'image/x-tiff',]:
        return '.tif'
    else:
        return None


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', '-q', action='store', required=True)
    parser.add_argument('--num', '-n', action='store', type=int, required=True)
    parser.add_argument('--dest_dir', '-d', action='store', required=True)
    args = parser.parse_args()
    main(args)
