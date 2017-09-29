#!/usr/bin/env python3.6
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
    
    # Wrapper for transfer_store and transfer_retrieve
    def transfer(self, method, key, file_):
        if method == "STORE":
            return self.transfer_store(key, file_)
        elif method == "RETRIEVE":
            return self.transfer_retrieve(key, file_)
   
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

    # Remote replies
    class RemoteReply():
        pass

    class PrepareFailure(RemoteReply):
        pass

    class InitremoteFailure(RemoteReply):
        pass

    class RemoteReply():
        pass

    class TransferSuccess(RemoteReply):
        pass

    class TransferFailure(RemoteReply):
        pass

    class CheckpresentSuccess(RemoteReply):
        pass

    class CheckpresentFailure(RemoteReply):
        pass

    class RemoveSuccess(RemoteReply):
        pass

    class RemoveFailure(RemoteReply):
        pass

    class ClaimurlSuccess(RemoteReply):
        pass

    class ClaimurlFailure(RemoteReply):
        pass

    class CheckurlSuccess(RemoteReply):
        pass

    class CheckurlFailure(RemoteReply):
        pass

    class WhereisSuccess(RemoteReply):
        pass

    class WhereisFailure(RemoteReply):
        pass

class Master:
    def __init__(self, output):
        self.output = output

    def LinkRemote(self, remote):
        self.remote = remote
        self.requests = { 
                     "INITREMOTE": remote.initremote,
                     "PREPARE": remote.prepare,
                     "TRANSFER": remote.transfer,
                     "CHECKPRESENT": remote.checkpresent,
                     "REMOVE": remote.remove,
                     "GETCOST": remote.getcost,
                     "GETAVAILABILITY": remote.getavailability,
                     "CHECKURL": remote.checkurl,
                     "WHEREIS": remote.whereis
                    }

    def Listen(self, input_):
        self.input = input_
        self.__send("VERSION 1")
        for line in self.input:
            line = line.rstrip()
            line = line.split()
            try:
                if line[0] not in self.requests.keys():
                    raise UnsupportedRequest()
                self.__send(self.requests[line[0]](*line[1:]))
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
            raise UnexpectedMessage(f"Expected {reply_keyword} and {reply_count} values")

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
