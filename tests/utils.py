import unittest
import unittest.mock as mock
import io

import AnnexRemote


class GitAnnexTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.output = io.StringIO()
        self.input = io.StringIO()

        self.annex = AnnexRemote.Master(self.output)
        self.remote = mock.MagicMock(wraps=DummyRemote(self.annex))

        self.annex.LinkRemote(self.remote)


def last_buffer_line(buffer):
    current_position = buffer.tell()
    buffer.seek(0)
    lines = buffer.readlines()
    buffer.seek(current_position)
    return lines[-1].rstrip("\n")
    
    
class DummyRemote(AnnexRemote.ExportRemote):
    def __init__(self, annex):
        pass
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

