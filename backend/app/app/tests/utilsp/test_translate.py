from sqlalchemy.orm import Session
from app import schemas, crud
from app.crud.base import CRUDBase
import pytest

#TODO : move this test in crud base test .
def test_detect_field(
    db:Session,
    ):
    question= schemas.QuestionCreate(
        label_eng='What is the question test',
        label_fr='',
        label_pt='', 
        datatype= 'TEXT',
        level='ma',
        is_active=True,
        mandatory=True
        )
    lang_label_corr={
        'label_eng': schemas.Lang.ENG,
        'label_fr': schemas.Lang.FR,
        'label_pt': schemas.Lang.PT,}
    lang_tab_corr={
            'tabheader_eng': schemas.Lang.ENG,
            'tabheader_fr': schemas.Lang.FR,
            'tabheader_pt': schemas.Lang.PT,
        }
    lang_subquestion_corr={
            'subquestion_eng': schemas.Lang.ENG,
            'subquestion_fr': schemas.Lang.FR,
            'subquestion_pt': schemas.Lang.PT,
        }
    lang_choices_corr={
            'choices_eng': schemas.Lang.ENG,
            'choices_fr': schemas.Lang.FR,
            'choices_pt': schemas.Lang.PT,
        }
    
    from_language,tos= crud.question.detect_fied_to_translate(question, lang_corr=lang_label_corr)
    assert from_language==(schemas.Lang.ENG, 'label_eng')
    assert tos==[(schemas.Lang.FR, 'label_fr'),(schemas.Lang.PT, 'label_pt') ]
    question= schemas.QuestionCreate(
        label_eng='What is the question test for table',
        label_fr='',
        label_pt='', 
        datatype= 'TABLE',
        tabheader_eng=["Name","Email"],
        tabheader_pt=[],
        tabheader_fr=[],
        level='ma',
        is_active=True,
        mandatory=True
        )
    from_language,tos= CRUDBase.detect_fied_to_translate(question, lang_corr=lang_tab_corr)
    assert from_language==(schemas.Lang.ENG, 'tabheader_eng')
    assert tos==[(schemas.Lang.FR, 'tabheader_fr'),(schemas.Lang.PT, 'tabheader_pt') ]
    answer=schemas.AnswerCreate(
        country_id=1,
        question_id=49,#wHERE YOUR headquarter is located
        value_string_eng='In the place you should be',
        no_translate=False
        )

    lang_string_corr={
        'value_string_eng': schemas.Lang.ENG,
        'value_string_fr': schemas.Lang.FR,
        'value_string_pt': schemas.Lang.PT,
    }
    from_language,tos= CRUDBase.detect_fied_to_translate(answer, lang_corr=lang_string_corr)
    assert from_language==(schemas.Lang.ENG, 'value_string_eng')
    assert tos==[(schemas.Lang.FR, 'value_string_fr'),(schemas.Lang.PT, 'value_string_pt') ]
    answer=schemas.AnswerCreate(
        country_id=1,
        question_id=66,#List of principals donators
        value_tab_eng=[['Aleks','Adresses','Email','Contact']],
        no_translate=False
        )
    lang_tab_ans_corr={
            'value_tab_eng': schemas.Lang.ENG,
            'value_tab_fr': schemas.Lang.FR,
            'value_tab_pt': schemas.Lang.PT,
        }
    from_language,tos= CRUDBase.detect_fied_to_translate(answer, lang_corr=lang_tab_ans_corr)
    assert from_language==(schemas.Lang.ENG, 'value_tab_eng')
    assert tos==[(schemas.Lang.FR, 'value_tab_fr'),(schemas.Lang.PT, 'value_tab_pt') ]

# @pytest.mark.skip()
def test_translate_field_question_create(
    db: Session
    ):
    question= schemas.QuestionCreate(
    label_eng='What is the question test',
    label_fr='',
    label_pt='', 
    datatype= 'TEXT',
    level='ma',
    is_active=True,
    mandatory=True
    )


    question= crud.question.create(db=db, obj_in=question)
    # #printquestion.label_fr)
    assert question.label_fr!=''
    question= schemas.QuestionCreate(
    label_eng='What is the best club on earth',
    label_fr='',
    label_pt='', 
    datatype= 'SUBQUESTION',
    subquestion_eng=['Name','contact','Email'],
    level='ma',
    is_active=True,
    mandatory=True
    )
    question= crud.question.create(db=db, obj_in=question)

    assert question.subquestion_fr!=[]

# @pytest.mark.skip()
def test_translate_field_question_update(db:Session):


    question= schemas.QuestionCreate(
    label_eng='What is the question test',
    label_fr='',
    label_pt='', 
    datatype= 'TEXT',
    level='ma',
    is_active=True,
    mandatory=True
    )


    question= crud.question.create(db=db, obj_in=question)

    question_update= schemas.QuestionUpdate(
    label_eng='What is the best club on earth',
    label_fr='',
    label_pt='', 
    datatype= 'SUBQUESTION',
    subquestion_eng=['Name','contact','Email'],
    level='ma',
    is_active=True,
    mandatory=True
    )
    question_up= crud.question.update(db=db, db_obj=question, obj_in=question_update)



# @pytest.mark.skip()
def test_translate_field_answer_create(db:Session):
    """
    Test the translation of answer or no if the no_translate is activated.
    """
    #The string datatype
    answer=schemas.AnswerCreate(
        country_id=1,
        question_id=49,#wHERE YOUR headquarter is located
        value_string_eng='In the place you should be',
        no_translate=False
        )
    ans=crud.answer.create(db=db,obj_in=answer)
    #printans.value_string_fr)
    assert ans.value_string_fr!=''
    #text
    # answer=schemas.AnswerCreate(
    #     country_id=1,
    #     question_id=??,#wHERE YOUR headquarter is located
    #     value_text_eng='In the place you should be',
    #     no_translate=False
    #     )
    # ans=crud.answer.create(db=db,obj_in=answer)
    # #printans.value_text_fr)
    # assert ans.value_text_fr!=''
    #choice
    answer=schemas.AnswerCreate(
        country_id=1,
        question_id=50,#Select the working language
        value_choices_eng=['French', "English"],
        no_translate=False
        )
    ans=crud.answer.create(db=db,obj_in=answer)
    #printans.value_choices_fr)
    assert ans.value_choices_fr!=''
    #table
    answer=schemas.AnswerCreate(
        country_id=1,
        question_id=66,#List of principals donators
        value_tab_eng=[['Aleks','Abengourou','aleksnougbele@gmail.com','+2250777010775']],
        no_translate=False
        )
    ans=crud.answer.create(db=db,obj_in=answer)
    #printans.value_tab_fr)
    assert ans.value_tab_fr!=''
    #subquestion

