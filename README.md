# AnnexRemote
Helper module to easily develop special remotes for [git annex](https://git-annex.branchable.com).
AnnexRemote handles all the protocol stuff for you, so you can focus on the remote itself.
It implements the complete [external special remote protocol](https://git-annex.branchable.com/design/external_special_remote_protocol)
and fulfils all specifications regarding whitespaces etc. This is ensured by an excessive test suite.
Extensions to the protocol are normally added within hours after they've been published.

[Documentation](https://lykos153.github.io/AnnexRemote/annexremote/)

(Also have a look at the [examples](examples) and [git-annex-remote-googledrive](https://github.com/Lykos153/git-annex-remote-googledrive) which is based on AnnexRemote.)

## Getting started
### Prerequisites
You need python installed on your system. AnnexRemote has been tested with version 2.7 and 3.4 to 3.7.

### Installing
`pip install annexremote`

### Running the tests
If you want to run the tests, copy the content of the `tests` folder to the same location as `annexremote.py`.
Then use a test discovery like [nose](http://nose.readthedocs.io) to run them.

### Usage

Import the necessary classes

```
from annexremote import Master
from annexremote import SpecialRemote
from annexremote import RemoteError
```

Now create your special remote class. It must subtype ``SpecialRemote`` and implement at least the 6 basic methods:

```
class MyRemote(SpecialRemote):
    def initremote(self):
        # initialize the remote, eg. create the folders
        # raise RemoteError if the remote couldn't be initialized

    def prepare(self):
        # prepare to be used, eg. open TCP connection, authenticate with the server etc.
        # raise RemoteError if not ready to use

    def transfer_store(self, key, filename):
        # store the file in `filename` to a unique location derived from `key`
        # raise RemoteError if the file couldn't be stored

    def transfer_retrieve(self, key, filename):
        # get the file identified by `key` and store it to `filename`
        # raise RemoteError if the file couldn't be retrieved

    def checkpresent(self, key):
        # return True if the key is present in the remote
        # return False if the key is not present
        # raise RemoteError if the presence of the key couldn't be determined, eg. in case of connection error
        
    def remove(self, key):
        # remove the key from the remote
        # raise RemoteError if it couldn't be removed
        # note that removing a not existing key isn't considered an error
```

In your ``main`` function, link your remote to the master class and initialize the protocol:

```
def main():
    master = Master()
    remote = MyRemote(master)
    master.LinkRemote(remote)
    master.Listen()

if __name__ == "__main__":
    main()
```

Now save your program as ``git-annex-remote-$something`` and make it executable.

``chmod +x git-annex-remote-$something``
(You'll need the sheebang line ``#!/usr/bin/env python3``)

That's it. Now you've created your special remote.

#### Export remotes
Import and subtype `ExportRemote` instead of `SpecialRemote`:

```
# ...
from annexremote import ExportRemote

class MyRemote(ExportRemote):
    # implement the remote methods just like in the above example and then additionally:
    
    def transferexport_store(self, key, local_file, remote_file):
        # store the file located at `local_file` to `remote_file` on the remote
        # raise RemoteError if the file couldn't be stored

    def transferexport_retrieve(self, key, local_file, remote_file):
        # get the file located at `remote_file` from the remote and store it to `local_file`
        # raise RemoteError if the file couldn't be retrieved

    def checkpresentexport(self, key, remote_file):
        # return True if the file `remote_file` is present in the remote
        # return False if not
        # raise RemoteError if the presence of the file couldn't be determined, eg. in case of connection error

    def removeexport(self, key, remote_file):
        # remove the file in `remote_file` from the remote
        # raise RemoteError if it couldn't be removed
        # note that removing a not existing key isn't considered an error

    def removeexportdirectory(self, remote_directory):
        # remove the directory `remote_directory` from the remote
        # raise RemoteError if it couldn't be removed
        # note that removing a not existing directory isn't considered an error

    def renameexport(self, key, filename, new_filename):
        # move the remote file in `name` to `new_name`
        # raise RemoteError if it couldn't be moved

```

#### Logging
This module includes a StreamHandler to send log records to git annex via the special remote protocol (using DEBUG). You can use it like this:

```
...
import logging
...

def main():
    master = Master()
    remote = MyRemote(master)
    master.LinkRemote(remote)

    logger = logging.getLogger()
    logger.addHandler(master.LoggingHandler())

    master.Listen()

if __name__ == "__main__":
    main()
```


## License

This project is licensed under GPLv3 - see the [LICENSE](LICENSE) file for details

