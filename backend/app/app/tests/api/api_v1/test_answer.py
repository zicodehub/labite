from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.item import create_random_item
from  app.models.answer import Answer


# def test_create_answer(
#     client: TestClient, superuser_token_headers: dict, db: Session
# ) -> None:

#     data_table = {"answer_in":{"answer":[["ALEKS","9380303"]],"ma_id":"1","question_id":3,"value_floating":"0.0","value_string_eng":"0.0","value_string_fr":"0","value_string_pt":"","value_text_eng":"","value_text_fr":"","value_text_pt":"","value_choices_eng":[],"value_choices_fr":[],"value_choices_pt":[],"value_tab_eng":[["ALEKS","9380303"]],"user_pr_lang":"ENG"},"level":"ma"}

#     response = client.post(
#         f"{settings.API_V1_STR}/api/", headers=superuser_token_headers, json=data_table,
#     )
#     assert response.status_code == 200
#     content = response.json()
#     assert content["title"] == data["title"]
#     assert content["description"] == data["description"]
#     assert "id" in content
#     assert "owner_id" in content
def test_import_country(
    client: TestClient,
    superuser_token_headers: dict,
    db:Session
    )->None:
    with open('./app/tests/api/api_v1/Mozambique_import.csv','rb') as fp:
        data={'level':'country','level_id':36}
        response=client.post(f"{settings.API_V1_STR}/answer/template/import",headers=superuser_token_headers, files={'file':fp}, data=data)
        response=response.json()
        data_imported=db.query(Answer).filter(Answer.country_id==36, Answer.question_id==137).first()
        assert data_imported.value_choices_eng==['South Africa']

