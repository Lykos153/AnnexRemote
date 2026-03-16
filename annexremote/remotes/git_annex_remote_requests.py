#!/usr/bin/env python
import sys
from contextlib import contextmanager
from pathlib import Path
from shutil import copyfileobj

import requests
from annexremote import (
    Master,
    RemoteError,
    SpecialRemote,
)


@contextmanager
def wrap_remote_error(exc):
    try:
        yield
    except exc as e:
        raise RemoteError(e)


class RequestsRemote(SpecialRemote):

    def listconfigs(self):
        return {
            # ALL parameters passed to initremote must be here
            "url": "url for remote",
        }

    @property
    def confignames(self):
        return tuple(self.listconfigs())

    def set_configs(self):
        for configname in self.confignames:
            configvalue = self.annex.getconfig(configname)
            setattr(self, configname, configvalue)

    def initremote(self):
        self.set_configs()
        missing_configs = tuple(
            configname for configname, value in self.listconfigs().items() if not value
        )
        if missing_configs:
            infix = ", ".join(f"{configname}=" for configname in missing_configs)
            raise RemoteError(f"You need to set {infix}")

    def prepare(self):
        self.set_configs()
        self.info = {
            configname: getattr(self, configname) for configname in self.confignames
        }
        # check that the server is alive
        resp = requests.head(self.url)
        assert resp.status_code == 200

    def transfer_store(self, key, filename):
        with wrap_remote_error(Exception):
            return self._do_put(key, filename)

    def transfer_retrieve(self, key, filename):
        with wrap_remote_error(Exception):
            return self._do_get(key, filename)

    def checkpresent(self, key):
        with wrap_remote_error(Exception):
            return self._do_exists(key)

    def remove(self, key):
        with wrap_remote_error(Exception):
            return self._do_drop(key)

    def _get_tmp_location(self, path):
        tmp_location = Path(path + ".tmp")
        return tmp_location

    def _do_get(self, key, local_file):
        tmp_location = self._get_tmp_location(local_file)
        with wrap_remote_error(Exception):
            with requests.get(self.url, data={"filename": key}, stream=True) as resp:
                resp.raise_for_status()
                with tmp_location.open("wb") as dest:
                    copyfileobj(resp.raw, dest)
                    tmp_location.rename(local_file)

    def _do_put(self, key, local_file):
        with wrap_remote_error(Exception):
            with Path(local_file).open("rb") as fh:
                files = {"file": (key, fh)}
                resp = requests.put(self.url, files=files)
                resp.raise_for_status()

    def _do_exists(self, key):
        with wrap_remote_error(Exception):
            resp = requests.head(self.url, data={"filename": key})
            return resp.status_code == 200

    def _do_drop(self, key):
        with wrap_remote_error(Exception):
            resp = requests.delete(self.url, data={"filename": key})
            resp.raise_for_status()


class RequestsExportRemote(RequestsRemote):

    def exportsupported(self):
        return True

    def transferexport_store(self, key, local_file, remote_file):
        """
        Requests the transfer of a file on local disk to the special remote.
        Note that it's important that, while a file is being stored,
        checkpresentexport() not indicate it's present until all the data
        has been transferred.
        While the transfer is running, the remote can send any number of progress(size) messages.


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
        self._do_put(remote_file, local_file)

    def transferexport_retrieve(self, key, local_file, remote_file):
        """
        Requests the transfer of a file from the special remote to the local disk.
        Note that it's important that, while a file is being stored,
        checkpresentexport() not indicate it's present until all the data
        has been transferred.
        While the transfer is running, the remote can send any number of progress(size) messages.


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
        self._do_get(remote_file, local_file)

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
        return self._do_exists(remote_file)

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
        self._do_drop(remote_file)


def main():
    output = sys.stdout
    sys.stdout = sys.stderr

    master = Master(output)
    remote = RequestsExportRemote(master)
    master.LinkRemote(remote)
    master.Listen()


if __name__ == "__main__":
    main()
