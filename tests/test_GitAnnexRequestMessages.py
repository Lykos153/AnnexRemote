import io
import unittest

import utils
from AnnexRemote import Error
from AnnexRemote import UnsupportedRequest

class TestGitAnnexRequestMessages(utils.GitAnnexTestCase):

    def last_line(self, buffer):
        current_position = buffer.tell()
        buffer.seek(0)
        lines = buffer.readlines()
        buffer.seek(current_position)
        return lines[-1]
        
    def TestInitremoteSuccess(self):
        self.remote.initremote.return_value = True
        self.annex.Listen(io.StringIO("INITREMOTE"))
        self.remote.initremote.assert_called_once()
        self.assertEqual(self.last_line(self.output), "INITREMOTE-SUCCESS")
        
    def TestInitremoteFailure(self):
        self.remote.initremote.return_value = Error("ErrorMsg")
        self.annex.Listen(io.StringIO("INITREMOTE"))
        self.remote.initremote.assert_called_once()
        self.assertEqual(self.last_line(self.output), "INITREMOTE-FAILURE ErrorMsg")  
        
    def TestInitremoteFailureNoMessage(self):
        self.remote.initremote.return_value = False
        self.annex.Listen(io.StringIO("INITREMOTE"))
        self.remote.initremote.assert_called_once()
        self.assertEqual(self.last_line(self.output), "INITREMOTE-FAILURE")       

    def TestPrepareSuccess(self):
        self.remote.prepare.return_value = True
        self.annex.Listen(io.StringIO("PREPARE"))
        self.remote.prepare.assert_called_once()
        self.assertEqual(self.last_line(self.output), "PREPARE-SUCCESS")
        
    def TestPrepareFailure(self):
        self.remote.prepare.return_value = Error("ErrorMsg")
        self.annex.Listen(io.StringIO("PREPARE"))
        self.remote.prepare.assert_called_once()
        self.assertEqual(self.last_line(self.output), "PREPARE-FAILURE ErrorMsg")
        
    def TestPrepareFailureNoMessage(self):
        self.remote.prepare.return_value = False
        self.annex.Listen(io.StringIO("PREPARE"))
        self.remote.prepare.assert_called_once()
        self.assertEqual(self.last_line(self.output), "PREPARE-FAILURE")

    def TestTransferStoreSuccess(self):
        self.remote.transfer_store.return_value = True
        self.annex.Listen(io.StringIO("TRANSFER STORE Key File"))
        self.remote.transfer_store.assert_called_once_with("Key", "File")
        self.assertEqual(self.last_line(self.output), "TRANSFER-SUCCESS STORE Key")
        
    def TestTransferStoreFailure(self):
        self.remote.transfer_store.return_value = False
        self.annex.Listen(io.StringIO("TRANSFER STORE Key File"))
        self.remote.transfer_store.assert_called_once_with("Key", "File")
        self.assertEqual(self.last_line(self.output), "TRANSFER-FAILURE STORE Key")

    def TestTransferStoreMissingFilename(self):
        with self.assertRaises(SyntaxError):
            self.annex.Listen(io.StringIO("TRANSFER STORE Key"))

    def TestTransferStore_SpaceInFilename(self):
        self.annex.Listen(io.StringIO("TRANSFER STORE Key File with spaces"))
        self.remote.transfer_store.assert_called_once_with("Key", "File with spaces")

    def TestTransferRetrieveSuccess(self):
        self.remote.transfer_retrieve.return_value = True
        self.annex.Listen(io.StringIO("TRANSFER RETRIEVE Key File"))
        self.remote.transfer_retrieve.assert_called_once_with("Key", "File")
        self.assertEqual(self.last_line(self.output), "TRANSFER-SUCCESS RETRIEVE Key")
        
    def TestTransferRetrieveFailure(self):
        self.remote.transfer_retrieve.return_value = False
        self.annex.Listen(io.StringIO("TRANSFER RETRIEVE Key File"))
        self.remote.transfer_retrieve.assert_called_once_with("Key", "File")
        self.assertEqual(self.last_line(self.output), "TRANSFER-FAILURE RETRIEVE Key")

    def TestTransferRetrieve_MissingFilename(self):
        with self.assertRaises(SyntaxError):
            self.annex.Listen(io.StringIO("TRANSFER RETRIEVE Key"))

    def TestTransferRetrieve_SpaceInFilename(self):
        self.annex.Listen(io.StringIO("TRANSFER RETRIEVE Key File with spaces"))
        self.remote.transfer_retrieve.assert_called_once_with("Key", "File with spaces")

    def TestCheckpresentSuccess(self):
        self.remote.checkpresent.return_value = True
        self.annex.Listen(io.StringIO("CHECKPRESENT Key"))
        self.remote.checkpresent.assert_called_once_with("Key")
        self.assertEqual(self.last_line(self.output), "CHECKPRESENT-SUCCESS Key")
        
    def TestCheckpresentFailure(self):
        self.remote.checkpresent.return_value = False
        self.annex.Listen(io.StringIO("CHECKPRESENT Key"))
        self.remote.checkpresent.assert_called_once_with("Key")
        self.assertEqual(self.last_line(self.output), "CHECKPRESENT-FAILURE Key")

    def TestCheckpresentUnknown(self):
        self.remote.checkpresent.return_value = Error("ErrorMsg")
        self.annex.Listen(io.StringIO("CHECKPRESENT Key"))
        self.remote.checkpresent.assert_called_once_with("Key")
        self.assertEqual(self.last_line(self.output), "CHECKPRESENT-UNKNOWN Key ErrorMsg")

    def TestRemoveSuccess(self):
        self.remote.remove.return_value = True
        self.annex.Listen(io.StringIO("REMOVE Key"))
        self.remote.remove.assert_called_once_with("Key")
        self.assertEqual(self.last_line(self.output), "REMOVE-SUCCESS Key")
        
    def TestRemoveFailure(self):
        self.remote.remove.return_value = Error("ErrorMsg")
        self.annex.Listen(io.StringIO("REMOVE Key"))
        self.remote.remove.assert_called_once_with("Key")
        self.assertEqual(self.last_line(self.output), "REMOVE-FAILURE Key ErrorMsg")
        
    def TestRemoveFailureNoMessage(self):
        self.remote.remove.return_value = False
        self.annex.Listen(io.StringIO("REMOVE Key"))
        self.remote.remove.assert_called_once_with("Key")
        self.assertEqual(self.last_line(self.output), "REMOVE-FAILURE Key")

    def TestGetcost(self):
        self.remote.getcost.return_value = 5
        self.annex.Listen(io.StringIO("GETCOST"))
        self.remote.getcost.assert_called_once()
        self.assertEqual(self.last_line(self.output), "COST 5")

    def TestGetcostUnsupported(self):
        with self.assertRaises(UnsupportedRequest):
            self.annex.Listen(io.StringIO("GETCOST"))

    def TestGetavailabilityGlobal(self):
        self.remote.getavailability.return_value = "global"
        self.annex.Listen(io.StringIO("GETAVAILABILITY"))
        self.remote.getavailability.assert_called_once()
        self.assertEqual(self.last_line(self.output), "AVAILABILITY GLOBAL")

    def TestGetavailabilityLocal(self):
        self.remote.getavailability.return_value = "local"
        self.annex.Listen(io.StringIO("GETAVAILABILITY"))
        self.remote.getavailability.assert_called_once()
        self.assertEqual(self.last_line(self.output), "AVAILABILITY LOCAL")

    def TestGetavailabilityInvalid(self):
        self.remote.getavailability.return_value = "something else"
        with self.assertRaises(ValueError):
            self.annex.Listen(io.StringIO("GETAVAILABILITY"))

    def TestGetavailabilityUnsupported(self):
        with self.assertRaises(UnsupportedRequest):
            self.annex.Listen(io.StringIO("GETAVAILABILITY"))

    def TestClaimurlSuccess(self):
        self.remote.claimurl.return_value = True
        self.annex.Listen(io.StringIO("CLAIMURL Url"))
        self.remote.claimurl.assert_called_once_with("Url")
        self.assertEqual(self.last_line(self.output), "CLAIMURL-SUCCESS")

    def TestClaimurlFailure(self):
        self.remote.claimurl.return_value = False
        self.annex.Listen(io.StringIO("CLAIMURL Url"))
        self.remote.claimurl.assert_called_once_with("Url")
        self.assertEqual(self.last_line(self.output), "CLAIMURL-FAILURE")
        
    def TestClaimurlUnsupported(self):
        with self.assertRaises(UnsupportedRequest):
            self.annex.Listen(io.StringIO("CLAIMURL Url"))

    def TestCheckurlContents(self):
        self.remote.checkurl.return_value = (512, "Filename")
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")
        self.assertEqual(self.last_line(self.output), "CHECKURL-CONTENTS 512 Filename")

    def TestCheckurlContentsUnknownSize(self):
        self.remote.checkurl.return_value = (None, "Filename")
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")
        self.assertEqual(self.last_line(self.output), "CHECKURL-CONTENTS UNKNOWN Filename")

    def TestCheckurlContentsWithoutFilename(self):
        self.remote.checkurl.return_value = (512)
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")
        self.assertEqual(self.last_line(self.output), "CHECKURL-CONTENTS 512")

    def TestCheckurlMultiTwoUrls(self):
        urllist = [("Url1", 512, "Filename1"),
                   ("Url2", None, "Filename2")]
        self.remote.checkurl.return_value = urllist
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")
        self.assertEqual(self.last_line(self.output), "CHECKURL-MULTI Url1 512 Filename1 Url2 UNKNOWN Filename2")

    def TestCheckurlMultiFiveUrls(self):
        urllist = [("Url1", 512, "Filename1"),
                   ("Url2", None, "Filename2"),
                   ("Url3", 1024, "Filename3"),
                   ("Url4", 134789, "Filename4"),
                   ("Url5", None, "Filename5")]
        self.remote.checkurl.return_value = urllist
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")
        self.assertEqual(self.last_line(self.output), "CHECKURL-MULTI Url1 512 Filename1 Url2 UNKNOWN Filename2 Url3 1024 Filename3 Url4 134789 Filename4 Url5 UNKNOWN Filename5")

    def TestCheckurlFailure(self):
        self.remote.checkurl.return_value = False
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")
        self.assertEqual(self.last_line(self.output), "CHECKURL-FAILURE")

    def TestWhereisSuccess(self):
        self.remote.checkurl.return_value = "String"
        self.annex.Listen(io.StringIO("WHEREIS Key"))
        self.remote.whereis.assert_called_once_with("Key")
        self.assertEqual(self.last_line(self.output), "WHEREIS-SUCCESS String")

    def TestWhereisFailure(self):
        self.remote.checkurl.return_value = False
        self.annex.Listen(io.StringIO("WHEREIS Key"))
        self.remote.whereis.assert_called_once_with("Key")
        self.assertEqual(self.last_line(self.output), "WHEREIS-FAILURE")


