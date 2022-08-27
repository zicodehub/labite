
from app.utils import send_email, send_reset_password_email
from pathlib import Path
from app.core.config import settings
from app.utils import generate_password_reset_token
import pytest

@pytest.mark.skip()
def test_send_email():

    send_email(
        email_to="aleksnougbele@gmail.com",
        subject_template="test of sendgrid integration",

        environment={"project_name":"amap", "email":"aleksnougbele@gmail.com"}
    )
def test_send_reset_password_email():
    print(settings.EMAIL_TEST_USER)
    # assert False
    password_reset_token = generate_password_reset_token(email=settings.EMAIL_TEST_USER,)

    send_reset_password_email(email_to=settings.EMAIL_TEST_USER,
        email='aleksnougbele@gmail.com',
        token=password_reset_token
        )

