# Key - Helper class to hold additional information about keys
#
# Copyright (C) 2021  Karl Semich
#
# This program is free software: you can redistribute it and/or modify it under the terms of version 3 of the GNU
# General Public License as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be uselful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

import collections

class Key(object):
    """
    Helper class to hold additional information about keys.

    '''
    Attributes
    ----------
    remote : SpecialRemote
        The SpecialRemote object this key is affiliated with.

    state : str
        The state associated with the key, stored in the git-annex branch, if any.
        May be mutated to update git-annex.

    size : Union(int, None)
        The size of the chunk of data represented by the key, if available.

    bytesize : Union(int, None)
        The size of the entire file the key refers to, if available.

    mtime : Union(int, None)
        The mtime of the key, if available.

    keyname : str
        The name portion of the key, containing its hash and possible extension.

    backend : str
        The key backend.

    key : str
        The whole key itself.

    chunk : Union(int, None)
        The chunk index of the key, if it uses chunking.
        Chunk indices start at 1.

    chunksize : Union(int, None)
        The chunk size for this file, if it uses chunking.
    """

    def __init__(self, key, remote):
        self.key = key
        self.remote = remote
        try:
            # name
            keyparts, self.keyname = key.split('--', 1)

            keyparts = keyparts.split('-')

            # chunking
            if len(keyparts) > 2 and keyparts[-1].startswith('C') and keyparts[-2].startswith('S'):
                self.chunk = int(keyparts.pop()[1:])
                self.chunksize = int(keyparts.pop()[1:])
            else:
                self.chunk = None
                self.chunksize = None

            # mtime
            if keyparts and keyparts[-1].startswith('m'):
                self.mtime = int(keyparts.pop()[1:])
            else:
                self.mtime = None
            
            # filesize
            if keyparts and keyparts[-1].startswith('s'):
                self.bytesize = int(keyparts.pop()[1:])
            else:
                self.bytesize = None

            # backend
            self.backend = keyparts.pop()
        except ValueError:
            raise RemoteError('bad key: ' + key)

        if len(keyparts):
            raise RemoteError('bad key: ' + key)

        if self.chunk and self.bytesize:
            if self.chunk * self.chunksize >= self.bytesize + self.chunksize:
                raise RemoteError('bad key: ' + key)

    def uris(self, prefix = ''):
        """
        The recorded URIs where a key can be downloaded from.

        Parameters
        ----------
        prefix : str
            Only uris that start with the prefix will be returned.
            The prefix may be empty to get all uris.

        Returns
        ----------
        UriList
            The URIs from which the key can be downloaded.
        """
        return UriList(self.key, self.remote.annex, prefix)

    @property
    def state(self):
        return self.remote.annex.getstate(self.key)

    @state.setter
    def state(self, value):
        self.remote.annex.setstate(self.key, value)

    @property
    def size(self):
        if not hasattr(self, '_size'):
            if self.chunksize:
                if self.bytesize:
                    # if this is the last chunk, the size may be truncated
                    if self.chunk * self.chunksize > self.bytesize:
                        self._size = self.bytesize % self.chunksize
                    else:
                        self._size = self.chunksize
                else:
                    # can't tell whether the size is truncated without the full size
                    self._size = None
            else:
                self._size = self.bytesize
        return self._size
        
    def __str__(self):
        return self.key

    def __repr__(self):
        return str(self)

class UriList(collections.MutableSet):
    """
    A list of URIs.

    This is a MutableSet of str which updates git-annex when mutated with add() or discard().

    Additionally may be indexed in the order git-annex returns the values.
    """

    def __init__(self, key, annex, prefix = ''):
        self._key = key
        self._annex = annex
        self._prefix = prefix
        self._uris = None

    @property
    def uris(self):
        if self._uris is None:
            self._uris = self._annex.geturls(self._key, self._prefix)
        return self._uris

    @classmethod
    def _from_iterable(cls, iterable):
        return set(iterable)

    def __contains__(self, uri):
        return uri in self.uris

    def __iter__(self):
        return iter(self.uris)

    def __len__(self):
        return len(self.uris)

    def __getitem__(self, idx):
        return self.uris[idx]

    def add(self, uri):
        if uri.split('://')[0].lower() in UriList.URL_SCHEMAS:
            self._annex.seturlpresent(self._key, uri)
        else:
            self._annex.seturipresent(self._key, uri)
        self._uris = None

    def discard(self, uri):
        if uri.split('://')[0].lower() in UriList.URL_SCHEMAS:
            self._annex.seturlmissing(self._key, uri)
        else:
            self._annex.seturimissing(self._key, uri)
        self._uris = None

    URL_SCHEMAS = set(('http', 'ftp', 'gopher', 'mailto', 'mid', 'cid', 'news', 'nntp', 'propsero', 'telnet', 'rlogin', 'tn3270', 'wais'))
