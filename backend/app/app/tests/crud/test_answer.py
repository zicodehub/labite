from typing import Tuple
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app import models, schemas, crud
from app.tests.utils.utils import random_email, random_lower_string

def create_some_answer(db: Session) -> Tuple :
        question_in_tab = schemas.QuestionCreate(
            level=  schemas.Level.country.name,
            label_eng= 'the question ?' ,
            label_fr= 'Question test', 
            label_pt=  'questionna testo',
            datatype=  'CHOICE',
            tabheader_eng= ['choice1', 'choice 2'],
            tabheader_fr=  ['choice1', 'choice 2'],
            tabheader_pt=  ['choice1', 'choice 2'],
            multichoices=False,
            choicecreation=False,
            mandatory=False,
            is_active=True,
            user_lastmodifier=1
            )
        question = crud.question.create(db, obj_in= question_in_tab)
        answer_schema = schemas.AnswerCreate(
                country_id = 1,
                question_id = question.id,
                value_tab_eng = [['ans1_col1', 'ans1_col2' ], ['ans2_col1', 'ans2_col2' ], ['ans3_col1', 'ans3_col2' ]],
                comment_eng = "My comment",
                no_translate = True,
        )
        answer = crud.answer.create_with_modifier(db, obj_in= answer_schema)

        return answer, question, answer_schema, question_in_tab

def test_create_answer(db: Session) -> None:

    answer, question, ass, qss = create_some_answer()

    assert answer.question_id == question.id
    assert answer.status == schemas.AnswerStatus.DRAFT
    assert answer.comment_eng == ass.comment_eng
    assert answer.country_id == 1
    assert answer.value_file == None
    

def test_get_filter(db: Session) -> None:

    answer, question, ass, qss = create_some_answer()

    filters = schemas.AnswerSearch(query= 'ans1_col2')
    results = crud.answer.get_filter(db, filters)

    assert results is not None
    assert len(results) == 1
    
    found = results[0]

    assert found.id == answer.id 