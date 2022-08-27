from app.utilsp.import_question import init_report
from sqlalchemy.orm import Session
from app import crud


def test_report(db:Session):
    init_report(db=db)
    reports=crud.report.get_all(db=db)
    assert len([k for k in reports if k.report_name=='the_initial_report'])>0