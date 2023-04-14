# -*- coding: utf-8 -*-

import io
import logging

import utils

RemoteError = utils.annexremote.RemoteError
ProtocolError = utils.annexremote.ProtocolError
UnsupportedReqeust = utils.annexremote.UnsupportedRequest


class TestGitAnnexRequestMessages(utils.ExportTestCase):
    def test_InitremoteSuccess(self):
        self.annex.Listen(io.StringIO("INITREMOTE"))
        self.remote.initremote.call_count == 1
        self.assertEqual(utils.second_buffer_line(self.output), "INITREMOTE-SUCCESS")

    def test_InitremoteFailure(self):
        self.remote.initremote.side_effect = RemoteError("ErrorMsg")
        self.annex.Listen(io.StringIO("INITREMOTE"))
        self.remote.initremote.call_count == 1
        self.assertEqual(
            utils.second_buffer_line(self.output), "INITREMOTE-FAILURE ErrorMsg"
        )

    def test_Extensions(self):
        self.annex.Listen(io.StringIO("EXTENSIONS Annex1 Annex2"))
        self.assertEqual(utils.second_buffer_line(self.output), "EXTENSIONS")

    def test_PrepareSuccess(self):
        self.annex.Listen(io.StringIO("PREPARE"))
        self.remote.prepare.call_count == 1
        self.assertEqual(utils.second_buffer_line(self.output), "PREPARE-SUCCESS")

    def test_PrepareFailure(self):
        self.remote.prepare.side_effect = RemoteError("ErrorMsg")
        self.annex.Listen(io.StringIO("PREPARE"))
        self.remote.prepare.call_count == 1
        self.assertEqual(
            utils.second_buffer_line(self.output), "PREPARE-FAILURE ErrorMsg"
        )

    def test_TransferStoreSuccess(self):
        self.annex.Listen(io.StringIO("TRANSFER STORE Key File"))
        self.remote.transfer_store.assert_called_once_with("Key", "File")
        self.assertEqual(
            utils.second_buffer_line(self.output), "TRANSFER-SUCCESS STORE Key"
        )

    def test_TransferStoreFailure(self):
        self.remote.transfer_store.side_effect = RemoteError("ErrorMsg")
        self.annex.Listen(io.StringIO("TRANSFER STORE Key File"))
        self.remote.transfer_store.assert_called_once_with("Key", "File")
        self.assertEqual(
            utils.second_buffer_line(self.output), "TRANSFER-FAILURE STORE Key ErrorMsg"
        )

    def test_TransferStoreMissingFilename(self):
        with self.assertRaises(SystemExit):
            self.annex.Listen(io.StringIO("TRANSFER STORE Key"))
        self.assertEqual(utils.last_buffer_line(self.output), "ERROR Expected Key File")

    def test_TransferStore_SpaceInFilename(self):
        self.annex.Listen(io.StringIO("TRANSFER STORE Key File with spaces"))
        self.remote.transfer_store.assert_called_once_with("Key", "File with spaces")

    def test_TransferRetrieveSuccess(self):
        self.annex.Listen(io.StringIO("TRANSFER RETRIEVE Key File"))
        self.remote.transfer_retrieve.assert_called_once_with("Key", "File")
        self.assertEqual(
            utils.second_buffer_line(self.output), "TRANSFER-SUCCESS RETRIEVE Key"
        )

    def test_TransferRetrieveFailure(self):
        self.remote.transfer_retrieve.side_effect = RemoteError("ErrorMsg")
        self.annex.Listen(io.StringIO("TRANSFER RETRIEVE Key File"))
        self.remote.transfer_retrieve.assert_called_once_with("Key", "File")
        self.assertEqual(
            utils.second_buffer_line(self.output),
            "TRANSFER-FAILURE RETRIEVE Key ErrorMsg",
        )

    def test_TransferRetrieve_MissingFilename(self):
        with self.assertRaises(SystemExit):
            self.annex.Listen(io.StringIO("TRANSFER RETRIEVE Key"))
        self.assertEqual(utils.last_buffer_line(self.output), "ERROR Expected Key File")

    def test_TransferRetrieve_SpaceInFilename(self):
        self.annex.Listen(io.StringIO("TRANSFER RETRIEVE Key File with spaces"))
        self.remote.transfer_retrieve.assert_called_once_with("Key", "File with spaces")

    def test_CheckpresentSuccess(self):
        self.remote.checkpresent.return_value = True
        self.annex.Listen(io.StringIO("CHECKPRESENT Key"))
        self.remote.checkpresent.assert_called_once_with("Key")
        self.assertEqual(
            utils.second_buffer_line(self.output), "CHECKPRESENT-SUCCESS Key"
        )

    def test_CheckpresentFailure(self):
        self.remote.checkpresent.return_value = False
        self.annex.Listen(io.StringIO("CHECKPRESENT Key"))
        self.remote.checkpresent.assert_called_once_with("Key")
        self.assertEqual(
            utils.second_buffer_line(self.output), "CHECKPRESENT-FAILURE Key"
        )

    def test_CheckpresentUnknown(self):
        self.remote.checkpresent.side_effect = RemoteError("ErrorMsg")
        self.annex.Listen(io.StringIO("CHECKPRESENT Key"))
        self.remote.checkpresent.assert_called_once_with("Key")
        self.assertEqual(
            utils.second_buffer_line(self.output), "CHECKPRESENT-UNKNOWN Key ErrorMsg"
        )

    def test_RemoveSuccess(self):
        self.annex.Listen(io.StringIO("REMOVE Key"))
        self.remote.remove.assert_called_once_with("Key")
        self.assertEqual(utils.second_buffer_line(self.output), "REMOVE-SUCCESS Key")

    def test_RemoveFailure(self):
        self.remote.remove.side_effect = RemoteError("ErrorMsg")
        self.annex.Listen(io.StringIO("REMOVE Key"))
        self.remote.remove.assert_called_once_with("Key")
        self.assertEqual(
            utils.second_buffer_line(self.output), "REMOVE-FAILURE Key ErrorMsg"
        )

    def test_Listconfigs(self):
        self.remote.listconfigs.return_value = {
            "Name": "Description",
            "con1": "necessary configuration",
            "opt": "optional configuration",
        }
        self.annex.Listen(io.StringIO("LISTCONFIGS"))
        self.assertEqual(self.remote.listconfigs.call_count, 1)
        self.assertEqual(
            utils.buffer_lines(self.output)[1:],
            [
                "CONFIG Name Description",
                "CONFIG con1 necessary configuration",
                "CONFIG opt optional configuration",
                "CONFIGEND",
            ],
        )

    def test_ListconfigsSpaceInName(self):
        self.remote.listconfigs.return_value = {"Name with space": "Description"}
        with self.assertRaises(SystemExit):
            self.annex.Listen(io.StringIO("LISTCONFIGS"))
        self.assertEqual(
            utils.last_buffer_line(self.output),
            "ERROR Name must not contain space characters: Name with space",
        )

    def test_Getcost(self):
        self.remote.getcost.return_value = 5
        self.annex.Listen(io.StringIO("GETCOST"))
        self.remote.getcost.call_count == 1
        self.assertEqual(utils.second_buffer_line(self.output), "COST 5")

    def test_GetcostInvalid(self):
        self.remote.getcost.return_value = "not a number"
        with self.assertRaises(SystemExit):
            self.annex.Listen(io.StringIO("GETCOST"))
        self.assertEqual(
            utils.last_buffer_line(self.output), "ERROR Cost must be an integer"
        )

    def test_GetavailabilityGlobal(self):
        self.remote.getavailability.return_value = "global"
        self.annex.Listen(io.StringIO("GETAVAILABILITY"))
        self.remote.getavailability.call_count == 1
        self.assertEqual(utils.second_buffer_line(self.output), "AVAILABILITY GLOBAL")

    def test_GetavailabilityLocal(self):
        self.remote.getavailability.return_value = "local"
        self.annex.Listen(io.StringIO("GETAVAILABILITY"))
        self.remote.getavailability.call_count == 1
        self.assertEqual(utils.second_buffer_line(self.output), "AVAILABILITY LOCAL")

    def test_GetavailabilityInvalid(self):
        self.remote.getavailability.return_value = "something else"
        with self.assertRaises(SystemExit):
            self.annex.Listen(io.StringIO("GETAVAILABILITY"))
        self.assertEqual(
            utils.last_buffer_line(self.output),
            "ERROR Availability must be either 'global' or 'local'",
        )

    def test_ClaimurlSuccess(self):
        self.remote.claimurl.return_value = True
        self.annex.Listen(io.StringIO("CLAIMURL Url"))
        self.remote.claimurl.assert_called_once_with("Url")
        self.assertEqual(utils.second_buffer_line(self.output), "CLAIMURL-SUCCESS")

    def test_ClaimurlFailure(self):
        self.remote.claimurl.return_value = False
        self.annex.Listen(io.StringIO("CLAIMURL Url"))
        self.assertEqual(utils.second_buffer_line(self.output), "CLAIMURL-FAILURE")

    def test_CheckurlContentsTrue(self):
        self.remote.checkurl.return_value = True
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")
        self.assertEqual(
            utils.second_buffer_line(self.output), "CHECKURL-CONTENTS UNKNOWN"
        )

    def test_CheckurlContents(self):
        self.remote.checkurl.return_value = [{"size": 512, "filename": "Filename"}]
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")
        self.assertEqual(
            utils.second_buffer_line(self.output), "CHECKURL-CONTENTS 512 Filename"
        )

    def test_CheckurlContentsUnknownSize(self):
        self.remote.checkurl.return_value = [{"filename": "Filename"}]
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")
        self.assertEqual(
            utils.second_buffer_line(self.output), "CHECKURL-CONTENTS UNKNOWN Filename"
        )

    def test_CheckurlContentsWithoutFilename(self):
        self.remote.checkurl.return_value = [{"size": 512}]
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")
        self.assertEqual(utils.second_buffer_line(self.output), "CHECKURL-CONTENTS 512")

    def test_CheckurlContentsWithoutSizeAndFilename(self):
        self.remote.checkurl.return_value = True
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")
        self.assertEqual(
            utils.second_buffer_line(self.output), "CHECKURL-CONTENTS UNKNOWN"
        )

    def test_CheckurlMultiOneItemWithUrl(self):
        self.remote.checkurl.return_value = [
            {"url": "Url_exact", "size": 512, "filename": "Filename"}
        ]
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")
        self.assertEqual(
            utils.second_buffer_line(self.output),
            "CHECKURL-MULTI Url_exact 512 Filename",
        )

    def test_CheckurlMultiTwoUrls(self):
        urllist = [
            {"url": "Url1", "size": 512, "filename": "Filename1"},
            {"url": "Url2", "filename": "Filename2"},
        ]
        self.remote.checkurl.return_value = urllist
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")
        self.assertEqual(
            utils.second_buffer_line(self.output),
            "CHECKURL-MULTI Url1 512 Filename1 Url2 UNKNOWN Filename2",
        )

    def test_CheckurlMultiFiveUrls(self):
        urllist = [
            {"url": "Url1", "size": 512, "filename": "Filename1"},
            {"url": "Url2", "filename": "Filename2"},
            {"url": "Url3", "size": 1024},
            {"url": "Url4", "size": 134789, "filename": "Filename4"},
            {"url": "Url5", "filename": "Filename5"},
        ]
        self.remote.checkurl.return_value = urllist
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")
        self.assertEqual(
            utils.second_buffer_line(self.output),
            "CHECKURL-MULTI Url1 512 Filename1 Url2 UNKNOWN Filename2 Url3 1024  Url4 134789 Filename4 Url5 UNKNOWN Filename5",
        )

    def test_CheckurlMultiSpaceInUrl(self):
        urllist = [
            {"url": "Url with spaces", "size": 512, "filename": "Filename1"},
            {"url": "Url2", "filename": "Filename2"},
        ]
        self.remote.checkurl.return_value = urllist
        with self.assertRaises(SystemExit):
            self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.assertEqual(
            utils.last_buffer_line(self.output), "ERROR Url must not contain spaces."
        )

    def test_CheckurlMultiSpaceInFilename(self):
        urllist = [
            {"url": "Url1", "size": 512, "filename": "Filename with spaces"},
            {"url": "Url2", "filename": "Filename2"},
        ]
        self.remote.checkurl.return_value = urllist
        with self.assertRaises(SystemExit):
            self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.assertEqual(
            utils.last_buffer_line(self.output),
            "ERROR Filename must not contain spaces.",
        )

    def test_CheckurlMultiTabInUrlAndFilename(self):
        urllist = [
            {"url": "Url\twith\ttabs", "size": 512, "filename": "Filename1"},
            {"url": "Url2", "filename": "Filename\twith\ttabs"},
        ]
        self.remote.checkurl.return_value = urllist
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        result = "CHECKURL-MULTI Url\twith\ttabs 512 Filename1 Url2 UNKNOWN Filename\twith\ttabs"
        self.assertEqual(utils.second_buffer_line(self.output), result)

    def test_CheckurlFailure(self):
        self.remote.checkurl.side_effect = RemoteError()
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")
        self.assertEqual(utils.second_buffer_line(self.output), "CHECKURL-FAILURE")

    def test_CheckurlFailureByException(self):
        self.remote.checkurl.return_value = False
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.remote.checkurl.assert_called_once_with("Url")
        self.assertEqual(utils.second_buffer_line(self.output), "CHECKURL-FAILURE")

    def test_WhereisSuccess(self):
        self.remote.whereis.return_value = "String"
        self.annex.Listen(io.StringIO("WHEREIS Key"))
        self.remote.whereis.assert_called_once_with("Key")
        self.assertEqual(
            utils.second_buffer_line(self.output), "WHEREIS-SUCCESS String"
        )

    def test_WhereisFailure(self):
        self.remote.whereis.return_value = False
        self.annex.Listen(io.StringIO("WHEREIS Key"))
        self.remote.whereis.assert_called_once_with("Key")
        self.assertEqual(utils.second_buffer_line(self.output), "WHEREIS-FAILURE")

    def test_Getinfo(self):
        self.remote.info = {"info field 1": "infovalue", "info field 2": "infovalue 2"}
        self.annex.Listen(io.StringIO("GETINFO"))
        self.assertEqual(
            utils.buffer_lines(self.output)[1:],
            [
                "INFOFIELD info field 1",
                "INFOVALUE infovalue",
                "INFOFIELD info field 2",
                "INFOVALUE infovalue 2",
                "INFOEND",
            ],
        )

    def test_GetinfoNone(self):
        self.remote.info = {}
        self.annex.Listen(io.StringIO("GETINFO"))
        self.assertEqual(utils.buffer_lines(self.output)[1:], ["INFOEND"])

    def test_Error(self):
        self.annex.Listen(io.StringIO("ERROR ErrorMsg"))
        self.remote.error.assert_called_once_with("ErrorMsg")


