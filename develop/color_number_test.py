# -*- coding: utf-8 -*-

import unittest

import numpy as np

from color_number import ColorNumber

class ErrorDiffusionTest(unittest.TestCase):
    def test_get_converted_value(self):
        """ _get_color_levelのテスト """
        cn = ColorNumber()
        self.assertEqual(0, cn._get_color_level(32, 0))
        self.assertEqual(0, cn._get_color_level(32, 31))
        self.assertEqual(1, cn._get_color_level(32, 32))
        self.assertEqual(1, cn._get_color_level(32, 63))
        self.assertEqual(2, cn._get_color_level(32, 64))
        self.assertEqual(6, cn._get_color_level(32, 223))
        self.assertEqual(7, cn._get_color_level(32, 224))
        self.assertEqual(7, cn._get_color_level(32, 255))
        self.assertEqual(0, cn._get_color_level(64, 0))
        self.assertEqual(0, cn._get_color_level(64, 31))
        self.assertEqual(0, cn._get_color_level(64, 32))
        self.assertEqual(0, cn._get_color_level(64, 63))
        self.assertEqual(1, cn._get_color_level(64, 64))
        self.assertEqual(2, cn._get_color_level(64, 191))
        self.assertEqual(3, cn._get_color_level(64, 192))
        self.assertEqual(3, cn._get_color_level(64, 255))


    def test_get_conveted_bgr(self):
        """ _get_bgr_color_levelのテスト """
        cn = ColorNumber()
        self.assertEqual((0, 0, 0), cn._get_bgr_color_level(np.array([0, 0, 0])))
        self.assertEqual((0, 1, 1), cn._get_bgr_color_level(np.array([31, 32, 33])))
        self.assertEqual((6, 7, 7), cn._get_bgr_color_level(np.array([223, 224, 255])))

        cn = ColorNumber(4, 8, 16)
        self.assertEqual((0, 0, 0), cn._get_bgr_color_level(np.array([0, 0, 0])))
        self.assertEqual((0, 0, 0), cn._get_bgr_color_level(np.array([15, 15, 15])))
        self.assertEqual((0, 0, 1), cn._get_bgr_color_level(np.array([16, 16, 16])))
        self.assertEqual((0, 0, 1), cn._get_bgr_color_level(np.array([31, 31, 31])))
        self.assertEqual((0, 1, 2), cn._get_bgr_color_level(np.array([32, 32, 32])))
        self.assertEqual((0, 1, 3), cn._get_bgr_color_level(np.array([63, 63, 63])))
        self.assertEqual((1, 2, 4), cn._get_bgr_color_level(np.array([64, 64, 64])))

    def test_get_color_num(self):
        cn = ColorNumber()
        self.assertEqual(0, cn.get_color_num(np.array([0, 0, 0])))
        self.assertEqual(0, cn.get_color_num(np.array([0, 0, 31])))
        self.assertEqual(1, cn.get_color_num(np.array([0, 0, 32])))
        self.assertEqual(1, cn.get_color_num(np.array([0, 31, 32])))
        self.assertEqual(9, cn.get_color_num(np.array([0, 32, 32])))
        self.assertEqual(9, cn.get_color_num(np.array([31, 32, 32])))
        self.assertEqual(73, cn.get_color_num(np.array([32, 32, 32])))
        self.assertEqual(74, cn.get_color_num(np.array([32, 32, 64])))

        cn = ColorNumber(4, 8, 16)
        self.assertEqual(0, cn.get_color_num(np.array([0, 0, 0])))
        self.assertEqual(0, cn.get_color_num(np.array([0, 0, 15])))
        self.assertEqual(1, cn.get_color_num(np.array([0, 0, 16])))
        self.assertEqual(1, cn.get_color_num(np.array([0, 31, 16])))
        self.assertEqual(17, cn.get_color_num(np.array([0, 32, 16])))
        self.assertEqual(17, cn.get_color_num(np.array([0, 63, 16])))
        self.assertEqual(33, cn.get_color_num(np.array([0, 64, 16])))
        self.assertEqual(33, cn.get_color_num(np.array([63, 64, 16])))
        self.assertEqual(161, cn.get_color_num(np.array([64, 64, 16])))


    def test_get_converted_bgr(self):
        cn = ColorNumber()
        self.assertEqual((0, 0, 0), cn.get_converted_bgr(np.array([0, 0, 0])))
        self.assertEqual((0, 32, 32), cn.get_converted_bgr(np.array([31, 32, 33])))
        self.assertEqual((32, 64, 64), cn.get_converted_bgr(np.array([63, 64, 65])))
        self.assertEqual((192, 224, 224), cn.get_converted_bgr(np.array([223, 224, 225])))


    def test_get_color(self):
        cn = ColorNumber()
        self.assertEqual((0, 0, 0), cn.get_color(0))
        self.assertEqual((0, 0, 32), cn.get_color(1))
        self.assertEqual((0, 0, 224), cn.get_color(7))
        self.assertEqual((0, 32, 0), cn.get_color(8))
        self.assertEqual((0, 32, 32), cn.get_color(9))
        self.assertEqual((0, 224, 224), cn.get_color(63))
        self.assertEqual((32, 0, 0), cn.get_color(64))
        self.assertEqual((32, 32, 0), cn.get_color(72))
        self.assertEqual((224, 224, 192), cn.get_color(510))
        self.assertEqual((224, 224, 224), cn.get_color(511))

    def test_get_color_num_range(self):
        cn = ColorNumber()
        self.assertEqual(512, cn.get_color_num_range())
        cn = ColorNumber(4, 4, 4)
        self.assertEqual(64, cn.get_color_num_range())
        cn = ColorNumber(2, 4, 6)
        self.assertEqual(48, cn.get_color_num_range())


if __name__ == '__main__':
    unittest.main()

