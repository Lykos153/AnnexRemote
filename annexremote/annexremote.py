# AnnexRemote - Helper module to easily develop git-annex remotes
#
# Copyright (C) 2017  Silvio Ankermann
#
# This program is free software: you can redistribute it and/or modify it under the terms of version 3 of the GNU
# General Public License as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be uselful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import int
from builtins import str
from future import standard_library
standard_library.install_aliases()
from future.utils import with_metaclass
from builtins import object


from abc import ABCMeta, abstractmethod

import sys
import string


# Exceptions
class AnnexError(Exception):
    pass
class ProtocolError(AnnexError):
    pass

class UnsupportedRequest(ProtocolError):
    pass

class UnexpectedMessage(ProtocolError):
    pass

class RemoteError(AnnexError):
    pass

class NotLinkedError(AnnexError):
    pass

class SpecialRemote(with_metaclass(ABCMeta, object)):
    """
    Metaclass for non-export remotes.

    ...

    Attributes
    ----------
    annex : Master
        The Master object to which this remote is linked. Master acts as an abstraction layer for git-annex.
    info : dict
        Contains information describing the configuration of the remote, for display by `git annex info` in
        the form of {'Name': 'Value', ...} where both can be anything you want to be displayed to the user.
        Note: Both Name and Value *can* contain spaces.
    configs : dict
        Contains the settings which the remote uses (with getconfig() and setconfig()) in the form of
        {'Name': 'Description', ...}
        Note: Name *must not* contain spaces. Description should be reasonably short.
        Example: {'directory': "store data here"}
        Providing them makes `git annex initremote` work better, because it can check the user's input, 
        and can also display a list of settings with descriptions.
        Note that the user is not required to provided all the settings listed here.
    """

    def __init__(self, annex):
        self.annex = annex
        self.info = {}
        self.configs = {}

    @abstractmethod
    def initremote(self):
        """
        Gets called when `git annex initremote` or `git annex enableremote` are run. 
        This is where any one-time setup tasks can be done, for example creating the remote folder.
        Note: This may be run repeatedly over time, as a remote is initialized in different repositories,
        or as the configuration of a remote is changed. So any one-time setup tasks should be done idempotently.

        Raises
        ------
        RemoteError
            If the remote could not be initialized.
        """

    @abstractmethod
    def prepare(self):
        """
        Tells the remote that it's time to prepare itself to be used.
        Gets called whenever git annex is about to access any of the below 
        methods, so it shouldn't be too expensive. Otherwise it will
        slow down operations like `git annex whereis` or `git annex info`.

        Internet connection *can* be established here, though it's
        recommended to defer this until it's actually needed.

        Raises
        ------
        RemoteError
            If the remote could not be prepared.
        """

    @abstractmethod
    def transfer_store(self, key, local_file):
        """
        Store the file in `local_file` to a unique location derived from `key`.

        It's important that, while a Key is being stored, checkpresent(key)
        not indicate it's present until all the data has been transferred.
        While the transfer is running, the remote can repeatedly call 
        annex.progress(size) to indicate the number of bytes already stored.
        This will influence the progress shown to the user.

        Parameters
        ----------
        key : str
            The Key to be stored in the remote. In most cases, this is going to be the
            remote file name. It should be at least be unambigiously derived from it.
        local_file: str
            Path to the file to upload.
            Note that in some cases, local_file may contain whitespace.
            Note that local_file should not influence the filename used on the remote.

        Raises
        ------
        RemoteError
            If the file could not be stored to the remote.
        """

    @abstractmethod
    def transfer_retrieve(self, key, local_file):
        """
        Get the file identified by `key` from the remote and store it in `local_file`.

        While the transfer is running, the remote can repeatedly call 
        annex.progress(size) to indicate the number of bytes already stored.
        This will influence the progress shown to the user.

        Parameters
        ----------
        key : str
            The Key to get from the remote.
        local_file: str
            Path where to store the file.
            Note that in some cases, local_file may contain whitespace.

        Raises
        ------
        RemoteError
            If the file could not be received from the remote.
        """

    @abstractmethod
    def checkpresent(self, key):
        """
        Requests the remote to check if a key is present in it.

        Parameters
        ----------
        key : str

        Returns
        -------
        bool
            True if the key is present in the remote.
            False if the key is not present.

        Raises
        ------
        RemoteError
            If the presence of the key couldn't be determined, eg. in case of connection error.

        """

    @abstractmethod
    def remove(self, key):
        """
        Requests the remote to remove a key's contents.

        Parameters
        ----------
        key : str

        Raises
        ------
        RemoteError
            If the key couldn't be deleted from the remote.
        """
    
    # Optional requests
    def listconfigs(self):
        return self.configs

    def getcost(self):
        """
        Requests the remote to return a use cost. Higher costs are more expensive. 
        
        cheapRemoteCost = 100
        nearlyCheapRemoteCost = 110
        semiExpensiveRemoteCost = 175
        expensiveRemoteCost = 200
        veryExpensiveRemoteCost = 1000
        (taken from Config/Cost.hs)

        Returns
        -------
        int
            Indicates the cost of the remote.
        """
        raise UnsupportedRequest()

    def getavailability(self):
        """
        Asks the remote if it is locally or globally available. (Ie stored in the cloud vs on a local disk.)

        Returns
        -------
        str
            Allowed values are "global" or "local".

        """
        raise UnsupportedRequest()

    def claimurl(self, url):
        """
        Asks the remote if it wishes to claim responsibility for downloading an url.


        Parameters
        ----------
        url : str

        Returns
        -------
        bool
            True if it wants to claim this url.
            False if it doesn't.

        """
        raise UnsupportedRequest()

    def checkurl(self, url):
        """
        Asks the remote to check if the url's content can currently be downloaded (without downloading it).
        The remote can optionally provide additional information about the file.

        Parameters
        ----------
        url : str

        Returns
        -------
        Union(bool, List(Dict))
            True if the url's content can currently be downloaded and no additional information can be provided.
            False if it can't currently be downloaded.

            In order to provide additional information, a list of dictionaries can be returned.
            The dictionaries can have 3 keys: {'url': str, 'size': int, 'filename': str}
            If there is only one file to be downloaded, we could return:
            [{'size': 512, 'filename':'example_file.txt'}]
            Both `size` and `filename` can be ommited.

            If there are multiple files to be downloaded from this url



            The dictionaries are of the form:
            {'url':"https://example.com", 'size':512, 'filename':"example_file.txt"}

            [{'url':"Url1", 'size':512, 'filename':"Filename1"}, {'url':"Url2", 'filename':"Filename2"}]



        """
        raise UnsupportedRequest()

    def whereis(self, key):
        """
        Asks the remote to provide additional information about ways to access the
        content of a key stored in it, such as eg, public urls. This will be displayed 
        to the user by eg, git annex whereis.
        Note that users expect git annex whereis to run fast, without eg, network access.
        
        Parameters
        ----------
        key : str

        Returns
        -------
        str
            Information about the location of the key, eg. public urls.

        """
        raise UnsupportedRequest()
    
    # Export methods
    def exportsupported(self):
        return False

    def transferexport_store(self, key, local_file, remote_file):
        raise UnsupportedRequest()

    def transferexport_retrieve(self, key, local_file, remote_file):
        raise UnsupportedRequest()

    def checkpresentexport(self, key, remote_file):
        raise UnsupportedRequest()

    def removeexport(self, key, remote_file):
        raise UnsupportedRequest()

    def removeexportdirectory(self, remote_directory):
        raise UnsupportedRequest()

    def renameexport(self, key, filename, new_filename):
        raise UnsupportedRequest()

    # Setup function to be run before initremote to handle things like authentication interactively
    def setup(self):
        print("Nothing to do. Just run 'git annex initremote' with your desired parameters")

