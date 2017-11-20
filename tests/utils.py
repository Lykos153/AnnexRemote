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
        def dummy_transfer(method, key, file_):
            if method == "STORE":
                return self.remote.transfer_store(key, file_)
            elif method == "RETRIEVE":
                return self.remote.transfer_retrieve(key, file_)
        self.remote.transfer = mock.MagicMock(wraps=dummy_transfer)
        def dummy_transferexport(method, key, file_):
            if method == "STORE":
                return self.remote.transferexport_store(key, file_)
            elif method == "RETRIEVE":
                return self.remote.transferexport_retrieve(key, file_)
        self.remote.transferexport = mock.MagicMock(wraps=dummy_transferexport)

        self.annex.LinkRemote(self.remote)

class DummyReply(AnnexRemote.Reply.RemoteReply):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return f"{self.msg}"

class DummyRemote(AnnexRemote.ExportRemote):
    def __init__(self, annex):
        pass
        #self.transfer_store = mock.MagicMock(wraps=self.transfer_store)
        #self.transfer_retrieve = mock.MagicMock(wraps=self.transfer_retrieve)
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
    def export(self, name):
        pass
    def transferexport_store(self, key, file_):
        pass
    def transferexport_retrieve(self, key, file_):
        pass
    def checkpresentexport(self, key):
        pass
    def removeexport(self, key):
        pass
    def removeexportdirectory(self, directory):
        pass
    def renameexport(self, key, new_name):
        pass

