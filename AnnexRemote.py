# git-annex-remote-gdrive2 - python rewrite of git-annex-remote-gdrive to add direct support for Google Drive to git annex
#
# Install in PATH as git-annex-remote-gdrive2
#
# Copyright (C) 2017  Silvio Ankermann
#
# This program is free software: you can redistribute it and/or modify it under the terms of version 3 of the GNU
# General Public License as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#

from abc import ABC, abstractmethod

import string


# Exceptions
class RequestError(Exception):
    pass

class UnsupportedRequest(RequestError):
    pass

class UnexpectedMessage(RequestError):
    pass


class SpecialRemote(ABC):

    @abstractmethod
    def __init__(self, annex):
        pass

    @abstractmethod
    def initremote(self):
        pass

    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def transfer_store(self, key, file_):
        pass

    @abstractmethod
    def transfer_retrieve(self, key, file_):
        pass

    @abstractmethod
    def checkpresent(self, key):
        pass

    @abstractmethod
    def remove(self, key):
        pass
    
    # Optional requests
    def getcost(self):
        raise UnsupportedRequest()

    def getavailability(self):
        raise UnsupportedRequest()

    def claimurl(self, url):
        raise UnsupportedRequest()

    def checkurl(self):
        raise UnsupportedRequest()

    def whereis(self):
        raise UnsupportedRequest()

    # Setup function to be run before initremote to handle things like authentication interactively
    def setup(self):
        print("Nothing to do. Just run 'git annex initremote' with your desired parameters")

class ExportRemote(SpecialRemote):
    def exportsupported(self):
        return Reply.ExportsupportedSuccess()

    @abstractmethod
    def export(self, name):
        pass

    @abstractmethod
    def transferexport_store(self, key, file_):
        pass

    @abstractmethod
    def transferexport_retrieve(self, key, file_):
        pass

    @abstractmethod
    def checkpresentexport(self, key):
        pass

    @abstractmethod
    def removeexport(self, key):
        pass

    @abstractmethod
    def removeexportdirectory(self, directory):
        pass

    @abstractmethod
    def renameexport(self, key, new_name):
        pass

# Remote replies
class Reply():
    class RemoteReply():
        pass

    class InitremoteSuccess(RemoteReply):
        def __str__(self):
            return "INITREMOTE-SUCCESS"

    class InitremoteFailure(RemoteReply):
        def __init__(self, msg):
            self.msg = msg
        def __str__(self):
            return f"INITREMOTE-FAILURE {self.msg}"
    
    class PrepareSuccess(RemoteReply):
        def __str__(self):
            return "PREPARE-SUCCESS"

    class PrepareFailure(RemoteReply):
        def __init__(self, msg):
            self.msg = msg
        def __str__(self):
            return f"PREPARE-FAILURE {self.msg}"


    class KeyReply(RemoteReply):
        def __init__(self, key):
            self.key = key

    class TransferSuccess_Store(KeyReply):
        def __str__(self):
            return f"TRANSFER-SUCCESS STORE {self.key}"

    class TransferFailure_Store(KeyReply):
        def __str__(self):
            return f"TRANSFER-FAILURE STORE {self.key}"
    
    class TransferSuccess_Retrieve(KeyReply):
        def __str__(self):
            return f"TRANSFER-SUCCESS RETRIEVE {self.key}"

    class TransferFailure_Retrieve(KeyReply):
        def __str__(self):
            return f"TRANSFER-FAILURE RETRIEVE {self.key}"

    class CheckpresentSuccess(KeyReply):
        def __str__(self):
            return f"CHECKPRESENT-SUCCESS {self.key}"

    class CheckpresentUnknown(KeyReply):
        def __str__(self):
            return f"CHECKPRESENT-UNKNOWN {self.key}"
      
    class CheckpresentFailure(KeyReply):
        def __str__(self):
            return f"CHECKPRESENT-FAILURE {self.key}"

    class RemoveSuccess(KeyReply):
        def __str__(self):
            return f"REMOVE-SUCCESS {self.key}"

    class RemoveFailure(KeyReply):
        def __str__(self):
            return f"REMOVE-FAILURE {self.key}"

    class ClaimurlSuccess(KeyReply):
        def __str__(self):
            return f"CLAIMURL-SUCCESS {self.key}"

    class ClaimurlFailure(KeyReply):
        def __str__(self):
            return f"CLAIMURL-FAILURE {self.key}"

    class CheckurlSuccess(KeyReply):
        def __str__(self):
            return f"CHECKURL-SUCCESS {self.key}"

    class CheckurlFailure(KeyReply):
        def __str__(self):
            return f"CHECKURL-FAILURE {self.key}"

    class WhereisSuccess(KeyReply):
        def __str__(self):
            return f"WHEREIS-SUCCESS {self.key}"

    class WhereisFailure(KeyReply):
        def __str__(self):
            return f"WHEREIS-FAILURE {self.key}"
    class ExportsupportedSuccess(RemoteReply):
        def __str__(self):
            return "EXPORTSUPPORTED-SUCCESS"
    class ExportsupportedFailure(RemoteReply):
        def __str__(self):
            return "EXPORTSUPPORTED-FAILURE"
    class RenameexportSuccess(KeyReply):
        def __str__(self):
            return f"RENAMEEXPORT-SUCCESS {self.key}"
    class RenameexportFailure(KeyReply):
        def __str__(self):
            return f"RENAMEEXPORT-FAILURE {self.key}"
    class RemoveexportdirectorySuccess(RemoteReply):
        def __str__(self):
            return f"REMOVEEXPORTDIRECTORY-SUCCESS"
    class RemoveexportdirectoryFailure(RemoteReply):
        def __str__(self):
            return f"REMOVEEXPORTDIRECTORY-FAILURE"