class ExportRemote(SpecialRemote):
    """
    Metaclass for remotes that support non-export *and* export behaviour.

    ...

    Attributes
    ----------
    annex : Master
        The Master object to which this remote is linked. Master acts as an abstraction layer for git-annex.
    info : dict
        Contains information describing the configuration of the remote, for display by `git annex info` in
        the form of {'Name': 'Value', ...} where both can be anything you want to be displayed to the user.
        Note: Both Name and Value *can* contain spaces.
    configs : dict
        Contains the settings which the remote uses (with getconfig() and setconfig()) in the form of
        {'Name': 'Description', ...}
        Note: Name *must not* contain spaces. Description should be reasonably short.
        Example: {'directory': "store data here"}
        Providing them makes `git annex initremote` work better, because it can check the user's input, 
        and can also display a list of settings with descriptions.
        Note that the user is not required to provided all the settings listed here.
    """

    def exportsupported(self):
        return True

    @abstractmethod
    def transferexport_store(self, key, local_file, remote_file):
        """
        Requests the transfer of a file on local disk to the special remote.
        Note that it's important that, while a file is being stored, 
        checkpresentexport() not indicate it's present until all the data 
        has been transferred.
        While the transfer is running, the remote can send any number of progess(size) messages.


        Parameters
        ----------
        key : str
            The Key to be stored in the remote.
        local_file: str
            Path to the file to upload.
            Note that in some cases, local_file may contain whitespace.
        remote_file : str
            The path to the location to which the file will be uploaded.
            It will be in the form of a relative path, and may contain
            path separators, whitespace, and other special characters.

        Raises
        ------
        RemoteError
            If the key couldn't be stored on the remote.
        """

    @abstractmethod
    def transferexport_retrieve(self, key, local_file, remote_file):
        """
        Requests the transfer of a file from the special remote to the local disk.
        Note that it's important that, while a file is being stored, 
        checkpresentexport() not indicate it's present until all the data 
        has been transferred.
        While the transfer is running, the remote can send any number of progess(size) messages.


        Parameters
        ----------
        key : str
            The Key to get from the remote.
        local_file: str
            Path where to store the file.
            Note that in some cases, local_file may contain whitespace.
        remote_file : str
            The remote path of the file to download.
            It will be in the form of a relative path, and may contain
            path separators, whitespace, and other special characters.

        Raises
        ------
        RemoteError
            If the key couldn't be stored on the remote.
        """

    @abstractmethod
    def checkpresentexport(self, key, remote_file):
        """
        Requests the remote to check if the file is present in it.

        Parameters
        ----------
        key : str
            The key of the file to check. 
        remote_file : str
            The remote path of the file to check.

        Returns
        -------
        bool
            True if the file is present in the remote.
            False if the file is not present in the remote

        Raises
        ------
        RemoteError
            If the the presence of the key couldn't be determined.
        """

    @abstractmethod
    def removeexport(self, key, remote_file):
        """
        Requests the remote to remove content stored by transferexportstore().

        Parameters
        ----------
        key : str
            The key of the file to check. 
        remote_file : str
            The remote path of the file to delete.

        Raises
        ------
        RemoteError
            If the the remote file couldn't be deleted.
        """

    def removeexportdirectory(self, remote_directory):
        """
        Requests the remote to remove an exported directory.
        If the remote does not use directories, or removeexport() cleans
        up directories that are empty, this does not need to be implemented.

        Parameters
        ----------
        remote_directory : str
            The remote path to the directory to delete. 
            The directory will be in the form of a relative path,
            and may contain path separators, whitespace, and other special characters.
            Typically the directory will be empty, but it could possibly contain
            files or other directories, and it's ok to remove those,
            but not required to do so. 

        Raises
        ------
        RemoteError
            If the the remote directory couldn't be deleted.
        """
        raise UnsupportedRequest()

    def renameexport(self, key, filename, new_filename):
        """
        Requests the remote rename a file stored on it from `filename` to `new_filename`. 
        Remotes that support exports but not renaming do not need to implement this.

        Parameters
        ----------
        key : str
            The key of the file to rename
        filename : str
            The old path to the file.
        new_filename : str
            The new path to the file.

        Raises
        ------
        RemoteError
            If the the remote directory couldn't be deleted.
        """
        raise UnsupportedRequest()
        
