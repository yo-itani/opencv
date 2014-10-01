# -*- coding: utf-8 -*-

VERSION = '1.00'

class ColorNumber(object):
    """ 色の値を一意の番号に変える処理を行うクラス

    """
    MAX_COLOR_VALUE = 255
    DEFAULT_LEVEL = 8
    def __init__(self, num_val1_levels=DEFAULT_LEVEL,
                 num_val2_levels=DEFAULT_LEVEL,
                 num_val3_levels=DEFAULT_LEVEL):
        """

        """
        max_color_value = self.MAX_COLOR_VALUE + 1
        self._num_val1_levels = num_val1_levels
        self._num_val2_levels = num_val2_levels
        self._num_val3_levels = num_val3_levels
        self._val1_level_val = max_color_value // num_val1_levels
        self._val2_level_val = max_color_value // num_val2_levels
        self._val3_level_val = max_color_value // num_val3_levels

    def _get_color_level(self, level_val, value):
        return value // level_val

    def _get_bgr_color_level(self, bgr):
        v1 = self._get_color_level(self._val1_level_val, bgr[0])
        v2 = self._get_color_level(self._val2_level_val, bgr[1])
        v3 = self._get_color_level(self._val3_level_val, bgr[2])
        return v1, v2, v3 

    def get_converted_bgr(self, bgr):
        v1 = self._get_color_level(self._val1_level_val, bgr[0])
        v2 = self._get_color_level(self._val2_level_val, bgr[1])
        v3 = self._get_color_level(self._val3_level_val, bgr[2])
        return (v1 * self._val1_level_val,
                v2 * self._val2_level_val,
                v3 * self._val3_level_val,)

    def get_color(self, color_num):
        multi_levels = self._num_val2_levels * self._num_val3_levels
        v1_level = color_num // multi_levels
        remainder = color_num % multi_levels
        v2_level = remainder // self._num_val3_levels
        v3_level = remainder % self._num_val3_levels
        return (v1_level * self._val1_level_val,
                v2_level * self._val2_level_val,
                v3_level * self._val3_level_val,)


    def get_color_num(self, bgr):
        (v1, v2, v3) = self._get_bgr_color_level(bgr)
        return v1 * self._num_val2_levels * self._num_val3_levels + \
               v2 * self._num_val3_levels + v3

def main():
    pass


if __name__ == '__main__':
    main()

