from __future__ import annotations

import logging
from typing import Callable, Final, List, Optional

import jinja2
import pydantic

_logger: Final = logging.getLogger(__name__)
_LoadTemplate = Callable[[str], jinja2.Template]


class Contact(pydantic.BaseModel):
    display_name: str
    mail_address: str

    class Config:
        allow_mutation = False


class BaseEmail(pydantic.BaseModel):
    title: str
    sender: Contact
    receiver: Contact
    cc_receivers: Optional[List[Contact]]
    bcc_receivers: Optional[List[Contact]]

    class Config:
        allow_mutation = False


class AdventCalendarContributionRequestMail(pydantic.BaseModel):
    mail: BaseEmail
    title: str
    abstract: str
    expected_content: str

    class Config:
        allow_mutation = False