class Protocol(object):

    def __init__(self, remote):
        self.remote = remote
        self.version = "VERSION 1"
        self.exporting = False
        self.extensions = list()
        
    def command(self, line):
        line = line.strip()
        parts = line.split(" ", 1)
        if not parts:
            raise ProtocolError("Got empty line")
            

        method = self.lookupMethod(parts[0]) or self.do_UNKNOWN


        try:
            if len(parts) == 1:
                reply = method()
            else:
                reply = method(parts[1])
        except TypeError as e:
            raise SyntaxError(e)
        else:
            if method != self.do_EXPORT:
                self.exporting = False
            return reply

    def lookupMethod(self, command):
        return getattr(self, 'do_' + command.upper(), None)
        
    def check_key(self, key):
        if len(key.split()) != 1:
            raise ValueError("Invalid key. Key contains whitespace character")

    def do_UNKNOWN(self, *arg):
        raise UnsupportedRequest()
        
    def do_INITREMOTE(self):
        try:
            reply = self.remote.initremote()
        except RemoteError as e:
            return "INITREMOTE-FAILURE {e}".format(e=e)
        else:
            return "INITREMOTE-SUCCESS"
            
    def do_EXTENSIONS(self, param):
        self.extensions = param.split(" ")
        return "EXTENSIONS"
    
    def do_PREPARE(self):
        try:
            reply = self.remote.prepare()
        except RemoteError as e:
            return "PREPARE-FAILURE {e}".format(e=e)
        else:
            return "PREPARE-SUCCESS"
    
    def do_TRANSFER(self, param):
        try:
            (method, key, file_) = param.split(" ", 2)
        except ValueError:
            raise SyntaxError("Expected Key File")
        
        if not (method == "STORE" or method == "RETRIEVE"):
            return self.do_UNKNOWN()
        
        func = getattr(self.remote, "transfer_{}".format(method.lower()), None)
        try:
            func(key, file_)
        except RemoteError as e:
            return "TRANSFER-FAILURE {method} {key} {e}".format(method=method, key=key, e=e)
        else:
            return "TRANSFER-SUCCESS {method} {key}".format(method=method, key=key)
    
    def do_CHECKPRESENT(self, key):
        self.check_key(key)
        try:
            if self.remote.checkpresent(key):
                return "CHECKPRESENT-SUCCESS {key}".format(key=key)
            else:
                return "CHECKPRESENT-FAILURE {key}".format(key=key)
        except RemoteError as e:
            return "CHECKPRESENT-UNKNOWN {key} {e}".format(key=key, e=e)
    
    def do_REMOVE(self, key):
        self.check_key(key)
        
        try:
            self.remote.remove(key)
        except RemoteError as e:
            return "REMOVE-FAILURE {key} {e}".format(key=key, e=e)
        else:
            return "REMOVE-SUCCESS {key}".format(key=key)
    
    def do_LISTCONFIGS(self):
        return_string = ""
        for name, description in self.remote.listconfigs().items():
            if " " in name:
                raise ValueError("Name must not contain space characters: {}".format(name))
            return_string += "CONFIG {} {}\n".format(name, description)
        return_string += "CONFIGEND"
        return return_string

    def do_GETCOST(self):
        cost = self.remote.getcost()
        try:
            cost = int(cost)
        except ValueError:
            raise ValueError("Cost must be an integer")
        return "COST {cost}".format(cost=cost)
    
    def do_GETAVAILABILITY(self):
        reply = self.remote.getavailability()
        if reply == "global":
            return "AVAILABILITY GLOBAL"
        elif reply == "local":
            return "AVAILABILITY LOCAL"
        else:
            raise ValueError("Availability must be either 'global' or 'local'")
        
    def do_CLAIMURL(self, url):
        if self.remote.claimurl(url):
            return "CLAIMURL-SUCCESS"
        else:
            return "CLAIMURL-FAILURE"
    
    def do_CHECKURL(self, url):
        try:
            reply = self.remote.checkurl(url)
        except RemoteError:
            return "CHECKURL-FAILURE"
        if not reply:
            return "CHECKURL-FAILURE"
        elif reply is True:
            return "CHECKURL-CONTENTS UNKNOWN"
        
        if len(reply)==1 and 'url' not in reply[0]:
            entry = reply[0]
            size = entry.get("size", "UNKNOWN")
                
            returnvalue = " ".join(("CHECKURL-CONTENTS", str(size)))
        
            if 'filename' in entry and entry['filename']:
                returnvalue = " ".join((returnvalue, entry['filename']))
            return returnvalue
                
        returnvalue = "CHECKURL-MULTI"
        for entry in reply:
            if 'url' not in entry:
                raise ValueError("Url must be present when specifying multiple values.")
            if len(entry['url'].split()) != 1:
                raise ValueError("Url must not contain spaces.")
                
            size = entry.get("size", "UNKNOWN")
            filename = entry.get("filename", "")    
            if " " in filename:
                raise ValueError("Filename must not contain spaces.")
                
            returnvalue = " ".join((returnvalue, entry['url'], str(size), filename))
        return returnvalue
        
    
    def do_WHEREIS(self, key):
        self.check_key(key)
        reply = self.remote.whereis(key)
        if reply:
            return "WHEREIS-SUCCESS {reply}".format(reply=reply)
        else:
            return "WHEREIS-FAILURE"

    def do_GETINFO(self):
        info = self.remote.info
        reply = []
        for field in sorted(info):
            reply.append("INFOFIELD {}".format(field))
            reply.append("INFOVALUE {}".format(info[field]))
        reply.append("INFOEND")
        return '\n'.join(reply)
    
    def do_EXPORTSUPPORTED(self):
        if self.remote.exportsupported():
            return "EXPORTSUPPORTED-SUCCESS"
        else:
            return "EXPORTSUPPORTED-FAILURE"
    
    def do_EXPORT(self, name):
        self.exporting = name
    
    def do_TRANSFEREXPORT(self, param):
        if not self.exporting:
            raise ProtocolError("Export request without prior EXPORT")
        try:
            (method, key, file_) = param.split(" ", 2)
        except ValueError:
            raise SyntaxError("Expected Key File")
        
        if not (method == "STORE" or method == "RETRIEVE"):
            return self.do_UNKNOWN()
        
        func = getattr(self.remote, "transferexport_{}".format(method.lower()), None)
        try:
            func(key, file_, self.exporting)
        except RemoteError as e:
            return "TRANSFER-FAILURE {method} {key} {e}".format(method=method, key=key, e=e)
        else:
            return "TRANSFER-SUCCESS {method} {key}".format(method=method, key=key)
    
    def do_CHECKPRESENTEXPORT(self, key):
        if not self.exporting:
            raise ProtocolError("Export request without prior EXPORT")  
        self.check_key(key)
        try:
            if self.remote.checkpresentexport(key, self.exporting):
                return "CHECKPRESENT-SUCCESS {key}".format(key=key)
            else:
                return "CHECKPRESENT-FAILURE {key}".format(key=key)
        except RemoteError as e:
            return "CHECKPRESENT-UNKNOWN {key} {e}".format(key=key, e=e)
            
    def do_REMOVEEXPORT(self, key):
        if not self.exporting:
            raise ProtocolError("Export request without prior EXPORT")  
        self.check_key(key)
        
        try:
            self.remote.removeexport(key, self.exporting)
        except RemoteError as e:
            return "REMOVE-FAILURE {key} {e}".format(key=key, e=e)
        else:
            return "REMOVE-SUCCESS {key}".format(key=key)
                    
    def do_REMOVEEXPORTDIRECTORY(self, name):
        try:
            self.remote.removeexportdirectory(name)
        except RemoteError:
            return "REMOVEEXPORTDIRECTORY-FAILURE"
        else:
            return "REMOVEEXPORTDIRECTORY-SUCCESS"
    
    def do_RENAMEEXPORT(self, param):
        if not self.exporting:
            raise ProtocolError("Export request without prior EXPORT")  
        try:
            (key, new_name) = param.split(None, 1)
        except ValueError:
            raise SyntaxError("Expected TRANSFER STORE Key File")
            
        try:
            self.remote.renameexport(key, self.exporting, new_name)
        except RemoteError:
            return "RENAMEEXPORT-FAILURE {key}".format(key=key)
        else:
            return "RENAMEEXPORT-SUCCESS {key}".format(key=key)