class TestGitAnnexRequestMessagesExporttree(utils.GitAnnexTestCase):
    def TestExportsupportedSuccess(self):
        self.remote.exportsupported.return_value = True
        self.annex.Listen(io.StringIO("EXPORTSUPPORTED"))
        self.remote.exportsupported.assert_called_once()
        self.assertEqual(self.last_line(self.output), "EXPORTSUPPORTED-SUCCESS")
        
    def TestExportsupportedFailure(self):
        self.remote.exportsupported.return_value = False
        self.annex.Listen(io.StringIO("EXPORTSUPPORTED"))
        self.remote.exportsupported.assert_called_once()
        self.assertEqual(self.last_line(self.output), "EXPORTSUPPORTED-FAILURE")

    def TestExport(self):
        self.annex.Listen(io.StringIO("EXPORT Name"))
        self.remote.export.assert_called_once_with("Name")

    def TestExport_MissingName(self):
        with self.assertRaises(SyntaxError):
            self.annex.Listen(io.StringIO("EXPORT"))

    def TestExport_SpaceInName(self):
        self.annex.Listen(io.StringIO("EXPORT Name with spaces"))
        self.remote.export.assert_called_once_with("Name with spaces")
    
    def TestTransferexportStoreSuccess(self):
        self.remote.transferexport_store.return_value = True
        self.annex.Listen(io.StringIO("TRANSFEREXPORT STORE Key File"))
        self.remote.transferexport_store.assert_called_once_with("Key", "File")
        self.assertEqual(self.last_line(self.output), "TRANSFER-SUCCESS STORE Key")
        
    def TestTransferexportStoreFailure(self):
        self.remote.transferexport_store.return_value = False
        self.annex.Listen(io.StringIO("TRANSFEREXPORT STORE Key File"))
        self.remote.transferexport_store.assert_called_once_with("Key", "File")
        self.assertEqual(self.last_line(self.output), "TRANSFER-FAILURE STORE Key")

    def TestTransferexportStore_MissingFilename(self):
        with self.assertRaises(SyntaxError):
            self.annex.Listen(io.StringIO("TRANSFEREXPORT STORE Key"))

    def TestTransferexportStore_SpaceInFilename(self):
        self.annex.Listen(io.StringIO("TRANSFEREXPORT STORE Key File with spaces"))
        self.remote.transferexport_store.assert_called_once_with("Key", "File with spaces")

    def TestTransferexportRetrieveSuccess(self):
        self.remote.transferexport_retrieve.return_value = True
        self.annex.Listen(io.StringIO("TRANSFEREXPORT RETRIEVE Key File"))
        self.remote.transferexport_retrieve.assert_called_once_with("Key", "File")
        self.assertEqual(self.last_line(self.output), "TRANSFER-SUCCESS RETRIEVE Key")
        
    def TestTransferexportRetrieveFailure(self):
        self.remote.transferexport_retrieve.return_value = False
        self.annex.Listen(io.StringIO("TRANSFEREXPORT RETRIEVE Key File"))
        self.remote.transferexport_retrieve.assert_called_once_with("Key", "File")
        self.assertEqual(self.last_line(self.output), "TRANSFER-FAILURE RETRIEVE Key")
        
    def TestTransferexportRetrieve_MissingFilename(self):
        with self.assertRaises(SyntaxError):
            self.annex.Listen(io.StringIO("TRANSFEREXPORT RETRIEVE Key"))

    def TestTransferexportRetrieve_SpaceInFilename(self):
        self.annex.Listen(io.StringIO("TRANSFEREXPORT RETRIEVE Key File with spaces"))
        self.remote.transferexport_retrieve.assert_called_once_with("Key", "File with spaces")

    def TestCheckpresentexportSuccess(self):
        self.remote.checkpresentexport.return_value = True
        self.annex.Listen(io.StringIO("CHECKPRESENT Key"))
        self.remote.checkpresentexport.assert_called_once_with("Key")
        self.assertEqual(self.last_line(self.output), "CHECKPRESENT-SUCCESS Key")
        
    def TestCheckpresentexportFailure(self):
        self.remote.checkpresentexport.return_value = False
        self.annex.Listen(io.StringIO("CHECKPRESENT Key"))
        self.remote.checkpresentexport.assert_called_once_with("Key")
        self.assertEqual(self.last_line(self.output), "CHECKPRESENT-FAILURE Key")

    def TestCheckpresentexportUnknown(self):
        self.remote.checkpresentexport.return_value = Error("ErrorMsg")
        self.annex.Listen(io.StringIO("CHECKPRESENT Key"))
        self.remote.checkpresentexport.assert_called_once_with("Key")
        self.assertEqual(self.last_line(self.output), "CHECKPRESENT-UNKNOWN Key ErrorMsg")
        
    def TestRemoveexportSuccess(self):
        self.remote.removeexport.return_value = True
        self.annex.Listen(io.StringIO("REMOVE Key"))
        self.remote.removeexport.assert_called_once_with("Key")
        self.assertEqual(self.last_line(self.output), "REMOVE-SUCCESS Key")
        
    def TestRemoveexportFailure(self):
        self.remote.removeexport.return_value = Error("ErrorMsg")
        self.annex.Listen(io.StringIO("REMOVE Key"))
        self.remote.removeexport.assert_called_once_with("Key")
        self.assertEqual(self.last_line(self.output), "REMOVE-FAILURE Key ErrorMsg")
        
    def TestRemoveexportdirectorySuccess(self):
        self.remote.removeexportdirectory.return_value = True
        self.annex.Listen(io.StringIO("REMOVEEXPORTDIRECTORY Directory"))
        self.remote.removeexportdirectory.assert_called_once_with("Directory")
        self.assertEqual(self.last_line(self.output), "REMOVEEXPORTDIRECTORY-SUCCESS")

    def TestRemoveexportdirectoryFailure(self):
        self.remote.removeexportdirectory.return_value = False
        self.annex.Listen(io.StringIO("REMOVEEXPORTDIRECTORY Directory"))
        self.remote.removeexportdirectory.assert_called_once_with("Directory")
        self.assertEqual(self.last_line(self.output), "REMOVEEXPORTDIRECTORY-FAILURE")

    def TestRemoveexportdirectory_MissingDirectory(self):
        with self.assertRaises(SyntaxError):
            self.annex.Listen(io.StringIO("REMOVEEXPORTDIRECTORY"))

    def TestRemoveexportdirectory_SpaceInFilename(self):
        self.annex.Listen(io.StringIO("REMOVEEXPORTDIRECTORY Directory with spaces"))
        self.remote.removeexportdirectory.assert_called_once_with("Directory with spaces")
    
    def TestRenameexportSuccess(self):
        self.remote.renameexport.return_value = True
        self.annex.Listen(io.StringIO("RENAMEEXPORT Key NewName"))
        self.remote.renameexport.assert_called_once_with("Key", "NewName")
        self.assertEqual(self.last_line(self.output), "RENAMEEXPORT-SUCCESS Key")
    
    def TestRenameexportFailure(self):
        self.remote.renameexport.return_value = False
        self.annex.Listen(io.StringIO("RENAMEEXPORT Key NewName"))
        self.remote.renameexport.assert_called_once_with("Key", "NewName")
        self.assertEqual(self.last_line(self.output), "RENAMEEXPORT-FAILURE Key")
    
    def TestRenameexport_MissingNewName(self):
        with self.assertRaises(SyntaxError):
            self.annex.Listen(io.StringIO("RENAMEEXPORT Key"))
    
    def TestRenameexport_SpaceInNewName(self):
        self.annex.Listen(io.StringIO("RENAMEEXPORT Key NewName with spaces"))
        self.remote.renameexport.assert_called_once_with("Key", "NewName with spaces")
        
    def TestUnsupportedRequest(self):
        self.annex.Listen(io.StringIO("Not a request"))
        self.assertEqual(self.last_line(self.output), "UNSUPPORTED-REQUEST")
