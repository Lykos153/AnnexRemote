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

from abc import ABC, abstractmethod

import sys
import string


# Exceptions
class Error(Exception):
    pass
class ProtocolError(Error):
    pass

class UnsupportedRequest(ProtocolError):
    pass

class UnexpectedMessage(ProtocolError):
    pass

class RemoteError(Error):
    pass

class SpecialRemote(ABC):

    def __init__(self, annex):
        self.annex = annex

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
        return True

    @abstractmethod
    def transferexport_store(self, key, file_, name):
        pass

    @abstractmethod
    def transferexport_retrieve(self, key, file_, name):
        pass

    @abstractmethod
    def checkpresentexport(self, key, name):
        pass

    @abstractmethod
    def removeexport(self, key, name):
        pass

    @abstractmethod
    def removeexportdirectory(self, directory):
        pass

    @abstractmethod
    def renameexport(self, key, name, new_name):
        pass

        
class Protocol:

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
        
        if len(reply)==1:
            entry = reply[0]
            if 'size' not in entry or entry['size'] is None:
                entry['size'] = "UNKNOWN"
                
            returnvalue = " ".join(("CHECKURL-CONTENTS", str(entry['size'])))
        
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

class Master:
    def __init__(self, output=sys.stdout):
        self.output = output

    def LinkRemote(self, remote):
        self.remote = remote
        self.protocol = Protocol(remote)

    def Listen(self, input_=sys.stdin):
        self.input = input_
        self._send(self.protocol.version)
        for line in self.input:
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
        for line in self.input:
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
        if type(progress) == int:
            self._send("PROGRESS", progress)
        else:
            raise TypeError("Expected integer")

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
