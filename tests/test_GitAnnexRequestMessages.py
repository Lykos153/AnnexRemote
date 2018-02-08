import io
from unittest import skip

import utils
from AnnexRemote import RemoteError
from AnnexRemote import ProtocolError
from AnnexRemote import UnsupportedRequest

class TestGitAnnexRequestMessages(utils.GitAnnexTestCase):

    def last_line(self, buffer):
        current_position = buffer.tell()
        buffer.seek(0)
        lines = buffer.readlines()
        buffer.seek(current_position)
        return lines[-1].rstrip("\n")
        
    def TestInitremoteSuccess(self):
        self.annex.Listen(io.StringIO("INITREMOTE"))
        self.remote.initremote.assert_called_once()
        self.assertEqual(self.last_line(self.output), "INITREMOTE-SUCCESS")
        
    def TestInitremoteFailure(self):
        self.remote.initremote.side_effect = RemoteError("ErrorMsg")
        self.annex.Listen(io.StringIO("INITREMOTE"))
        self.remote.initremote.assert_called_once()
        self.assertEqual(self.last_line(self.output), "INITREMOTE-FAILURE ErrorMsg")  
        
    def TestPrepareSuccess(self):
        self.annex.Listen(io.StringIO("PREPARE"))
        self.remote.prepare.assert_called_once()
        self.assertEqual(self.last_line(self.output), "PREPARE-SUCCESS")
        
    def TestPrepareFailure(self):
        self.remote.prepare.side_effect = RemoteError("ErrorMsg")
        self.annex.Listen(io.StringIO("PREPARE"))
        self.remote.prepare.assert_called_once()
        self.assertEqual(self.last_line(self.output), "PREPARE-FAILURE ErrorMsg")
                
    def TestTransferStoreSuccess(self):
        self.annex.Listen(io.StringIO("TRANSFER STORE Key File"))
        self.remote.transfer_store.assert_called_once_with("Key", "File")
        self.assertEqual(self.last_line(self.output), "TRANSFER-SUCCESS STORE Key")
        
    def TestTransferStoreFailure(self):
        self.remote.transfer_store.side_effect = RemoteError("ErrorMsg")
        self.annex.Listen(io.StringIO("TRANSFER STORE Key File"))
        self.remote.transfer_store.assert_called_once_with("Key", "File")
        self.assertEqual(self.last_line(self.output), "TRANSFER-FAILURE STORE Key ErrorMsg")

    def TestTransferStoreMissingFilename(self):
        with self.assertRaises(SyntaxError):
            self.annex.Listen(io.StringIO("TRANSFER STORE Key"))

    def TestTransferStore_SpaceInFilename(self):
        self.annex.Listen(io.StringIO("TRANSFER STORE Key File with spaces"))
        self.remote.transfer_store.assert_called_once_with("Key", "File with spaces")

    def TestTransferRetrieveSuccess(self):
        self.annex.Listen(io.StringIO("TRANSFER RETRIEVE Key File"))
        self.remote.transfer_retrieve.assert_called_once_with("Key", "File")
        self.assertEqual(self.last_line(self.output), "TRANSFER-SUCCESS RETRIEVE Key")
        
    def TestTransferRetrieveFailure(self):
        self.remote.transfer_retrieve.side_effect = RemoteError("ErrorMsg")
        self.annex.Listen(io.StringIO("TRANSFER RETRIEVE Key File"))
        self.remote.transfer_retrieve.assert_called_once_with("Key", "File")
        self.assertEqual(self.last_line(self.output), "TRANSFER-FAILURE RETRIEVE Key ErrorMsg")

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
        self.remote.checkpresent.side_effect = RemoteError("ErrorMsg")
        self.annex.Listen(io.StringIO("CHECKPRESENT Key"))
        self.remote.checkpresent.assert_called_once_with("Key")
        self.assertEqual(self.last_line(self.output), "CHECKPRESENT-UNKNOWN Key ErrorMsg")

    def TestRemoveSuccess(self):
        self.annex.Listen(io.StringIO("REMOVE Key"))
        self.remote.remove.assert_called_once_with("Key")
        self.assertEqual(self.last_line(self.output), "REMOVE-SUCCESS Key")
        
    def TestRemoveFailure(self):
        self.remote.remove.side_effect = RemoteError("ErrorMsg")
        self.annex.Listen(io.StringIO("REMOVE Key"))
        self.remote.remove.assert_called_once_with("Key")
        self.assertEqual(self.last_line(self.output), "REMOVE-FAILURE Key ErrorMsg")
                
    def TestGetcost(self):
        self.remote.getcost.return_value = 5
        self.annex.Listen(io.StringIO("GETCOST"))
        self.remote.getcost.assert_called_once()
        self.assertEqual(self.last_line(self.output), "COST 5")

    def TestGetcostInvalid(self):
        self.remote.getcost.return_value = "not a number"
        with self.assertRaises(ValueError):
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

    def TestClaimurlSuccess(self):
        self.remote.claimurl.return_value = True
        self.annex.Listen(io.StringIO("CLAIMURL Url"))
        self.remote.claimurl.assert_called_once_with("Url")
        self.assertEqual(self.last_line(self.output), "CLAIMURL-SUCCESS")

    def TestClaimurlFailure(self):
        self.remote.claimurl.return_value = False
        self.annex.Listen(io.StringIO("CLAIMURL Url"))
        self.assertEqual(self.last_line(self.output), "CLAIMURL-FAILURE")
        
    def TestCheckurlContents(self):
        self.remote.checkurl.return_value = [{'size':512,'filename':"Filename"}]
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")
        self.assertEqual(self.last_line(self.output), "CHECKURL-CONTENTS 512 Filename")
        
    def TestCheckurlContentsUnknownSize(self):
        self.remote.checkurl.return_value = [{'filename':"Filename"}]
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")
        self.assertEqual(self.last_line(self.output), "CHECKURL-CONTENTS UNKNOWN Filename")
        
    def TestCheckurlContentsWithoutFilename(self):
        self.remote.checkurl.return_value = [{'size':512}]
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")
        self.assertEqual(self.last_line(self.output), "CHECKURL-CONTENTS 512")
        
    def TestCheckurlContentsWithoutSizeAndFilename(self):
        self.remote.checkurl.return_value = True
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")
        self.assertEqual(self.last_line(self.output), "CHECKURL-CONTENTS UNKNOWN")
        
    def TestCheckurlMultiTwoUrls(self):
        urllist = [{'url':"Url1", 'size':512, 'filename':"Filename1"},
                   {'url':"Url2", 'filename':"Filename2"}]
        self.remote.checkurl.return_value = urllist
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")
        self.assertEqual(self.last_line(self.output), "CHECKURL-MULTI Url1 512 Filename1 Url2 UNKNOWN Filename2")
        
    def TestCheckurlMultiFiveUrls(self):
        urllist = [{'url':"Url1", 'size':512,   'filename':"Filename1"},
                   {'url':"Url2",               'filename':"Filename2"},
                   {'url':"Url3", 'size':1024},
                   {'url':"Url4", 'size':134789,'filename':"Filename4"},
                   {'url':"Url5",               'filename':"Filename5"}]
        self.remote.checkurl.return_value = urllist
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")
        self.assertEqual(self.last_line(self.output), "CHECKURL-MULTI Url1 512 Filename1 Url2 UNKNOWN Filename2 Url3 1024  Url4 134789 Filename4 Url5 UNKNOWN Filename5")
        
    def TestCheckurlMultiSpaceInUrl(self):
        urllist = [{'url':"Url with spaces", 'size':512, 'filename':"Filename1"},
                   {'url':"Url2",'filename':"Filename2"}]
        self.remote.checkurl.return_value = urllist
        with self.assertRaises(ValueError):
            self.annex.Listen(io.StringIO("CHECKURL Url"))
        
    def TestCheckurlMultiSpaceInFilename(self):
        urllist = [{'url':"Url1", 'size':512, 'filename':"Filename with spaces"},
                   {'url':"Url2", 'filename':"Filename2"}]
        self.remote.checkurl.return_value = urllist
        with self.assertRaises(ValueError):
            self.annex.Listen(io.StringIO("CHECKURL Url"))
        
    def TestCheckurlFailure(self):
        self.remote.checkurl.side_effect = RemoteError()
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")
        self.assertEqual(self.last_line(self.output), "CHECKURL-FAILURE")

    def TestCheckurlFailureByException(self):
        self.remote.checkurl.return_value = False
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")
        self.assertEqual(self.last_line(self.output), "CHECKURL-FAILURE")

    def TestWhereisSuccess(self):
        self.remote.whereis.return_value = "String"
        self.annex.Listen(io.StringIO("WHEREIS Key"))
        self.remote.whereis.assert_called_once_with("Key")
        self.assertEqual(self.last_line(self.output), "WHEREIS-SUCCESS String")

    def TestWhereisFailure(self):
        self.remote.whereis.return_value = False
        self.annex.Listen(io.StringIO("WHEREIS Key"))
        self.remote.whereis.assert_called_once_with("Key")
        self.assertEqual(self.last_line(self.output), "WHEREIS-FAILURE")

