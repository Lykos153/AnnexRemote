#!/usr/bin/env python
import os
from pathlib import Path
from shutil import copyfileobj

from flask import (
    Blueprint,
    Flask,
    abort,
    current_app,
    request,
    send_file,
)
from werkzeug.utils import secure_filename


default_upload_folder = "./upload-folder"
default_port = 6987


git_annex_blueprint = Blueprint("git-annex", __name__)


def get_filepath(filename):
    filepath = Path(current_app.config["UPLOAD_FOLDER"], secure_filename(filename))
    return filepath


def safe_copy(fh, path):
    tmp_filepath = path.parent.joinpath("tmp", path.name)
    tmp_filepath.parent.mkdir(exist_ok=True, parents=True)
    with tmp_filepath.open("wb") as tfh:
        copyfileobj(fh, tfh)
        tmp_filepath.rename(path)


@git_annex_blueprint.route("/git-annex", methods=("PUT", "GET", "HEAD", "DELETE"))
def git_annex():
    # https://flask.palletsprojects.com/en/stable/patterns/fileuploads/
    match request.method:
        case "PUT":
            # check if the post request has the file part
            if not (file := request.files.get("file")) or not (
                filename := file.filename
            ):
                abort(404)
            else:
                filepath = get_filepath(filename)
                safe_copy(file.stream, filepath)
                return {"filepath": str(filepath)}
        case "GET":
            if not (filename := request.form.get("filename")):
                abort(400)
            filepath = get_filepath(filename)
            return send_file(filepath, as_attachment=True)
        case "HEAD":
            if (filename := request.form.get("filename")) is None:
                # HEAD with no filename is a healtcheck
                return {}
            if (filepath := get_filepath(filename)).exists():
                return {}
            else:
                abort(404)
        case "DELETE":
            if not (filename := request.form.get("filename")):
                abort(400)
            if (filepath := get_filepath(filename)).exists():
                filepath.unlink()
                return {"filepath": str(filepath)}
            else:
                return {}
        case _:
            raise ValueError(f"invalid method: {request.method}")


def make_app(upload_folder):
    app = Flask(__name__)
    app.register_blueprint(git_annex_blueprint)
    config_update = {
        k: v
        for k, v in (
            ("UPLOAD_FOLDER", upload_folder),
            ("SERVER_NAME", os.environ.get("SERVER_NAME")),
        )
        if v is not None
    }
    app.config.update(config_update)
    return app


def main(upload_folder=None, port=None):
    upload_folder = upload_folder or os.environ.get(
        "UPLOAD_FOLDER", default_upload_folder
    )
    port = port or os.environ.get("FLASK_RUN_PORT", default_port)
    app = make_app(upload_folder)
    app.run(port=port)


if __name__ == "__main__":
    main()
