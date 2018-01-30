import io
import unittest

import utils
from utils import GitAnnexTestCase

class TestGitAnnexRequestMessages(GitAnnexTestCase):
    def TestInitremote(self):
        self.annex.Listen(io.StringIO("INITREMOTE"))
        self.remote.initremote.assert_called_once()

    def TestPrepare(self):
        self.annex.Listen(io.StringIO("PREPARE"))
        self.remote.prepare.assert_called_once()

    def TestTransferStore(self):
        self.annex.Listen(io.StringIO("TRANSFER STORE Key File"))
        self.remote.transfer_store.assert_called_once_with("Key", "File")

    def TestTransferStoreMissingFilename(self):
        with self.assertRaises(SyntaxError):
            self.annex.Listen(io.StringIO("TRANSFER STORE Key"))

    def TestTransferStore_SpaceInFilename(self):
        self.annex.Listen(io.StringIO("TRANSFER STORE Key File with spaces"))
        self.remote.transfer_store.assert_called_once_with("Key", "File with spaces")

    def TestTransferRetrieve(self):
        self.annex.Listen(io.StringIO("TRANSFER RETRIEVE Key File"))
        self.remote.transfer_retrieve.assert_called_once_with("Key", "File")

    def TestTransferRetrieve_MissingFilename(self):
        with self.assertRaises(SyntaxError):
            self.annex.Listen(io.StringIO("TRANSFER RETRIEVE Key"))

    def TestTransferRetrieve_SpaceInFilename(self):
        self.annex.Listen(io.StringIO("TRANSFER RETRIEVE Key File with spaces"))
        self.remote.transfer_retrieve.assert_called_once_with("Key", "File with spaces")

    def TestCheckpresent(self):
        self.annex.Listen(io.StringIO("CHECKPRESENT Key"))
        self.remote.checkpresent.assert_called_once_with("Key")

    def TestRemove(self):
        self.annex.Listen(io.StringIO("REMOVE Key"))
        self.remote.remove.assert_called_once_with("Key")

    def TestGetcost(self):
        self.annex.Listen(io.StringIO("GETCOST"))
        self.remote.getcost.assert_called_once()

    def TestGetavailability(self):
        self.annex.Listen(io.StringIO("GETAVAILABILITY"))
        self.remote.getavailability.assert_called_once()

    def TestClaimurl(self):
        self.annex.Listen(io.StringIO("CLAIMURL Url"))
        self.remote.claimurl.assert_called_once_with("Url")

    def TestCheckurl(self):
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")

    def TestWhereis(self):
        self.annex.Listen(io.StringIO("WHEREIS Key"))
        self.remote.whereis.assert_called_once_with("Key")


class TestGitAnnexRequestMessagesExporttree(GitAnnexTestCase):
    def TestExportsupported(self):
        self.annex.Listen(io.StringIO("EXPORTSUPPORTED"))
        self.remote.exportsupported.assert_called_once()

    def TestExport(self):
        self.annex.Listen(io.StringIO("EXPORT Name"))
        self.remote.export.assert_called_once_with("Name")

    def TestExport_MissingName(self):
        with self.assertRaises(SyntaxError):
            self.annex.Listen(io.StringIO("EXPORT"))

    def TestExport_SpaceInName(self):
        self.annex.Listen(io.StringIO("EXPORT Name with spaces"))
        self.remote.export.assert_called_once_with("Name with spaces")
    
    def TestTransferexportStore(self):
        self.annex.Listen(io.StringIO("TRANSFEREXPORT STORE Key File"))
        self.remote.transferexport_store.assert_called_once_with("Key", "File")

    def TestTransferexportStore_MissingFilename(self):
        with self.assertRaises(SyntaxError):
            self.annex.Listen(io.StringIO("TRANSFEREXPORT STORE Key"))

    def TestTransferexportStore_SpaceInFilename(self):
        self.annex.Listen(io.StringIO("TRANSFEREXPORT STORE Key File with spaces"))
        self.remote.transferexport_store.assert_called_once_with("Key", "File with spaces")

    def TestTransferexportRetrieve(self):
        self.annex.Listen(io.StringIO("TRANSFEREXPORT RETRIEVE Key File"))
        self.remote.transferexport_retrieve.assert_called_once_with("Key", "File")

    def TestTransferexportRetrieve_MissingFilename(self):
        with self.assertRaises(SyntaxError):
            self.annex.Listen(io.StringIO("TRANSFEREXPORT RETRIEVE Key"))

    def TestTransferexportRetrieve_SpaceInFilename(self):
        self.annex.Listen(io.StringIO("TRANSFEREXPORT RETRIEVE Key File with spaces"))
        self.remote.transferexport_retrieve.assert_called_once_with("Key", "File with spaces")

    def TestCheckpresentexport(self):
        self.annex.Listen(io.StringIO("CHECKPRESENTEXPORT Key"))
        self.remote.checkpresentexport.assert_called_once_with("Key")

    def TestRemoveexport(self):
        self.annex.Listen(io.StringIO("REMOVEEXPORT Key"))
        self.remote.removeexport.assert_called_once_with("Key")

    def TestRemoveexportdirectory(self):
        self.annex.Listen(io.StringIO("REMOVEEXPORTDIRECTORY Directory"))
        self.remote.removeexportdirectory.assert_called_once_with("Directory")

    def TestRemoveexportdirectory_MissingDirectory(self):
        with self.assertRaises(SyntaxError):
            self.annex.Listen(io.StringIO("REMOVEEXPORTDIRECTORY"))

    def TestRemoveexportdirectory_SpaceInFilename(self):
        self.annex.Listen(io.StringIO("REMOVEEXPORTDIRECTORY Directory with spaces"))
        self.remote.removeexportdirectory.assert_called_once_with("Directory with spaces")
    
    def TestRenameexport(self):
        self.annex.Listen(io.StringIO("RENAMEEXPORT Key NewName"))
        self.remote.renameexport.assert_called_once_with("Key", "NewName")
    
    def TestRenameexport_MissingNewName(self):
        with self.assertRaises(SyntaxError):
            self.annex.Listen(io.StringIO("RENAMEEXPORT Key"))
    
    def TestRenameexport_SpaceInNewName(self):
        self.annex.Listen(io.StringIO("RENAMEEXPORT Key NewName with spaces"))
        self.remote.renameexport.assert_called_once_with("Key", "NewName with spaces")
