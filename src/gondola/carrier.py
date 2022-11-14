from __future__ import annotations

import smtplib
from typing import Final


class Gmail:
    def __init__(
        self,
        gmail_address: str,
        gmail_app_password: str,
    ) -> None:
        self.gmail_address: Final = gmail_address
        self.gmail_app_password: Final = gmail_app_password
        self.smtp_obj: Final = smtplib.SMTP("smtp.gmail.com", 587)

    def __enter__(self) -> smtplib.SMTP:
        self.smtp_obj.ehlo()
        self.smtp_obj.starttls()
        self.smtp_obj.login(self.gmail_address, self.gmail_app_password)
        return self.smtp_obj

    def __exit__(self, exc_type, exc_value, traceback) -> None:  # type: ignore[no-untyped-def]
        self.smtp_obj.quit()
