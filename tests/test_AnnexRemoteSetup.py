# -*- coding: utf-8 -*-

import io
import unittest

import annexremote


class SetupTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.output = io.StringIO()
        self.input = io.StringIO()

    def test_ListenNotLinked(self):
        annex = annexremote.Master(self.output)
        with self.assertRaises(annexremote.NotLinkedError):
            annex.Listen(io.StringIO("INITREMOTE"))
