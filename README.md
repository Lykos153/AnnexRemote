# AnnexRemote
Helper module to easily develop special remotes for [git annex](https://git-annex.branchable.com).
AnnexRemote handles all the protocol stuff for you, so you can focus on the remote itself.
It implements the complete [external special remote protocol](https://git-annex.branchable.com/design/external_special_remote_protocol)
and fulfils all specifications regarding whitespaces etc.
Changes to the protocol are normally adopted within hours after they've been published without changing the interface for the remote.

## Getting started
### Prerequisites
In this module, I made heavy use of Python's f-strings, so compatibility is limited to v3.6+.
Fixing this is trivial, but I will probably only do this if requested. Feel free to open an issue or pull request.

### Installing
`pip3.6 install annexremote`

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
        # return true if the key is present in the remote
        # return false if the key is not present
        # raise RemoteError if the presence of the key couldn't be determined, eg. in case of connection error
        
    def remove(self, key):
        # remove the key from the remote
        # raise RemoteError if it couldn't be removed
        # note that removing a not existing key isn't considered an error
```

In your ``main`` function, link your remote to the master class and initialize the protocol:

```
def main():
    master = RemoteMaster()
    master.LinkRemote(MyRemote(master))
    master.Listen()

if __name__ == "__main__":
    main()
```

Now save your program as ``git-annex-remote-$something`` and make it executable.

``chmod +x git-annex-remote-$something``
(You'll need the sheebang line ``#!/usr/bin/env python3.6``)

That's it. Now you've created your special remote.

### Using other requests
A full documentation is being worked on. Until then, have a look at the test cases in order to see how the other methods are used.

## License

This project is licensed under GPLv3 - see the [LICENSE.md](LICENSE.md) file for details

