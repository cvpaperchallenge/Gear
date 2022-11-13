from __future__ import annotations

import logging
import pathlib
from typing import Callable, Final

import jinja2

from src.gondola import models

_logger: Final = logging.getLogger(__name__)
_LoadTemplate = Callable[[str], jinja2.Template]


def create_environment(
    template_dirpath: pathlib.Path = pathlib.Path(__file__).parent / "templates",
) -> jinja2.Environment:
    """ """
    environment: Final = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(template_dirpath)),
        autoescape=jinja2.select_autoescape(["jinja2"]),
        undefined=jinja2.StrictUndefined,
    )

    # Store template in cache of Environment.
    [environment.get_template(template) for template in environment.list_templates()]

    return environment


class _MailRenderer:
    def __init__(self, load_template: _LoadTemplate) -> None:
        self._load: Final = load_template

    def advent_calendar_contribution_request(
        self, parameter: models.AdventCalendarContributionRequestMail
    ) -> str:
        template_file: Final = "advent_calendar_contribution_request_2022.jinja2"
        return self._load(template_file).render(
            sender=parameter.mail.sender.display_name,
            receiver=parameter.mail.receiver.display_name,
            cc_receivers=[
                cc_receiver.display_name for cc_receiver in parameter.mail.cc_receivers
            ],
            expected_content=parameter.expected_content,
        )


class Renderer:
    """ """

    def __init__(self, environment: jinja2.Environment) -> None:
        self._environment: Final = environment
        self.mail: Final = _MailRenderer(self._load)

    def _load(self, name: str) -> jinja2.Template:
        return self._environment.get_template(name)
