# -*- coding: utf-8 -*-

import numpy as np
import cv2
import pickle
import color_utils as utils
import math
import collections


SIZE_OF_PATTERN = 40
NUM_COLUMNS = 600 / SIZE_OF_PATTERN

class Weight(object):
    def __init__(self, radius, center_weight):
        self._radius = radius
        self._center_weight = center_weight

    def get(self, x):
        x = math.fabs(x)
        return -(1 / (2.0 * self._radius)) * x + self._center_weight


def main():
    radius = 10
    img = cv2.imread('img/girl1.jpg')
    rgbs = []
    #for i in xrange(300):
    for i in xrange(10):
        rgb, origin = pick_color_circle(img, radius, 20, shift_x=0, shift_y=-90, most_common=3)
        #rgb, start, end = pick_color(img, 7, most_common=3)
        rgbs.append(rgb)
    patterns = utils.get_color_pattern(rgbs, 40, 20)
    cv2.imwrite('img/pattern.jpg', patterns)
    #cv2.rectangle(img, start, end, (255, 255, 0), 1)
    cv2.circle(img, origin, radius, (255, 255, 0), 1)
    cv2.imwrite('img/range.jpg', img)


def get_circle_coordinates_all(origin, radius):
    coordinates = []
    for x in xrange(-radius, radius + 1):
        abs_y = int(math.sin(math.acos(float(x) / radius)) * radius)
        for y in xrange(-abs_y, abs_y + 1):
            coordinates.append((x + origin[0], y + origin[1]))
    return coordinates
    #while len(coordinates) < num_coordinates and \
    #      counter < num_coordinates * 5:
    #    x = np.random.randint(-radius, radius)
    #    y = math.sin(math.acos(float(x) / radius)) * radius
    #    w = weight.get(y)
    #    if counter % 2 != 0:
    #        y = -y
    #    x = x + origin[0]
    #    y = int(y) + origin[1]
    #    if (x, y, w) not in coordinates:
    #        coordinates.append((x, y, w))
    #    counter += 1
    #return coordinates

def get_circle_coordinates(origin, radius, num_coordinates):
    counter = 0
    coordinates = []
    #weight = Weight(radius, 1.5)
    while len(coordinates) < num_coordinates and \
          counter < num_coordinates * 5:
        x = np.random.randint(-radius, radius)
        y = math.sin(math.acos(float(x) / radius)) * radius
        #w = weight.get(y)
        if counter % 2 != 0:
            y = -y
        x = x + origin[0]
        y = int(y) + origin[1]
        #if (x, y, w) not in coordinates:
        #    coordinates.append((x, y, w))
        if (x, y) not in coordinates:
            coordinates.append((x, y))
        counter += 1
    return coordinates

def pick_color_circle(img, radius, num_coordinates=10, shift_x=0, shift_y=0, most_common=10):
    height, width = img.shape[:2]
    origin = width / 2 + shift_x, height / 2 + shift_y
    coordinates = get_circle_coordinates_all(origin, radius)
    #coordinates = get_circle_coordinates(origin, radius, num_coordinates)
    hsvs = {}
    cnt = collections.Counter()
    for w, h in coordinates:
        gbr = img[h][w]
        h, s, v = get_hsv(cv2.cvtColor(np.array([[gbr]]), cv2.COLOR_BGR2HSV)[0][0])
        if h in hsvs:
            hsvs[h].append(tuple(gbr))
        else:
            hsvs[h] = [tuple(gbr)]
        cnt[h] += 1
    rgb = get_median_rgb(hsvs, cnt, most_common)
    if not rgb:
        rgb = get_mean_rgb(hsvs, cnt, most_common)
    return (rgb, origin)


def get_median_rgb(hsvs, cnt, most_common):
    sum_b, sum_g, sum_r, counter = 0, 0, 0, 0
    hs = []
    for h, c in cnt.most_common(most_common):
        hs += [h] * c
    median = int(np.median(np.array(hs)))
    for h in xrange(median - 10, median + 10):
        if h in hsvs:
            for bgr in hsvs[h]:
                counter += 1
                sum_b += bgr[0]
                sum_g += bgr[1]
                sum_r += bgr[2]
    if counter:
        return (sum_r / counter, sum_g / counter, sum_b / counter)
    #return (255, 255, 255)
    return None

def get_mean_rgb(hsvs, cnt, most_common):
    sum_b, sum_g, sum_r, counter = 0, 0, 0, 0
    for h, c in cnt.most_common(most_common):
        for bgr in hsvs[h]:
            counter += 1
            sum_b += bgr[0]
            sum_g += bgr[1]
            sum_r += bgr[2]
    return (sum_r / counter, sum_g / counter, sum_b / counter)


def pick_color(img, band=3, shift_x=0, shift_y=0, most_common=10):
    band_lower = band / 2
    band_upper = band_lower + 1

    height, width = img.shape[:2]
    height_start = height / band * band_lower + shift_y
    height_end = height / band * band_upper + shift_y
    width_start = width / band * band_lower + shift_x
    width_end = width / band * band_upper + shift_x
    cnt = collections.Counter()
    data = {}
    for w in tuple(set(np.random.randint(height_start, height_end, 20)))[:10]:
        for h in tuple(set(np.random.randint(width_start, width_end, 20)))[:10]:
            gbr = img[h][w]
            h, s, v = get_hsv(cv2.cvtColor(np.array([[gbr]]), cv2.COLOR_BGR2HSV)[0][0])
            if h in data:
                data[h].append(tuple(gbr))
            else:
                data[h] = [tuple(gbr)]
            cnt[h] += 1
    hs = []
    for h, c in cnt.most_common(most_common):
        hs.append(h)
    sum_b, sum_g, sum_r, counter = 0, 0, 0, 0
    for h in hs:
        for bgr in data[h]:
            counter += 1
            sum_b += bgr[0]
            sum_g += bgr[1]
            sum_r += bgr[2]
    return ((sum_r / counter, sum_g / counter, sum_b / counter), (width_start, height_start), (width_end, height_end))

