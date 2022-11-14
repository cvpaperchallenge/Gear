import logging
import os
import pathlib
from email.mime.text import MIMEText
from email.utils import formatdate
from typing import Final

from src.gondola.carrier import Gmail
from src.gondola.models import AdventCalendarContributionRequestMail, from_yaml
from src.gondola.renderer import Renderer, create_environment

_logger: Final = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

model_class: Final = {
    "advent_calendar_contribution_request": AdventCalendarContributionRequestMail,
}


def main(
    method_name: str,
    file_path: pathlib.Path,
    gmail_address: str = os.getenv("GMAIL_ADDRESS", ""),
    gmail_app_password: str = os.getenv("GMAIL_APP_PASSWORD", ""),
) -> None:
    mail_renderer: Final = Renderer(create_environment()).mail
    render_method: Final = getattr(mail_renderer, method_name)

    parameters: Final = from_yaml(
        file_path,
        model_class[method_name],
    )
    _logger.info(f"{len(parameters)} mail will be sent.")

    with Gmail(gmail_address, gmail_app_password) as carrier:
        for i, parameter in enumerate(parameters):
            message = MIMEText(render_method(parameter))
            message["Subject"] = parameter.mail.title
            message["From"] = parameter.mail.sender.mail_address
            message["To"] = parameter.mail.receiver.mail_address
            message["Cc"] = ",".join(
                [
                    cc_reciever.mail_address
                    for cc_reciever in parameter.mail.cc_receivers
                ]
            )
            message["Bcc"] = ",".join(
                [
                    bcc_reciever.mail_address
                    for bcc_reciever in parameter.mail.bcc_receivers
                ]
            )
            message["Date"] = formatdate()
            carrier.send_message(message)
            _logger.info(f"[{i+1}/{len(parameters)}] sending complete.")


if __name__ == "__main__":
    import argparse

    parser: Final = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "method",
        type=str,
    )
    parser.add_argument(
        "data",
        type=str,
    )

    args: Final = parser.parse_args()
    main(args.method, pathlib.Path(args.data))
