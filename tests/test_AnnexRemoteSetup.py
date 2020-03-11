# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
import io
import unittest

import annexremote

import utils


class SetupTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.output = io.StringIO()
        self.input = io.StringIO()

    def TestListenNotLinked(self):
        annex = annexremote.Master(self.output)
        with self.assertRaises(annexremote.NotLinkedError):
            annex.Listen(io.StringIO("INITREMOTE"))