def get_hsv(hsv_img_val):
    hsv_h = hsv_img_val[0] * 2
    hsv_s = hsv_img_val[0] / 255.0
    hsv_v = hsv_img_val[0] / 255.0
    return (hsv_h, hsv_s, hsv_v)


def get_lab(lab_img_val):
    lab_l = lab_img_val[0] * 100.0 / 255.0
    lab_a = lab_img_val[1] - 128
    lab_b = lab_img_val[2] - 128
    return (lab_l, lab_a, lab_b)


def create_lab_pickle(filename):
    import csv
    data = {}
    for row in csv.reader(open(filename), delimiter='\t'):
        rstr, gstr, bstr = row[0][:2], row[0][2:4], row[0][4:]
        r, g, b = int(rstr, 16), int(gstr, 16), int(bstr, 16)
        bgr_img = np.array([[[np.uint8(b), np.uint8(g), np.uint8(r)]]])
        cielab_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2LAB)
        lab_val = get_lab(cielab_img[0][0])
        data[lab_val] = [(r, g, b), row[1],]
    pickle.dump(data, open('color_cielab.pickle', 'w'))


def create_color_pattern(filename):
    import csv
    color_pattern = []
    for row in csv.reader(open(filename), delimiter='\t'):
        rstr, gstr, bstr = row[0][:2], row[0][2:4], row[0][4:]
        color_pattern.append((int(rstr, 16), int(gstr, 16), int(bstr, 16)))
        img = utils.get_color_pattern(color_pattern, 40, 5)
    cv2.imwrite('img/pattern.jpg', img)


def cielab_test():
    pattern = utils.get_color_pattern([(255,0,0),], 40, 1)
    cv2.imwrite('img/red.jpg', pattern)
    lab_img = cv2.cvtColor(pattern, cv2.COLOR_BGR2LAB)
    #print lab_img
    print 208.0 - 128, 195.0 - 128
    print math.atan((195.0-128)/(208.0-128))
    #img = cv2.imread(img_file, cv2.CV_LOAD_IMAGE_COLOR)
    #height = len(img)
    #width = len(img[0])
    ##black_img = np.zeros((height, width, 1), np.uint8)
    ##cv2.circle(black_img, (200, 200), 500, 1, -1)
    #lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    #channels = [0, 1, 2,]  # L,a,b値を計算
    #hist_size = [4, 4, 4] # 各値を30段階で量子化
    #ranges = [0, 256, 0, 256, 0, 256]  # 各値の範囲は0〜255(http://opencv.jp/opencv-2svn/cpp/histograms.html)
    ##result = cv2.calcHist([img], channels, black_img, np.array(hist_size), np.array(ranges))
    #result = cv2.calcHist([img], [0], None, np.array([4]), np.array([0, 256]))
    #print result
    #result = cv2.calcHist([img], [1], None, np.array([4]), np.array([0, 256]))
    #print result
    #result = cv2.calcHist([img], [2], None, np.array([4]), np.array([0, 256]))
    #print result
    #result = cv2.calcHist([img], [0, 1], None, np.array([4, 4]), np.array([0, 256, 0, 256]))
    ##print result
    #result = cv2.calcHist([lab_img], channels, None, np.array(hist_size), np.array(ranges))
    #for l, A in enumerate(result):
    #    for a, B in enumerate(A):
    #        for b, val in enumerate(B):
    #            if val > 0:
    #                print l, a, b, val
    ##print result
    ##print len(result), len(result[0]), len(result[0][0])
    ##return cv2.calcHist([img], [0], black_img, np.array(hist_size), np.array(ranges))
    ## mask
    ##res = cv2.bitwise_and(img, img, mask=bkack_img)
    ##cv2.imwrite('img/result3.jpg', res)


    ##print len(img), len(img[0]), len(img)/4, len(img[0])/4
    ##img = cv2.resize(img, (len(img)/4, len(img[0])/4))
    ##pickle_file = 'rgbs3.pickle'
    ##part_y = len(img) / 4
    ##part_x = len(img[0]) / 4
    ##utils.create_rgb_frequency_picle(img, pickle_file, (part_y,  part_y * 2), (part_x, part_x * 3))
    ##rgbs = pickle.load(open(pickle_file))
    ##color_pattern = []
    ##for k, v in reversed(sorted(rgbs.items(), key=lambda x:x[1])):
    ##    if sum([int(x) for x in k.split(',')]) < 100:
    ##        continue
    ##    color_pattern.append(utils.get_rgb_int(k))
    ##    if len(color_pattern) >= 300:
    ##        break
    ###result = utils.get_cielab_histgram(com_img_np)
    ###for y in img:
    ###    for x in y:
    ###        color_pattern.append(','.join([str(a) for a in x]))
    ###cv2.imwrite('result.jpg', black_img)
    ##color_pattern.append(utils.get_rgb_avg(color_pattern))
    ##color_pattern = utils.get_color_pattern(color_pattern, SIZE_OF_PATTERN, NUM_COLUMNS)
    ###cv2.imwrite('img/result.jpg', color_pattern)
    ##cv2.imwrite('img/result2.jpg', color_pattern)
    ##cv2.imwrite('img/result2_base.jpg', img)
    ###cv2.imwrite('result.jpg', img)


if __name__ == '__main__':
    main()