class TestGitAnnexRequestMessagesExporttree(TestGitAnnexRequestMessages):
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

    def TestExport_MissingName(self):
        with self.assertRaises(SyntaxError):
            self.annex.Listen(io.StringIO("EXPORT"))

    def TestExport_SpaceInName(self):
        # testing this only with TRANSFEREXPORT
        self.annex.Listen(io.StringIO("EXPORT Name with spaces\nTRANSFEREXPORT STORE Key File"))
        self.remote.transferexport_store.assert_called_once_with("Key", "File", "Name with spaces")
    
    def TestTransferexportStoreSuccess(self):
        self.annex.Listen(io.StringIO("EXPORT Name\nTRANSFEREXPORT STORE Key File"))
        self.remote.transferexport_store.assert_called_once_with("Key", "File", "Name")
        self.assertEqual(self.last_line(self.output), "TRANSFER-SUCCESS STORE Key")
        
    def TestTransferexportStoreFailure(self):
        self.remote.transferexport_store.side_effect = RemoteError("ErrorMsg")
        self.annex.Listen(io.StringIO("EXPORT Name\nTRANSFEREXPORT STORE Key File"))
        self.remote.transferexport_store.assert_called_once_with("Key", "File", "Name")
        self.assertEqual(self.last_line(self.output), "TRANSFER-FAILURE STORE Key ErrorMsg")

    def TestTransferexportStore_WithoutExport(self):
        with self.assertRaises(ProtocolError):
            self.annex.Listen(io.StringIO("TRANSFEREXPORT STORE Key"))

    def TestTransferexportStore_MissingFilename(self):
        with self.assertRaises(SyntaxError):
            self.annex.Listen(io.StringIO("EXPORT Name\nTRANSFEREXPORT STORE Key"))

    def TestTransferexportStore_SpaceInFilename(self):
        self.annex.Listen(io.StringIO("EXPORT Name\nTRANSFEREXPORT STORE Key File with spaces"))
        self.remote.transferexport_store.assert_called_once_with("Key", "File with spaces", "Name")

    def TestTransferexportRetrieveSuccess(self):
        self.annex.Listen(io.StringIO("EXPORT Name\nTRANSFEREXPORT RETRIEVE Key File"))
        self.remote.transferexport_retrieve.assert_called_once_with("Key", "File", "Name")
        self.assertEqual(self.last_line(self.output), "TRANSFER-SUCCESS RETRIEVE Key")
        
    def TestTransferexportRetrieveFailure(self):
        self.remote.transferexport_retrieve.side_effect = RemoteError("ErrorMsg")
        self.annex.Listen(io.StringIO("EXPORT Name\nTRANSFEREXPORT RETRIEVE Key File"))
        self.remote.transferexport_retrieve.assert_called_once_with("Key", "File", "Name")
        self.assertEqual(self.last_line(self.output), "TRANSFER-FAILURE RETRIEVE Key ErrorMsg")
        
    def TestTransferexportRetrieve_WithoutExport(self):
        with self.assertRaises(ProtocolError):
            self.annex.Listen(io.StringIO("TRANSFEREXPORT RETRIEVE Key"))

    def TestTransferexportRetrieve_MissingFilename(self):
        with self.assertRaises(SyntaxError):
            self.annex.Listen(io.StringIO("EXPORT Name\nTRANSFEREXPORT RETRIEVE Key"))

    def TestTransferexportRetrieve_SpaceInFilename(self):
        self.annex.Listen(io.StringIO("EXPORT Name\nTRANSFEREXPORT RETRIEVE Key File with spaces"))
        self.remote.transferexport_retrieve.assert_called_once_with("Key", "File with spaces", "Name")

    def TestCheckpresentexportSuccess(self):
        self.remote.checkpresentexport.return_value = True
        self.annex.Listen(io.StringIO("EXPORT Name\nCHECKPRESENTEXPORT Key"))
        self.remote.checkpresentexport.assert_called_once_with("Key", "Name")
        self.assertEqual(self.last_line(self.output), "CHECKPRESENT-SUCCESS Key")
        
    def TestCheckpresentexportFailure(self):
        self.remote.checkpresentexport.return_value = False
        self.annex.Listen(io.StringIO("EXPORT Name\nCHECKPRESENTEXPORT Key"))
        self.remote.checkpresentexport.assert_called_once_with("Key", "Name")
        self.assertEqual(self.last_line(self.output), "CHECKPRESENT-FAILURE Key")

    def TestCheckpresentexportUnknown(self):
        self.remote.checkpresentexport.side_effect=RemoteError("ErrorMsg")
        self.annex.Listen(io.StringIO("EXPORT Name\nCHECKPRESENTEXPORT Key"))
        self.remote.checkpresentexport.assert_called_once_with("Key", "Name")
        self.assertEqual(self.last_line(self.output), "CHECKPRESENT-UNKNOWN Key ErrorMsg")
    
    def TestCheckpresentexport_WithoutExport(self):
        with self.assertRaises(ProtocolError):
            self.annex.Listen(io.StringIO("CHECKPRESENTEXPORT Key"))

    def TestRemoveexportSuccess(self):
        self.annex.Listen(io.StringIO("EXPORT Name\nREMOVEEXPORT Key"))
        self.remote.removeexport.assert_called_once_with("Key", "Name")
        self.assertEqual(self.last_line(self.output), "REMOVE-SUCCESS Key")
        
    def TestRemoveexportFailure(self):
        self.remote.removeexport.side_effect = RemoteError("ErrorMsg")
        self.annex.Listen(io.StringIO("EXPORT Name\nREMOVEEXPORT Key"))
        self.remote.removeexport.assert_called_once_with("Key", "Name")
        self.assertEqual(self.last_line(self.output), "REMOVE-FAILURE Key ErrorMsg")
        
    def TestRemoveexport_WithoutExport(self):
        with self.assertRaises(ProtocolError):
            self.annex.Listen(io.StringIO("REMOVEEXPORT Key"))

    def TestRemoveexportdirectorySuccess(self):
        self.annex.Listen(io.StringIO("REMOVEEXPORTDIRECTORY Directory"))
        self.remote.removeexportdirectory.assert_called_once_with("Directory")
        self.assertEqual(self.last_line(self.output), "REMOVEEXPORTDIRECTORY-SUCCESS")

    def TestRemoveexportdirectoryFailure(self):
        self.remote.removeexportdirectory.side_effect = RemoteError()
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
        self.annex.Listen(io.StringIO("EXPORT Name\nRENAMEEXPORT Key NewName"))
        self.remote.renameexport.assert_called_once_with("Key", "Name", "NewName")
        self.assertEqual(self.last_line(self.output), "RENAMEEXPORT-SUCCESS Key")
    
    def TestRenameexportFailure(self):
        self.remote.renameexport.side_effect = RemoteError()
        self.annex.Listen(io.StringIO("EXPORT Name\nRENAMEEXPORT Key NewName"))
        self.remote.renameexport.assert_called_once_with("Key", "Name", "NewName")
        self.assertEqual(self.last_line(self.output), "RENAMEEXPORT-FAILURE Key")
    
    def TestRenameexport_WithoutExport(self):
        with self.assertRaises(ProtocolError):
            self.annex.Listen(io.StringIO("RENAMEEXPORT Key NewName"))

    def TestRenameexport_MissingNewName(self):
        with self.assertRaises(SyntaxError):
            self.annex.Listen(io.StringIO("EXPORT Name\nRENAMEEXPORT Key"))
    
    def TestRenameexport_SpaceInNewName(self):
        self.annex.Listen(io.StringIO("EXPORT Name\nRENAMEEXPORT Key NewName with spaces"))
        self.remote.renameexport.assert_called_once_with("Key", "Name", "NewName with spaces")
        
    def TestUnsupportedRequest(self):
        self.annex.Listen(io.StringIO("Not a request"))
        self.assertEqual(self.last_line(self.output), "UNSUPPORTED-REQUEST")
