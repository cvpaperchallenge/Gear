import pytest

from src.gondola.models import BaseMail, Contact
from src.gondola.renderer import Renderer, create_environment


@pytest.fixture
def renderer():
    return Renderer(create_environment())


@pytest.fixture
def multiple_lines_text(text_name="multiple_lines_text"):
    def f(text_name=text_name):
        return (
            f"This is first line of {text_name}\n"
            f"This is second line of {text_name}\n"
            f"This is third line of {text_name}\n"
        )

    return f


@pytest.fixture
def contact(name="contact"):
    def f(name=name):
        return Contact(
            display_name=f"This is display_name of {name}",
            mail_address=f"This is mail_address of {name}",
        )

    return f


@pytest.fixture
def base_mail(
    contact,
):
    return BaseMail(
        title="This is title",
        sender=contact(name="sender"),
        receiver=contact(name="receiver"),
        cc_receivers=[contact(name="cc_receiver")],
        bcc_receivers=[contact(name="bcc_receiver")],
    )