class Master(object):
    """
    Metaclass for non-export remotes.

    ...

    Attributes
    ----------
    input : io.TextIOBase
        Where to listen for git-annex request messages.
        Default: sys.stdin
    output : io.TextIOBase
        Where to send replies and special remote messages
        Default: sys.stdout
    remote : SpecialRemote
        A class implementing either the SpecialRemote or the
        ExternalSpecialRemote interface to which this master is linked.
    """

    def __init__(self, output=sys.stdout):
        """
        Initialize the Master with an ouput.

        Parameters
        ----------
        output : io.TextIOBase
            Where to send replies and special remote messages
            Default: sys.stdout
        """
        self.output = output

    def LinkRemote(self, remote):
        """
        Link the Master to a remote. This must be done before calling Listen()

        Parameters
        ----------
        remote : SpecialRemote
            A class implementing either the SpecialRemote or the
            ExternalSpecialRemote interface to which this master will be linked.
        """
        self.remote = remote
        self.protocol = Protocol(remote)

    def Listen(self, input=sys.stdin):
        """
        Listen on `input` for messages from git annex.

        Parameters
        ----------
        input : io.TextIOBase
            Where to listen for git-annex request messages.
            Default: sys.stdin

        Raises
        ----------
        NotLinkedError
            If there is no remote linked to this master.
        """
        if not (hasattr(self, 'remote') and hasattr(self, 'protocol')):
            raise NotLinkedError("Please execute LinkRemote(remote) first.")

        self.input = input
        self._send(self.protocol.version)
        while True:
            # due to a bug in python 2 we can't use an iterator here: https://bugs.python.org/issue1633941
            line = self.input.readline()
            if not line:
                break
            line = line.rstrip()
            try:
                reply = self.protocol.command(line)
                if reply:
                    self._send(reply)
            except (UnsupportedRequest):
                self._send ("UNSUPPORTED-REQUEST")
            except (NotImplementedError):
                self._send ("ERROR not yet implemented")
                raise SystemExit
            #except Exception as e:
            #    self._send ("ERROR", e)
            #    raise SystemExit

    def _ask(self, request, reply_keyword, reply_count):
        self._send(request)
        line = self.input.readline().rstrip().split(" ", reply_count)
        if line and line[0] == reply_keyword:
            line.extend([""] * (reply_count+1-len(line)))
            return line[1:]
        else:
            raise UnexpectedMessage("Expected {reply_keyword} and {reply_count} values. Got {line}".format(reply_keyword=reply_keyword, reply_count=reply_count, line=line))

    def _askvalues(self, request):
        self._send(request)
        reply = []
        while True:
            # due to a bug in python 2 we can't use an iterator here: https://bugs.python.org/issue1633941
            line = self.input.readline()
            line = line.rstrip()
            line = line.split(" ", 1)
            if len(line) == 2 and line[0] == "VALUE":
                 reply.append(line[1])
            elif len(line) == 1 and line[0] == "VALUE":
                return reply
            else:
                raise UnexpectedMessage("Expected VALUE {value}")

    def _askvalue(self, request):
        (reply,) = self._ask(request, "VALUE", 1)
        return reply
    
    def getconfig(self, req):
        """
        Gets one of the special remote's configuration settings,
        which can have been passed by the user when running `git annex initremote`,
        `git annex enableremote` or can have been set by a previous SETCONFIG. Can be run at any time.
It's recommended that special remotes that use this implement LISTCONFIGS. (git-annex replies with VALUE followed by the value. If the setting is not set, the value will be empty.)
        """
        return self._askvalue("GETCONFIG {req}".format(req=req))

    def setconfig(self, key, value):
        self._send("SETCONFIG {key} {value}".format(key=key, value=value))

    def getstate(self, key):
        return self._askvalue("GETSTATE {key}".format(key=key))

    def setstate(self, key, value):
        self._send("SETSTATE {key} {value}".format(key=key, value=value))

    def debug(self, *args):
        self._send("DEBUG", *args)
        
    def error(self, *args):
        self._send("ERROR", *args)

    def progress(self, progress):
        self._send("PROGRESS {progress}".format(progress=int(progress)))

    def dirhash(self, key):
        return self._askvalue("DIRHASH {key}".format(key=key))

    def dirhash_lower(self, key):
        return self._askvalue("DIRHASH-LOWER {key}".format(key=key))

    def setcreds(self, setting, user, password):
        self._send("SETCREDS", setting, user, password)

    def getcreds(self, setting):
        (user, password) = self._ask("GETCREDS {setting}".format(setting=setting), "CREDS", 2)
        return {'user': user, 'password': password}

    def getuuid(self):
        return self._askvalue("GETUUID")

    def getgitdir(self):
        return self._askvalue("GETGITDIR")

    def setwanted(self, prefcontent):
        self._send("SETWANTED", prefcontent)

    def getwanted(self):
        return self._askvalue("GETWANTED")

    def seturlpresent(self, key, url):
        self._send("SETURLPRESENT", key, url)

    def seturlmissing(self, key, url):
        self._send("SETURLMISSING", key, url)

    def seturipresent(self, key, uri):
        self._send("SETURIPRESENT", key, uri)
    
    def seturimissing(self, key, uri):
        self._send("SETURIMISSING", key, uri)

    def geturls(self, key, prefix):
        return self._askvalues("GETURLS {key} {prefix}".format(key=key, prefix=prefix))
        
    def info(self, message):
        if "INFO" in self.protocol.extensions:
            self._send("INFO", message)
        else:
            raise ProtocolError("INFO not available") 

    def _send(self, *args, **kwargs):
        print(*args, file=self.output, **kwargs)
        self.output.flush()
