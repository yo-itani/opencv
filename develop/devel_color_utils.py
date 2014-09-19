# -*- coding: utf-8 -*-

import numpy as np

MAX_CV_H = 108  # opencvが返すhの最大値


def get_median_rgb(cv_hsvs, cnt, most_common, scope=5):
    """ cv_hの出現数の上位most_common個の中央値を算出し
        その前後scopeの範囲内のcv_hを持つrgbの値の平均を返す

        Args:
            cv_hsvs: {cv_h: [(r1, g1, b1), (r2, g2, b2), ...], ...}
                    形式のディクショナリ
            cnt: cv_hの値をカウントしたcollections.Counterオブジェクト
            most_common: cv_hの上位何件を対象とするか指定
            scope: cv_hの中央値-scope〜cv_hの中央値+scopeの範囲のrgbを集計対象賭する
        Returns:
            計算されたrgb値: (r, g, b)
    """
    sum_b, sum_g, sum_r, counter = 0, 0, 0, 0
    cv_hs = []
    for cv_h, c in cnt.most_common(most_common):
        cv_hs += [cv_h] * c
    median = int(np.median(np.array(cv_hs)))
    for cv_h in xrange(median - scope, median + scope):
        if cv_h < 0:
            cv_h = MAX_CV_H - cv_h
        elif cv_h > 180:
            cv_h = cv_h - MAX_CV_H
        if cv_h in cv_hsvs:
            for bgr in cv_hsvs[cv_h]:
                counter += 1
                sum_b += bgr[0]
                sum_g += bgr[1]
                sum_r += bgr[2]
    if counter:
        return (sum_r / counter, sum_g / counter, sum_b / counter)
    return None


def get_mean_rgb(cv_hsvs, cnt, most_common):
    """ 出現率上位most_common個までのrgbの平均値を返す

        Args:
            cv_hsvs: {cv_h: [(r1, g1, b1), (r2, g2, b2), ...], ...}
                    形式のディクショナリ
            cnt: cv_hの値をカウントしたcollections.Counterオブジェクト
            most_common: cv_hの上位何件を対象とするか指定
        Returns:
            計算されたrgb値: (r, g, b)
    """
    sum_b, sum_g, sum_r, counter = 0, 0, 0, 0
    for cv_h, c in cnt.most_common(most_common):
        print cv_h
        for bgr in cv_hsvs[cv_h]:
            counter += 1
            sum_b += bgr[0]
            sum_g += bgr[1]
            sum_r += bgr[2]
    return (sum_r / counter, sum_g / counter, sum_b / counter)


def main():
    pass


if __name__ == '__main__':
    main()

