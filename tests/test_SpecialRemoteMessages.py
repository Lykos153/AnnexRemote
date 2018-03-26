import io
import utils
ProtocolError = utils.annexremote.ProtocolError

class TestSpecialRemoteMessages(utils.GitAnnexTestCase):
    """
    * Each protocol line starts with a command, which is followed by the command's parameters 
    (a fixed number per command), each separated by a single space.
    * The last parameter may contain spaces.
    * Parameters may be empty, but the separating spaces are still required in that case.
    (from https://git-annex.branchable.com/design/external_special_remote_protocol)
    """

    def _perform_test(self, function_to_call, function_parameters, expected_output,
                    annex_reply=None, function_result=None, skip_assertion=False):
        self.annex.input = io.StringIO(annex_reply)
        result = function_to_call(*function_parameters)
        self.assertEqual(result, function_result)
        if not skip_assertion:
            self.assertEqual(utils.first_buffer_line(self.output).rstrip(), expected_output)
        

    def TestVersion(self):
        self.annex.Listen(self.input)
        self.assertEqual(self.output.getvalue(), "VERSION 1\n")

    def TestProgress(self):
        function_to_call = self.annex.progress
        function_parameters = (2048,)
        expected_output = "PROGRESS 2048"
        
        self._perform_test(function_to_call, function_parameters, expected_output)

    def TestDirhash(self):
        function_to_call = self.annex.dirhash
        function_parameters = ("Key",)
        expected_output = "DIRHASH Key"
        annex_reply = "VALUE aB/Cd"
        function_result = "aB/Cd"
        
        self._perform_test(function_to_call, function_parameters, expected_output,
                        annex_reply, function_result)
        
    def TestDirhashLower(self):
        function_to_call = self.annex.dirhash_lower
        function_parameters = ("Key",)
        expected_output = "DIRHASH-LOWER Key"
        annex_reply = "VALUE abc/def"
        function_result = "abc/def"
        
        self._perform_test(function_to_call, function_parameters, expected_output,
                        annex_reply, function_result)
        
    def TestSetconfig(self):
        function_to_call = self.annex.setconfig
        function_parameters = ("Setting", "Value")
        expected_output = "SETCONFIG Setting Value"

        self._perform_test(function_to_call, function_parameters, expected_output)
        
    def TestSetconfig_SpaceInValue(self):
        """
        The last parameter may contain spaces. 
        """
        function_to_call = self.annex.setconfig
        function_parameters = ("Setting", "Value with spaces")
        expected_output = "SETCONFIG Setting Value with spaces"

        self._perform_test(function_to_call, function_parameters, expected_output)

    def TestGetconfig(self):
        function_to_call = self.annex.getconfig
        function_parameters = ("Setting",)
        expected_output = "GETCONFIG Setting"
        annex_reply = "VALUE Value"
        function_result = "Value"
        
        self._perform_test(function_to_call, function_parameters, expected_output,
                        annex_reply, function_result)

    def TestGetconfig_SpaceInValue(self):
        function_to_call = self.annex.getconfig
        function_parameters = ("Setting",)
        expected_output = "GETCONFIG Setting"
        annex_reply = "VALUE Value with spaces"
        function_result = "Value with spaces"
        
        self._perform_test(function_to_call, function_parameters, expected_output,
                        annex_reply, function_result)

    def TestSetcreds(self):
        function_to_call = self.annex.setcreds
        function_parameters = ("Setting", "User", "Password")
        expected_output = "SETCREDS Setting User Password"

        self._perform_test(function_to_call, function_parameters, expected_output)

    def TestSetcreds_SpaceInPassword(self):
        function_to_call = self.annex.setcreds
        function_parameters = ("Setting", "User", "Password with spaces")
        expected_output = "SETCREDS Setting User Password with spaces"

        self._perform_test(function_to_call, function_parameters, expected_output)
    def TestSetcreds_NoPassword(self):
        function_to_call = self.annex.setcreds
        function_parameters = ("Setting", "User", "")
        expected_output = "SETCREDS Setting User"

        self._perform_test(function_to_call, function_parameters, expected_output)

    def TestSetcreds_NoUser(self):
        """
        Parameters may be empty, but the separating spaces are still required in that case.
        """
        function_to_call = self.annex.setcreds
        function_parameters = ("Setting", "", "Password")
        expected_output = "SETCREDS Setting  Password"

        self._perform_test(function_to_call, function_parameters, expected_output)

    def TestGetcreds(self):
        function_to_call = self.annex.getcreds
        function_parameters = ("Setting",)
        expected_output = "GETCREDS Setting"
        annex_reply = "CREDS User Password"
        function_result = {'user': "User", 'password': "Password"}
        
        self._perform_test(function_to_call, function_parameters, expected_output,
                        annex_reply, function_result)

    def TestGetcreds_SpaceInPassword(self):
        function_to_call = self.annex.getcreds
        function_parameters = ("Setting",)
        expected_output = "GETCREDS Setting"
        annex_reply = "CREDS User Password with spaces"
        function_result = {'user': "User", 'password': "Password with spaces"}
        
        self._perform_test(function_to_call, function_parameters, expected_output,
                        annex_reply, function_result)

    def TestGetcreds_NoPassword(self):
        function_to_call = self.annex.getcreds
        function_parameters = ("Setting",)
        expected_output = "GETCREDS Setting"
        annex_reply = "CREDS User"
        function_result = {'user': "User", 'password': ""}
        
        self._perform_test(function_to_call, function_parameters, expected_output,
                        annex_reply, function_result)

    def TestGetcreds_NoUser(self):
        function_to_call = self.annex.getcreds
        function_parameters = ("Setting",)
        expected_output = "GETCREDS Setting"
        annex_reply = "CREDS  Password"
        function_result = {'user': "", 'password': "Password"}
        
        self._perform_test(function_to_call, function_parameters, expected_output,
                        annex_reply, function_result)
    
    def TestGetuuid(self):
        function_to_call = self.annex.getuuid
        function_parameters = ()
        expected_output = "GETUUID"
        annex_reply = "VALUE uuid"
        function_result = "uuid"
        
        self._perform_test(function_to_call, function_parameters, expected_output,
                        annex_reply, function_result)

    def TestGetgitdir(self):
        function_to_call = self.annex.getgitdir
        function_parameters = ()
        expected_output = "GETGITDIR"
        annex_reply = "VALUE /path/to/gitdir"
        function_result = "/path/to/gitdir"
        
        self._perform_test(function_to_call, function_parameters, expected_output,
                        annex_reply, function_result)

    def TestGetgitdir_SpaceInPath(self):
        function_to_call = self.annex.getgitdir
        function_parameters = ()
        expected_output = "GETGITDIR"
        annex_reply = "VALUE /path/to/gitdir with spaces/"
        function_result = "/path/to/gitdir with spaces/"
        
        self._perform_test(function_to_call, function_parameters, expected_output,
                        annex_reply, function_result)
    def TestSetwanted(self):
        function_to_call = self.annex.setwanted
        function_parameters = ("Preferred Content Expression",)
        expected_output = "SETWANTED Preferred Content Expression"
        
        self._perform_test(function_to_call, function_parameters, expected_output)

    def TestGetwanted(self):
        function_to_call = self.annex.getwanted
        function_parameters = ()
        expected_output = "GETWANTED"
        annex_reply = "VALUE Preferred Content Expression"
        function_result = "Preferred Content Expression"
        
        self._perform_test(function_to_call, function_parameters, expected_output,
                        annex_reply, function_result)

    def TestSetstate(self):
        function_to_call = self.annex.setstate
        function_parameters = ("Key", "Value")
        expected_output = "SETSTATE Key Value"

        self._perform_test(function_to_call, function_parameters, expected_output)
        
    def TestSetstate_SpaceInValue(self):
        function_to_call = self.annex.setstate
        function_parameters = ("Key", "Value with spaces")
        expected_output = "SETSTATE Key Value with spaces"

        self._perform_test(function_to_call, function_parameters, expected_output)
        
    def TestSetstate_NoValue(self):
        function_to_call = self.annex.setstate
        function_parameters = ("Key", "")
        expected_output = "SETSTATE Key"

        self._perform_test(function_to_call, function_parameters, expected_output)

    def TestGetstate(self):
        function_to_call = self.annex.getstate
        function_parameters = ("Key",)
        expected_output = "GETSTATE Key"
        annex_reply = "VALUE State"
        function_result = "State"
        
        self._perform_test(function_to_call, function_parameters, expected_output,
                        annex_reply, function_result)

    def TestGetstate_SpaceInValue(self):
        function_to_call = self.annex.getstate
        function_parameters = ("Key",)
        expected_output = "GETSTATE Key"
        annex_reply = "VALUE State with spaces"
        function_result = "State with spaces"
        
        self._perform_test(function_to_call, function_parameters, expected_output,
                        annex_reply, function_result)

    def TestGetstate_NoValue(self):
        function_to_call = self.annex.getstate
        function_parameters = ("Key",)
        expected_output = "GETSTATE Key"
        annex_reply = "VALUE"
        function_result = ""
        
        self._perform_test(function_to_call, function_parameters, expected_output,
                        annex_reply, function_result)

    def TestSeturlpresent(self):
        function_to_call = self.annex.seturlpresent
        function_parameters = ("Key", "Url")
        expected_output = "SETURLPRESENT Key Url"

        self._perform_test(function_to_call, function_parameters, expected_output)
        
    def TestSeturlmissing(self):
        function_to_call = self.annex.seturlmissing
        function_parameters = ("Key", "Url")
        expected_output = "SETURLMISSING Key Url"

        self._perform_test(function_to_call, function_parameters, expected_output)
        
    def TestSeturipresent(self):
        function_to_call = self.annex.seturipresent
        function_parameters = ("Key", "Uri")
        expected_output = "SETURIPRESENT Key Uri"

        self._perform_test(function_to_call, function_parameters, expected_output)
        
    def TestSeturimissing(self):
        function_to_call = self.annex.seturimissing
        function_parameters = ("Key", "Uri")
        expected_output = "SETURIMISSING Key Uri"

        self._perform_test(function_to_call, function_parameters, expected_output)
        
    def TestGeturls(self):
        function_to_call = self.annex.geturls
        function_parameters = ("Key", "Prefix")
        expected_output = "GETURLS Key Prefix"
        annex_reply = "VALUE State1\nVALUE State2\nVALUE"
        function_result = ["State1", "State2"]
        
        self._perform_test(function_to_call, function_parameters, expected_output,
                        annex_reply, function_result)
        
    def TestDebug(self):
        function_to_call = self.annex.debug
        function_parameters = ("message",)
        expected_output = "DEBUG message"
        
        self._perform_test(function_to_call, function_parameters, expected_output)

    def TestError(self):
        function_to_call = self.annex.error
        function_parameters = ("ErrorMsg",)
        expected_output = "ERROR ErrorMsg"
        
        self._perform_test(function_to_call, function_parameters, expected_output)

class TestSpecialRemoteMessages_Extensions(utils.GitAnnexTestCase):

    def _perform_test(self, function_to_call, function_parameters, expected_output,
                    annex_reply=None, function_result=None):
        
        self.annex.input = io.StringIO(annex_reply)
        result = function_to_call(*function_parameters)
        self.assertEqual(result, function_result)

        self.assertEqual(utils.buffer_lines(self.output)[1].rstrip(), "EXTENSIONS")
        self.assertEqual(utils.buffer_lines(self.output)[2].rstrip(), expected_output)

    def TestInfo(self):
        self.annex.Listen(io.StringIO("EXTENSIONS INFO"))
        function_to_call = self.annex.info
        function_parameters = ("message",)
        expected_output = "INFO message"
        
        self._perform_test(function_to_call, function_parameters, expected_output)
        

    def TestInfo_Unannounced(self):
        function_to_call = self.annex.info
        function_parameters = ("message",)
        with self.assertRaises(ProtocolError):
            self._perform_test(function_to_call, function_parameters, "")
        
                
        
        
        
        
        

