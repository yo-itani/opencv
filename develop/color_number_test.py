# -*- coding: utf-8 -*-

import unittest

import numpy as np

from color_number import ColorNumber

class ErrorDiffusionTest(unittest.TestCase):
    def test_get_converted_value(self):
        """ _get_color_levelのテスト """
        error_diffusion = ColorNumber()
        self.assertEqual(0, error_diffusion._get_color_level(32, 0))
        self.assertEqual(0, error_diffusion._get_color_level(32, 31))
        self.assertEqual(1, error_diffusion._get_color_level(32, 32))
        self.assertEqual(1, error_diffusion._get_color_level(32, 63))
        self.assertEqual(2, error_diffusion._get_color_level(32, 64))
        self.assertEqual(6, error_diffusion._get_color_level(32, 223))
        self.assertEqual(7, error_diffusion._get_color_level(32, 224))
        self.assertEqual(7, error_diffusion._get_color_level(32, 255))
        self.assertEqual(0, error_diffusion._get_color_level(64, 0))
        self.assertEqual(0, error_diffusion._get_color_level(64, 31))
        self.assertEqual(0, error_diffusion._get_color_level(64, 32))
        self.assertEqual(0, error_diffusion._get_color_level(64, 63))
        self.assertEqual(1, error_diffusion._get_color_level(64, 64))
        self.assertEqual(2, error_diffusion._get_color_level(64, 191))
        self.assertEqual(3, error_diffusion._get_color_level(64, 192))
        self.assertEqual(3, error_diffusion._get_color_level(64, 255))


    def test_get_conveted_bgr(self):
        """ _get_bgr_color_levelのテスト """
        error_diffusion = ColorNumber()
        self.assertEqual((0, 0, 0), error_diffusion._get_bgr_color_level(np.array([0, 0, 0])))
        self.assertEqual((0, 1, 1), error_diffusion._get_bgr_color_level(np.array([31, 32, 33])))
        self.assertEqual((6, 7, 7), error_diffusion._get_bgr_color_level(np.array([223, 224, 255])))

        error_diffusion = ColorNumber(4, 8, 16)
        self.assertEqual((0, 0, 0), error_diffusion._get_bgr_color_level(np.array([0, 0, 0])))
        self.assertEqual((0, 0, 0), error_diffusion._get_bgr_color_level(np.array([15, 15, 15])))
        self.assertEqual((0, 0, 1), error_diffusion._get_bgr_color_level(np.array([16, 16, 16])))
        self.assertEqual((0, 0, 1), error_diffusion._get_bgr_color_level(np.array([31, 31, 31])))
        self.assertEqual((0, 1, 2), error_diffusion._get_bgr_color_level(np.array([32, 32, 32])))
        self.assertEqual((0, 1, 3), error_diffusion._get_bgr_color_level(np.array([63, 63, 63])))
        self.assertEqual((1, 2, 4), error_diffusion._get_bgr_color_level(np.array([64, 64, 64])))

    def test_get_color_num(self):
        error_diffusion = ColorNumber()
        self.assertEqual(0, error_diffusion.get_color_num(np.array([0, 0, 0])))
        self.assertEqual(0, error_diffusion.get_color_num(np.array([0, 0, 31])))
        self.assertEqual(1, error_diffusion.get_color_num(np.array([0, 0, 32])))
        self.assertEqual(1, error_diffusion.get_color_num(np.array([0, 31, 32])))
        self.assertEqual(9, error_diffusion.get_color_num(np.array([0, 32, 32])))
        self.assertEqual(9, error_diffusion.get_color_num(np.array([31, 32, 32])))
        self.assertEqual(73, error_diffusion.get_color_num(np.array([32, 32, 32])))
        self.assertEqual(74, error_diffusion.get_color_num(np.array([32, 32, 64])))

        error_diffusion = ColorNumber(4, 8, 16)
        self.assertEqual(0, error_diffusion.get_color_num(np.array([0, 0, 0])))
        self.assertEqual(0, error_diffusion.get_color_num(np.array([0, 0, 15])))
        self.assertEqual(1, error_diffusion.get_color_num(np.array([0, 0, 16])))
        self.assertEqual(1, error_diffusion.get_color_num(np.array([0, 31, 16])))
        self.assertEqual(17, error_diffusion.get_color_num(np.array([0, 32, 16])))
        self.assertEqual(17, error_diffusion.get_color_num(np.array([0, 63, 16])))
        self.assertEqual(33, error_diffusion.get_color_num(np.array([0, 64, 16])))
        self.assertEqual(33, error_diffusion.get_color_num(np.array([63, 64, 16])))
        self.assertEqual(161, error_diffusion.get_color_num(np.array([64, 64, 16])))


    def test_get_converted_bgr(self):
        error_diffusion = ColorNumber()
        self.assertEqual((0, 0, 0), error_diffusion.get_converted_bgr(np.array([0, 0, 0])))
        self.assertEqual((0, 32, 32), error_diffusion.get_converted_bgr(np.array([31, 32, 33])))
        self.assertEqual((32, 64, 64), error_diffusion.get_converted_bgr(np.array([63, 64, 65])))
        self.assertEqual((192, 224, 224), error_diffusion.get_converted_bgr(np.array([223, 224, 225])))


    def test_get_color(self):
        error_diffusion = ColorNumber()
        self.assertEqual((0, 0, 0), error_diffusion.get_color(0))
        self.assertEqual((0, 0, 32), error_diffusion.get_color(1))
        self.assertEqual((0, 0, 224), error_diffusion.get_color(7))
        self.assertEqual((0, 32, 0), error_diffusion.get_color(8))
        self.assertEqual((0, 32, 32), error_diffusion.get_color(9))
        self.assertEqual((0, 224, 224), error_diffusion.get_color(63))
        self.assertEqual((32, 0, 0), error_diffusion.get_color(64))
        self.assertEqual((32, 32, 0), error_diffusion.get_color(72))
        self.assertEqual((224, 224, 192), error_diffusion.get_color(510))
        self.assertEqual((224, 224, 224), error_diffusion.get_color(511))


if __name__ == '__main__':
    unittest.main()