class TestGitAnnexRequestMessagesExporttree(utils.ExportTestCase):
    def test_ExportsupportedSuccess(self):
        self.annex.Listen(io.StringIO("EXPORTSUPPORTED"))
        self.remote.exportsupported.call_count == 1
        self.assertEqual(
            utils.second_buffer_line(self.output), "EXPORTSUPPORTED-SUCCESS"
        )

    def test_ExportsupportedFailure(self):
        self.remote.exportsupported.return_value = False
        self.annex.Listen(io.StringIO("EXPORTSUPPORTED"))
        self.remote.exportsupported.call_count == 1
        self.assertEqual(
            utils.second_buffer_line(self.output), "EXPORTSUPPORTED-FAILURE"
        )

    def test_Export_MissingName(self):
        with self.assertRaises(SystemExit):
            self.annex.Listen(io.StringIO("EXPORT"))
        self.assertRegex(
            utils.last_buffer_line(self.output),
            r"ERROR (Protocol\.|)do_EXPORT\(\) missing 1 required positional argument: 'name'",
        )

    def test_Export_DoubleExport(self):
        with self.assertRaises(SystemExit):
            self.annex.Listen(io.StringIO("EXPORT Name1\nEXPORT Name2"))
        self.assertEqual(utils.last_buffer_line(self.output), "ERROR Unexpected EXPORT")

    def test_Export_SpaceInName(self):
        # testing this only with TRANSFEREXPORT
        self.annex.Listen(
            io.StringIO("EXPORT Name with spaces\nTRANSFEREXPORT STORE Key File")
        )
        self.remote.transferexport_store.assert_called_once_with(
            "Key", "File", "Name with spaces"
        )

    def test_TransferexportStoreSuccess(self):
        self.annex.Listen(io.StringIO("EXPORT Name\nTRANSFEREXPORT STORE Key File"))
        self.remote.transferexport_store.assert_called_once_with("Key", "File", "Name")
        self.assertEqual(
            utils.second_buffer_line(self.output), "TRANSFER-SUCCESS STORE Key"
        )

    def test_TransferexportStoreFailure(self):
        self.remote.transferexport_store.side_effect = RemoteError("ErrorMsg")
        self.annex.Listen(io.StringIO("EXPORT Name\nTRANSFEREXPORT STORE Key File"))
        self.remote.transferexport_store.assert_called_once_with("Key", "File", "Name")
        self.assertEqual(
            utils.second_buffer_line(self.output), "TRANSFER-FAILURE STORE Key ErrorMsg"
        )

    def test_TransferexportStore_WithoutExport(self):
        with self.assertRaises(SystemExit):
            self.annex.Listen(io.StringIO("TRANSFEREXPORT STORE Key"))
        self.assertEqual(
            utils.last_buffer_line(self.output),
            "ERROR Export request without prior EXPORT",
        )

    def test_TransferexportStore_MissingFilename(self):
        with self.assertRaises(SystemExit):
            self.annex.Listen(io.StringIO("EXPORT Name\nTRANSFEREXPORT STORE Key"))
        self.assertEqual(utils.last_buffer_line(self.output), "ERROR Expected Key File")

    def test_TransferexportStore_SpaceInFilename(self):
        self.annex.Listen(
            io.StringIO("EXPORT Name\nTRANSFEREXPORT STORE Key File with spaces")
        )
        self.remote.transferexport_store.assert_called_once_with(
            "Key", "File with spaces", "Name"
        )

    def test_TransferexportStore_SpecialCharacterInName(self):
        self.annex.Listen(
            io.StringIO("EXPORT Näme\nTRANSFEREXPORT STORE Key File with spaces")
        )
        self.remote.transferexport_store.assert_called_once_with(
            "Key", "File with spaces", "Näme"
        )

    def test_TransferexportStore_UnicodeCharacterInName(self):
        self.annex.Listen(
            io.StringIO("EXPORT Name 😀\nTRANSFEREXPORT STORE Key File with spaces")
        )
        self.remote.transferexport_store.assert_called_once_with(
            "Key", "File with spaces", "Name 😀"
        )

    def test_TransferexportRetrieveSuccess(self):
        self.annex.Listen(io.StringIO("EXPORT Name\nTRANSFEREXPORT RETRIEVE Key File"))
        self.remote.transferexport_retrieve.assert_called_once_with(
            "Key", "File", "Name"
        )
        self.assertEqual(
            utils.second_buffer_line(self.output), "TRANSFER-SUCCESS RETRIEVE Key"
        )

    def test_TransferexportRetrieveFailure(self):
        self.remote.transferexport_retrieve.side_effect = RemoteError("ErrorMsg")
        self.annex.Listen(io.StringIO("EXPORT Name\nTRANSFEREXPORT RETRIEVE Key File"))
        self.remote.transferexport_retrieve.assert_called_once_with(
            "Key", "File", "Name"
        )
        self.assertEqual(
            utils.second_buffer_line(self.output),
            "TRANSFER-FAILURE RETRIEVE Key ErrorMsg",
        )

    def test_TransferexportRetrieve_WithoutExport(self):
        with self.assertRaises(SystemExit):
            self.annex.Listen(io.StringIO("TRANSFEREXPORT RETRIEVE Key"))
        self.assertEqual(
            utils.last_buffer_line(self.output),
            "ERROR Export request without prior EXPORT",
        )

    def test_TransferexportRetrieve_MissingFilename(self):
        with self.assertRaises(SystemExit):
            self.annex.Listen(io.StringIO("EXPORT Name\nTRANSFEREXPORT RETRIEVE Key"))
        self.assertEqual(utils.last_buffer_line(self.output), "ERROR Expected Key File")

    def test_TransferexportRetrieve_SpaceInFilename(self):
        self.annex.Listen(
            io.StringIO("EXPORT Name\nTRANSFEREXPORT RETRIEVE Key File with spaces")
        )
        self.remote.transferexport_retrieve.assert_called_once_with(
            "Key", "File with spaces", "Name"
        )

    def test_CheckpresentexportSuccess(self):
        self.remote.checkpresentexport.return_value = True
        self.annex.Listen(io.StringIO("EXPORT Name\nCHECKPRESENTEXPORT Key"))
        self.remote.checkpresentexport.assert_called_once_with("Key", "Name")
        self.assertEqual(
            utils.second_buffer_line(self.output), "CHECKPRESENT-SUCCESS Key"
        )

    def test_CheckpresentexportFailure(self):
        self.remote.checkpresentexport.return_value = False
        self.annex.Listen(io.StringIO("EXPORT Name\nCHECKPRESENTEXPORT Key"))
        self.remote.checkpresentexport.assert_called_once_with("Key", "Name")
        self.assertEqual(
            utils.second_buffer_line(self.output), "CHECKPRESENT-FAILURE Key"
        )

    def test_CheckpresentexportUnknown(self):
        self.remote.checkpresentexport.side_effect = RemoteError("ErrorMsg")
        self.annex.Listen(io.StringIO("EXPORT Name\nCHECKPRESENTEXPORT Key"))
        self.remote.checkpresentexport.assert_called_once_with("Key", "Name")
        self.assertEqual(
            utils.second_buffer_line(self.output), "CHECKPRESENT-UNKNOWN Key ErrorMsg"
        )

    def test_Checkpresentexport_WithoutExport(self):
        with self.assertRaises(SystemExit):
            self.annex.Listen(io.StringIO("CHECKPRESENTEXPORT Key"))
        self.assertEqual(
            utils.last_buffer_line(self.output),
            "ERROR Export request without prior EXPORT",
        )

    def test_RemoveexportSuccess(self):
        self.annex.Listen(io.StringIO("EXPORT Name\nREMOVEEXPORT Key"))
        self.remote.removeexport.assert_called_once_with("Key", "Name")
        self.assertEqual(utils.second_buffer_line(self.output), "REMOVE-SUCCESS Key")

    def test_RemoveexportFailure(self):
        self.remote.removeexport.side_effect = RemoteError("ErrorMsg")
        self.annex.Listen(io.StringIO("EXPORT Name\nREMOVEEXPORT Key"))
        self.remote.removeexport.assert_called_once_with("Key", "Name")
        self.assertEqual(
            utils.second_buffer_line(self.output), "REMOVE-FAILURE Key ErrorMsg"
        )

    def test_Removeexport_WithoutExport(self):
        with self.assertRaises(SystemExit):
            self.annex.Listen(io.StringIO("REMOVEEXPORT Key"))
        self.assertEqual(
            utils.last_buffer_line(self.output),
            "ERROR Export request without prior EXPORT",
        )

    def test_RemoveexportdirectorySuccess(self):
        self.annex.Listen(io.StringIO("REMOVEEXPORTDIRECTORY Directory"))
        self.remote.removeexportdirectory.assert_called_once_with("Directory")
        self.assertEqual(
            utils.second_buffer_line(self.output), "REMOVEEXPORTDIRECTORY-SUCCESS"
        )

    def test_RemoveexportdirectoryFailure(self):
        self.remote.removeexportdirectory.side_effect = RemoteError()
        self.annex.Listen(io.StringIO("REMOVEEXPORTDIRECTORY Directory"))
        self.remote.removeexportdirectory.assert_called_once_with("Directory")
        self.assertEqual(
            utils.second_buffer_line(self.output), "REMOVEEXPORTDIRECTORY-FAILURE"
        )

    def test_Removeexportdirectory_MissingDirectory(self):
        with self.assertRaises(SystemExit):
            self.annex.Listen(io.StringIO("REMOVEEXPORTDIRECTORY"))
        self.assertRegex(
            utils.last_buffer_line(self.output),
            r"ERROR (Protocol\.|)do_REMOVEEXPORTDIRECTORY\(\) missing 1 required positional argument: 'name'",
        )

    def test_Removeexportdirectory_SpaceInFilename(self):
        self.annex.Listen(io.StringIO("REMOVEEXPORTDIRECTORY Directory with spaces"))
        self.remote.removeexportdirectory.assert_called_once_with(
            "Directory with spaces"
        )

    def test_RenameexportSuccess(self):
        self.annex.Listen(io.StringIO("EXPORT Name\nRENAMEEXPORT Key NewName"))
        self.remote.renameexport.assert_called_once_with("Key", "Name", "NewName")
        self.assertEqual(
            utils.second_buffer_line(self.output), "RENAMEEXPORT-SUCCESS Key"
        )

    def test_RenameexportFailure(self):
        self.remote.renameexport.side_effect = RemoteError()
        self.annex.Listen(io.StringIO("EXPORT Name\nRENAMEEXPORT Key NewName"))
        self.remote.renameexport.assert_called_once_with("Key", "Name", "NewName")
        self.assertEqual(
            utils.second_buffer_line(self.output), "RENAMEEXPORT-FAILURE Key"
        )

    def test_Renameexport_WithoutExport(self):
        with self.assertRaises(SystemExit):
            self.annex.Listen(io.StringIO("RENAMEEXPORT Key NewName"))
        self.assertEqual(
            utils.last_buffer_line(self.output),
            "ERROR Export request without prior EXPORT",
        )

    def test_Renameexport_MissingNewName(self):
        with self.assertRaises(SystemExit):
            self.annex.Listen(io.StringIO("EXPORT Name\nRENAMEEXPORT Key"))
        self.assertEqual(
            utils.last_buffer_line(self.output),
            "ERROR Expected TRANSFER STORE Key File",
        )

    def test_Renameexport_SpaceInNewName(self):
        self.annex.Listen(
            io.StringIO("EXPORT Name\nRENAMEEXPORT Key NewName with spaces")
        )
        self.remote.renameexport.assert_called_once_with(
            "Key", "Name", "NewName with spaces"
        )


