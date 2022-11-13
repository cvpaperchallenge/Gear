from __future__ import annotations

import json
import logging
import pathlib
from typing import Callable, Final, List

import jinja2
import pydantic

_logger: Final = logging.getLogger(__name__)
_LoadTemplate = Callable[[str], jinja2.Template]


class Contact(pydantic.BaseModel):
    display_name: str
    mail_address: str

    class Config:
        allow_mutation = False


class BaseMail(pydantic.BaseModel):
    title: str
    sender: Contact
    receiver: Contact
    cc_receivers: List[Contact] = []
    bcc_receivers: List[Contact] = []

    class Config:
        allow_mutation = False


class AdventCalendarContributionRequestMail(pydantic.BaseModel):
    mail: BaseMail
    expected_content: str

    class Config:
        allow_mutation = False


def from_yaml(
    file_path: pathlib.Path,
    model_class: pydantic.BaseModel,
) -> List[pydantic.BaseModel]:
    with file_path.open(mode="r") as f:
        loaded_pramaters = json.load(f)

    return [model_class.parse_obj(parameter) for parameter in loaded_pramaters]
