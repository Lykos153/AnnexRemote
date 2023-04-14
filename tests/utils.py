import unittest
from unittest import mock
import io

import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import annexremote


class MinimalTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.output = io.StringIO()
        self.input = io.StringIO()

        self.annex = annexremote.Master(self.output)
        self.remote = MinimalRemote(self.annex)

        self.annex.LinkRemote(self.remote)


class FullTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.output = io.StringIO()
        self.input = io.StringIO()

        self.annex = annexremote.Master(self.output)
        self.remote = mock.MagicMock(wraps=FullRemote(self.annex))

        self.annex.LinkRemote(self.remote)


class ExportTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.output = io.StringIO()
        self.input = io.StringIO()

        self.annex = annexremote.Master(self.output)
        self.remote = mock.MagicMock(wraps=FullExportRemote(self.annex))

        self.annex.LinkRemote(self.remote)


def first_buffer_line(buf):
    return buffer_lines(buf)[0]


def second_buffer_line(buf):
    return buffer_lines(buf)[1]


def last_buffer_line(buf):
    return buffer_lines(buf)[-1]


def buffer_lines(buf):
    current_position = buf.tell()
    buf.seek(0)
    lines = list()
    for line in buf:
        lines.append(line.rstrip("\n"))
    buf.seek(current_position)
    return lines


class MinimalRemote(annexremote.SpecialRemote):
    def initremote(self):
        pass

    def prepare(self):
        pass

    def transfer_store(self, key, file_):
        pass

    def transfer_retrieve(self, key, file_):
        pass

    def checkpresent(self, key):
        pass

    def remove(self, key):
        pass


class FullRemote(annexremote.SpecialRemote):
    def initremote(self):
        pass

    def prepare(self):
        pass

    def transfer_store(self, key, file_):
        pass

    def transfer_retrieve(self, key, file_):
        pass

    def checkpresent(self, key):
        pass

    def remove(self, key):
        pass

    def getcost(self):
        pass

    def getavailability(self):
        pass

    def claimurl(self, url):
        pass

    def checkurl(self, url):
        pass

    def whereis(self, whereis):
        pass

    def error(self, msg):
        pass


class FullExportRemote(annexremote.ExportRemote):
    def initremote(self):
        pass

    def prepare(self):
        pass

    def transfer_store(self, key, file_):
        pass

    def transfer_retrieve(self, key, file_):
        pass

    def checkpresent(self, key):
        pass

    def remove(self, key):
        pass

    def getcost(self):
        pass

    def getavailability(self):
        pass

    def claimurl(self, url):
        pass

    def checkurl(self, url):
        pass

    def whereis(self, whereis):
        pass

    def error(self, msg):
        pass

    # Export methods
    def transferexport_store(self, key, file_, name):
        pass

    def transferexport_retrieve(self, key, file_, name):
        pass

    def checkpresentexport(self, key, name):
        pass

    def removeexport(self, key, name):
        pass

    def removeexportdirectory(self, directory):
        pass

    def renameexport(self, key, name, new_name):
        pass