class Protocol:

    def __init__(self, remote):
        self.remote = remote
        self.version = "VERSION 1"
        
    def command(self, line):
        line = line.strip()
        parts = line.split(None, 1)
        if not parts:
            raise SyntaxError("Bad syntax")
        method = self.lookupMethod(parts[0]) or self.do_UNKNOWN
        try:
            if len(parts) == 1:
                return method()
            else:
                return method(parts[1])
        except TypeError:
            raise SyntaxError(f"Bad syntax in '{line}'")

    def lookupMethod(self, command):
        return getattr(self, 'do_' + command.upper(), None)
        
    def check_key(self, key):
        if len(key.split()) == 1:
            return True;
        else:
            return ValueError("Keys can't have whitespaces")

    def do_UNKNOWN(self, *arg):
        raise UnsupportedRequest()
        
        
    def do_INITREMOTE(self):
        return self.remote.initremote()
    
    def do_PREPARE(self):
        return self.remote.prepare()
    
    def do_TRANSFER(self, param):
        parts = param.split(None, 2)
        if len(parts) != 3:
            raise SyntaxError("Expected Key File")
        (method, key, file_) = parts
        if method == "STORE":
            return self.remote.transfer_store(key, file_)
        elif method == "RETRIEVE":
            return self.remote.transfer_retrieve(key, file_)
        else:
            return self.do_UNKNOWN()
    
    def do_CHECKPRESENT(self, param):
        if self.check_key(param):
            return self.remote.checkpresent(param)
    
    def do_REMOVE(self, param):
        if self.check_key(param):
            return self.remote.remove(param)
    
    def do_GETCOST(self):
        return self.remote.getcost()
    
    def do_GETAVAILABILITY(self):
        return self.remote.getavailability()
        
    def do_CLAIMURL(self, param):
        return self.remote.claimurl(param)
    
    def do_CHECKURL(self, param):
        return self.remote.checkurl(param)
    
    def do_WHEREIS(self, param):
        if self.check_key(param):
            return self.remote.whereis(param)
    
    def do_EXPORTSUPPORTED(self):
        return self.remote.exportsupported()
    
    def do_EXPORT(self, param):
        return self.remote.export(param)
    
    def do_TRANSFEREXPORT(self, param):
        parts = param.split(None, 2)
        if len(parts) != 3:
            raise SyntaxError("Expected Key File")
        (method, key, file_) = parts
        if method == "STORE":
            return self.remote.transferexport_store(key, file_)
        elif method == "RETRIEVE":
            return self.remote.transferexport_retrieve(key, file_)
        else:
            return self.do_UNKNOWN()
    
    def do_CHECKPRESENTEXPORT(self, param):
        if self.check_key(param):
            return self.remote.checkpresentexport(param)
    
    def do_REMOVEEXPORT(self, param):
        if self.check_key(param):
            return self.remote.removeexport(param)
            
    def do_REMOVEEXPORTDIRECTORY(self, param):
        return self.remote.removeexportdirectory(param)
    
    def do_RENAMEEXPORT(self, param):
        parts = param.split(None, 1)
        if len(parts) != 2:
            raise SyntaxError("Expected TRANSFER STORE Key File")
        return self.remote.renameexport(parts[0], parts[1])

