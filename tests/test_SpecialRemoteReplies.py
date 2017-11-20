import unittest
import AnnexRemote

class TestSpecialRemoteReplies(unittest.TestCase):
    def TestPrepareSuccess(self):
        reply = AnnexRemote.Reply.PrepareSuccess()
        self.assertEqual(str(reply), "PREPARE-SUCCESS")

    def TestPrepareFailure(self):
        reply = AnnexRemote.Reply.PrepareFailure("ErrorMsg")
        self.assertEqual(str(reply), "PREPARE-FAILURE ErrorMsg")

    def TestTransferSuccess_Store(self):
        reply = AnnexRemote.Reply.TransferSuccess_Store("Key")
        self.assertEqual(str(reply), "TRANSFER-SUCCESS STORE Key")

    def TestTransferFailure_Store(self):
        reply = AnnexRemote.Reply.TransferFailure_Store("Key")
        self.assertEqual(str(reply), "TRANSFER-FAILURE STORE Key")

    def TestTransferSuccess_Retrieve(self):
        reply = AnnexRemote.Reply.TransferSuccess_Retrieve("Key")
        self.assertEqual(str(reply), "TRANSFER-SUCCESS RETRIEVE Key")

    def TestTransferFailure_Retrieve(self):
        reply = AnnexRemote.Reply.TransferFailure_Retrieve("Key")
        self.assertEqual(str(reply), "TRANSFER-FAILURE RETRIEVE Key")

    def TestCheckpresentSuccess(self):
        reply = AnnexRemote.Reply.CheckpresentSuccess("Key")
        self.assertEqual(str(reply), "CHECKPRESENT-SUCCESS Key")

    def TestCheckpresentFailure(self):
        reply = AnnexRemote.Reply.CheckpresentFailure("Key")
        self.assertEqual(str(reply), "CHECKPRESENT-FAILURE Key")

    def TestCheckpresentUnknown(self):
        reply = AnnexRemote.Reply.CheckpresentUnknown("Key", "ErrorMsg")
        self.assertEqual(str(reply), "CHECKPRESENT-UNKNOWN Key ErrorMsg")

    def TestRemoveSuccess(self):
        reply = AnnexRemote.Reply.RemoveSuccess("Key")
        self.assertEqual(str(reply), "REMOVE-SUCCESS Key")

    def TestRemoveFailure(self):
        reply = AnnexRemote.Reply.RemoveFailure("Key")
        self.assertEqual(str(reply), "REMOVE-FAILURE Key ErrorMsg")

    def TestCost(self):
        reply = AnnexRemote.Reply.Cost(5)
        self.assertEqual(str(reply), "COST 5")
    
    def TestAvailabilityGlobal(self):
        reply = AnnexRemote.Reply.AvailabilityGlobal()
        self.assertEqual(str(reply), "AVAILABILITY GLOBAL")

    def TestAvailabilityLocal(self):
        reply = AnnexRemote.Reply.AvailabilityLocal()
        self.assertEqual(str(reply), "AVAILABILITY LOCAL")

    def TestInitremoteSuccess(self):
        reply = AnnexRemote.Reply.InitremoteSuccess()
        self.assertEqual(str(reply), "INITREMOTE-SUCCESS")

    def TestInitremoteFailure(self):
        reply = AnnexRemote.Reply.InitremoteFailure("ErrorMsg")
        self.assertEqual(str(reply), "INITREMOTE-FAILURE ErrorMsg")

    def TestClaimurlSuccess(self):
        reply = AnnexRemote.Reply.ClaimurlSuccess()
        self.assertEqual(str(reply), "CLAIMURL-SUCCESS")

    def TestClaimurlFailure(self):
        reply = AnnexRemote.Reply.ClaimurlFailure()
        self.assertEqual(str(reply), "CLAIMURL-FAILURE")

    def TestCheckurlContents(self):
        reply = AnnexRemote.Reply.CheckurlContents(512, "Filename")
        self.assertEqual(str(reply), "CHECKURL-CONTENTS 512 Filename")

    def TestCheckurlContentsUnknownSize(self):
        reply = AnnexRemote.Reply.CheckurlContents(None, "Filename")
        self.assertEqual(str(reply), "CHECKURL-CONTENTS UNKNOWN Filename")

    def TestCheckurlContentsWithoutFilename(self):
        reply = AnnexRemote.Reply.CheckurlContents(512)
        self.assertEqual(str(reply), "CHECKURL-CONTENTS 512")

    def TestCheckurlMultiTwoUrls(self):
        urllist = [("Url1", 512, "Filename1"),
                   ("Url2", None, "Filename2")]
        reply = AnnexRemote.Reply.CheckurlMulti(urllist)
        self.assertEqual(str(reply), "CHECKURL-MULTI Url1 512 Filename1 Url2 UNKNOWN Filename2")

    def TestCheckurlMultiFiveUrls(self):
        urllist = [("Url1", 512, "Filename1"),
                   ("Url2", None, "Filename2"),
                   ("Url3", 1024, "Filename3"),
                   ("Url4", 134789, "Filename4"),
                   ("Url5", None, "Filename5")]
        reply = AnnexRemote.Reply.CheckurlMulti(urllist)
        self.assertEqual(str(reply), "CHECKURL-MULTI Url1 512 Filename1 Url2 UNKNOWN Filename2 Url3 1024 Filename3 Url4 134789 Filename4 Url5 UNKNOWN Filename5")

    def TestCheckurlFailure(self):
        reply = AnnexRemote.Reply.CheckurlFailure()
        self.assertEqual(str(reply), "CHECKURL-FAILURE")

    def TestWhereisSuccess(self):
        reply = AnnexRemote.Reply.WhereisSuccess("String")
        self.assertEqual(str(reply), "WHEREIS-SUCCESS String")

    def TestWhereisFailure(self):
        reply = AnnexRemote.Reply.WhereisFailure()
        self.assertEqual(str(reply), "WHEREIS-FAILURE")

    def TestExportsupportedSuccess(self):
        reply = AnnexRemote.Reply.ExportsupportedSuccess()
        self.assertEqual(str(reply), "EXPORTSUPPORTED-SUCCESS")

    def TestExportsupportedFailure(self):
        reply = AnnexRemote.Reply.ExportsupportedFailure()
        self.assertEqual(str(reply), "EXPORTSUPPORTED-FAILURE")

    def TestRenameexportSuccess(self):
        reply = AnnexRemote.Reply.RenameexportSuccess("Key")
        self.assertEqual(str(reply), "RENAMEEXPORT-SUCCESS Key")

    def TestRenameexportFailure(self):
        reply = AnnexRemote.Reply.RenameexportFailure("Key")
        self.assertEqual(str(reply), "RENAMEEXPORT-FAILURE Key")

    def TestRemoveexportdirectorySuccess(self):
        reply = AnnexRemote.Reply.RemoveexportdirectorySuccess()
        self.assertEqual(str(reply), "REMOVEEXPORTDIRECTORY-SUCCESS")

    def TestRemoveexportdirectoryFailure(self):
        reply = AnnexRemote.Reply.RemoveexportdirectoryFailure()
        self.assertEqual(str(reply), "REMOVEEXPORTDIRECTORY-FAILURE")
    
    def TestUnsupportedRequest(self):
        reply = Annex.Remote.Reply.UnsupportedRequest()
        self.assertEqual(str(reply), "UNSUPPORTED-REQUEST")
