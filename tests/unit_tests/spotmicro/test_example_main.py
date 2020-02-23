#!/usr/bin/env python3

import unittest
import spotmicro.utilities.log as logging

from spotmicro.example_main import SpotMicro

log = logging.setup_logger('UnitTest_SpotMicroTestCase')


class SpotMicroTestCase(unittest.TestCase):

    def test_barks_in_spanish(self):
        # given
        spotmicro = SpotMicro()

        # when

        # then
        self.assertEqual(spotmicro._spanish_bark, spotmicro.bark_in_spanish())

    def test_barks_in_japanese(self):
        # given
        spotmicro = SpotMicro()

        # when

        # then
        self.assertEqual(spotmicro._japanese_bark, spotmicro.bark_in_japanese())

    def test_barks_in_german(self):
        # given
        spotmicro = SpotMicro()

        # when

        # then
        self.assertEqual(spotmicro._german_bark, spotmicro.bark_in_german())

    def test_barks_in_english(self):
        # given
        spotmicro = SpotMicro()

        # when

        # then
        self.assertEqual(spotmicro._english_bark, spotmicro.bark_in_english())


if __name__ == '__main__':
    unittest.main()
