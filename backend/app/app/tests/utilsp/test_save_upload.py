
from sqlalchemy.orm import Session
from app import schemas, crud
from app.crud.base import CRUDBase
from tempfile import NamedTemporaryFile

import pytest
from app.utilsp.uploads import save_upload_file
def test_save_upload():
    f=NamedTemporaryFile()
    f.close()
    ret=save_upload_file(f)
    #printret)
    assert False