class Master:
    def __init__(self, output):
        self.output = output

    def LinkRemote(self, remote):
        self.remote = remote
        self.protocol = Protocol(remote)

    def Listen(self, input_):
        self.input = input_
        self.__send(self.protocol.version)
        for line in self.input:
            line = line.rstrip()
            try:
                reply = self.protocol.command(line)
                if isinstance(reply, Reply.RemoteReply):
                    self.__send(reply)
            except (UnsupportedRequest):
                self.__send ("UNSUPPORTED-REQUEST")
            except (NotImplementedError):
                self.__send ("ERROR not yet implemented")
                raise SystemExit
            #except Exception as e:
            #    self.__send ("ERROR", e)
            #    raise SystemExit
    
    def __ask(self, request, reply_keyword, reply_count):
        self.__send(request)
        line = self.input.readline().rstrip().split(maxsplit=reply_count)
        if line and line[0] == reply_keyword:
            line.extend([""] * (reply_count+1-len(line)))
            return line[1:]
        else:
            raise UnexpectedMessage(f"Expected {reply_keyword} and {reply_count} values. Got {line}")

    def __askvalues(self, request):
        self.__send(request)
        reply = []
        for line in self.input:
            line = line.rstrip()
            line = line.split(maxsplit=1)
            if len(line) == 2 and line[0] == "VALUE":
                 reply.append(line[1])
            elif len(line) == 1 and line[0] == "VALUE":
                return reply
            else:
                raise UnexpectedMessage("Expected VALUE {value}")

    def __askvalue(self, request):
        (reply,) = self.__ask(request, "VALUE", 1)
        return reply
    
    def getconfig(self, req):
        return self.__askvalue(f"GETCONFIG {req}")

    def setconfig(self, key, value):
        # make sure there is no whitespace
        for s in (key, value):
            if any([c in s for c in string.whitespace]):
                raise ValueError(f"Cannot set config. {s} contains whitespace")
        self.__send(f"SETCONFIG {key} {value}")

    def getstate(self, key):
        return self.__askvalue(f"GETSTATE {key}")

    def setstate(self, key, value):
        # make sure there is no whitespace
        for s in (key, value):
            if any([c in s for c in string.whitespace]):
                raise ValueError(f"Cannot set state. {s} contains whitespace")
        self.__send(f"SETSTATE {key} {value}")

    def debug(self, *args):
        self.__send("DEBUG", *args)

    def progress(self, progress):
        if type(progress) == int:
            self.send("PROGRESS", progress)
        else:
            raise TypeError("Expected integer")

    def dirhash(self, key):
        return self.__askvalue(f"DIRHASH {key}")

    def dirhash_lower(self, key):
        return self.__askvalue(f"DIRHASH-LOWER {key}")

    def setcreds(self, setting, user, password):
        self.__send("SETCREDS", setting, user, password)

    def getcreds(self, setting):
        (user, password) = self.__ask(f"GETCREDS {setting}", "CREDS", 2)
        return {'user': user, 'password': password}

    def getuuid(self):
        return self.__askvalue("GETUUID")

    def getgitdir(self):
        return self.__askvalue("GETGITDIR")

    def setwanted(self, prefcontent):
        self.__send("SETWANTED", prefcontent)

    def getwanted(self):
        return self.__askvalue("GETWANTED")

    def seturlpresent(self, key, url):
        self.__send("SETURLPRESENT", key, url)

    def seturlmissing(self, key, url):
        self.__send("SETURLMISSING", key, url)

    def seturipresent(self, key, uri):
        self.__send("SETURIPRESENT", key, uri)
    
    def seturimissing(self, key, uri):
        self.__send("SETURIMISSING", key, uri)

    def geturls(self, key, prefix):
        return askvalues(f"GETURLS {key} {prefix}")

    def __send(self, *args, **kwargs):
        print(*args, file=self.output, **kwargs)
        self.output.flush()