class TestUnsupportedRequests(utils.MinimalTestCase):
    def test_UnsupportedRequest(self):
        self.annex.Listen(io.StringIO("Not a request"))
        self.assertEqual(utils.second_buffer_line(self.output), "UNSUPPORTED-REQUEST")

    def test_GetcostUnsupportedRequest(self):
        self.annex.Listen(io.StringIO("GETCOST"))
        self.assertEqual(utils.second_buffer_line(self.output), "UNSUPPORTED-REQUEST")

    def test_GetavailabilityUnsupportedRequest(self):
        self.annex.Listen(io.StringIO("GETAVAILABILITY"))
        self.assertEqual(utils.second_buffer_line(self.output), "UNSUPPORTED-REQUEST")

    def test_ClaimurlUnsupportedRequest(self):
        self.annex.Listen(io.StringIO("CLAIMURL Url"))
        self.assertEqual(utils.second_buffer_line(self.output), "UNSUPPORTED-REQUEST")

    def test_CheckurlUnsupportedRequest(self):
        self.annex.Listen(io.StringIO("CHECKURL Url"))
        self.assertEqual(utils.second_buffer_line(self.output), "UNSUPPORTED-REQUEST")

    def test_WhereisUnsupportedRequest(self):
        self.annex.Listen(io.StringIO("WHEREIS Key"))
        self.assertEqual(utils.second_buffer_line(self.output), "UNSUPPORTED-REQUEST")

    def test_TransferexportStoreUnsupportedRequest(self):
        self.annex.Listen(io.StringIO("EXPORT Name\nTRANSFEREXPORT STORE Key File"))
        self.assertEqual(utils.second_buffer_line(self.output), "UNSUPPORTED-REQUEST")

    def test_TransferexportRetrieveUnsupportedRequest(self):
        self.annex.Listen(io.StringIO("EXPORT Name\nTRANSFEREXPORT RETRIEVE Key File"))
        self.assertEqual(utils.second_buffer_line(self.output), "UNSUPPORTED-REQUEST")

    def test_CheckpresentexportUnsupportedRequest(self):
        self.annex.Listen(io.StringIO("EXPORT Name\nCHECKPRESENTEXPORT Key"))
        self.assertEqual(utils.second_buffer_line(self.output), "UNSUPPORTED-REQUEST")

    def test_RemoveexportUnsupportedRequest(self):
        self.annex.Listen(io.StringIO("EXPORT Name\nREMOVEEXPORT Key"))
        self.assertEqual(utils.second_buffer_line(self.output), "UNSUPPORTED-REQUEST")

    def test_RemoveexportdirectoryUnsupportedRequest(self):
        self.annex.Listen(io.StringIO("REMOVEEXPORTDIRECTORY Directory"))
        self.assertEqual(utils.second_buffer_line(self.output), "UNSUPPORTED-REQUEST")

    def test_RenameexportUnsupportedRequest(self):
        self.annex.Listen(io.StringIO("EXPORT Name\nRENAMEEXPORT Key NewName"))
        self.assertEqual(utils.second_buffer_line(self.output), "UNSUPPORTED-REQUEST")

    def test_ListconfigsEmpty(self):
        self.annex.Listen(io.StringIO("LISTCONFIGS"))
        self.assertEqual(utils.second_buffer_line(self.output), "CONFIGEND")


class LoggingRemote(utils.MinimalRemote):
    def __init__(self, annex):
        super().__init__(annex)
        self.logger = logging.getLogger()
        self.logger.addHandler(self.annex.LoggingHandler())

    def prepare(self):
        self.logger.warning("test\nthis is a new line")


class TestLogging(utils.ExportTestCase):
    def setUp(self):
        super().setUp()
        self.remote = LoggingRemote(self.annex)

        self.annex.LinkRemote(self.remote)

    def test_Logging(self):
        self.annex.Listen(io.StringIO("PREPARE"))

        buffer_lines = utils.buffer_lines(self.output)

        self.assertEqual(buffer_lines[1], "DEBUG root - WARNING - test")
        self.assertEqual(buffer_lines[2], "DEBUG this is a new line")
